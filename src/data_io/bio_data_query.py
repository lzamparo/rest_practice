from abc import ABC, abstractmethod
import requests
import time
from typing import Any, Dict, Optional, TypedDict, NotRequired
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import xml.etree.ElementTree as ET


class PubMedQuery(TypedDict):
    terms: list[str]
    fields: NotRequired[list[str]]  # Makes fields optional

class BioDatabaseInterface(ABC):
    def __init__(self, base_url: str, rate_limit: float = 0.34):
        self.base_url = base_url
        self.rate_limit = rate_limit
        self.session = self._create_retry_session()
    
    def _create_retry_session(self, retries: int = 3) -> requests.Session:
        """Create a session with retry logic"""
        session = requests.Session()
        retry = Retry(
            total=retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def query_db(self, endpoint: str, params: Dict[str, Any], 
                 method: str = 'GET', headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Generic database query method with rate limiting and error handling
        """
        url = f"{self.base_url}/{endpoint}"
        time.sleep(self.rate_limit)  # Rate limiting
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, params=params, headers=headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, params=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.RequestException as e:
            raise DatabaseQueryError(f"Error querying {url}: {str(e)}")

    @abstractmethod
    def search(self, query: dict[str, Any]) -> Any:
        """
        Abstract method that must be implemented by concrete classes
        """
        raise NotImplementedError("`search` must be implemented in subclasses")

class DatabaseQueryError(Exception):
    """Custom exception for database query errors"""
    pass

# Concrete implementation for PubMed
class PubMedClient(BioDatabaseInterface):
    def __init__(self):
        super().__init__("https://eutils.ncbi.nlm.nih.gov/entrez/eutils")

    def format_search_term(self, term: str, field: str = None) -> str:
        """
        Format a search term with proper PubMed syntax
        Examples:
            - major topic [majr]
            - MeSH terms [mh]
            - text words [tw]
            - title [ti]
            - title/abstract [tiab]
            N.B: for full text, use free full text[Filter]
            format_search_term("CRISPR Cas9", "ti") -> '"CRISPR Cas9"[ti]'
            format_search_term("cancer") -> 'cancer[all]'
        """
        # If term has spaces, wrap it in quotes
        formatted_term = f'"{term}"' if ' ' in term else term
        
        # Add field tag if specified, otherwise default to All Fields
        field_tag = f'[{field}]' if field else '[all]'
        return f'{formatted_term}{field_tag}'
    
    def search(self, query: PubMedQuery, retmax: int = 10) -> Dict:
        """
        Search PubMed and fetch title and abstract for each query result

        Args:
            query (PubMedQuery): TypedDict containing:
                - terms: List[str] - search terms (required)
                - fields: List[str] - corresponding fields for each term (optional)
            retmax (int, optional): _description_. Defaults to 10.

        Returns:
            Dict: _description_
        """

        terms = query['terms']
        fields = query.get('fields', ['all'] * len(terms))

        # Handle field specifications
        if fields is None:
            fields = ['All Fields'] * len(terms)
        elif len(fields) != len(terms):
            raise ValueError("Number of fields must match number of terms")

        # Format each term with its corresponding field
        formatted_terms = [
            self.format_search_term(term, field if field != 'All Fields' else None)
            for term, field in zip(terms, fields)
        ]
        
        # Join terms with AND
        # TODO: add support for OR in a grouping of terms?
        query = ' AND '.join(formatted_terms)

        # Search for IDs
        search_response = self.query_db(
            'esearch.fcgi',
            params={'db': 'pubmed', 'term': " AND ".join(terms), 'retmax': retmax, 'retmode': 'xml'}
        )
         # Parse XML response
        root = ET.fromstring(search_response.content)
        id_list = [id_elem.text for id_elem in root.findall('.//Id')]
        
        # Fetch details
        fetch_response = self.query_db(
            'efetch.fcgi',
            params={'db': 'pubmed', 'id': ','.join(id_list), 'rettype': 'abstract', 'retmode': 'json'}
        )
        return fetch_response.text


class EnsemblClient(BioDatabaseInterface):
    def __init__(self):
        super().__init__("https://rest.ensembl.org")
        self.rate_limit = 1.0

    def search(self, terms: list[str], species: str = "homo_sapiens") -> Dict:
        if len(terms) > 1:
            raise ValueError("EnsemblClient->search: Only one term at a time")
        headers = {"Content-Type": "application/json"}

        response = self.query_db(
            endpoint=f"lookup/symbol/{species}/{terms[0]}",
            params={"expand": 1},
            headers=headers
        )

        return response.json()
    
    def get_ensembl_id(self, symbol: str, species: str="homo_sapiens") -> str:
        data = self.search(terms=[symbol], species=species)
        
        # Get the first protein ID from the Translations
        if 'Transcript' in data:
            for transcript in data['Transcript']:
                if 'Translation' in transcript:
                    return transcript['Translation']['id']
        
        raise DatabaseQueryError(f"No protein ID found for gene {symbol}")


class StringDBClient(BioDatabaseInterface):
    def __init__(self):
        super().__init__("https://string-db.org/api")

    def map_ids(self, gene_names: list[str], species: int = 9606) -> Dict[str, str]:
        """
        Map gene names to STRING identifiers
        
        Args:
            gene_names: List of gene symbols
            species: NCBI taxonomy ID (default: 9606 for human)
            
        Returns:
            Dictionary mapping input gene names to STRING IDs
        """
        response = self.query_db(
            endpoint="json/get_string_ids",
            params={
                "identifiers": "\r".join(gene_names),
                "species": species,
                "format": "json"
            }
        )
        
        results = response.json()
        name_to_string_id = {}
        
        for result in results:
            if 'preferredName' in result and 'stringId' in result:
                name_to_string_id[result['preferredName']] = result['stringId']
                
        # Check for unmapped genes
        unmapped = set(gene_names) - set(name_to_string_id.keys())
        if unmapped:
            print(f"Warning: Could not map genes: {unmapped}")
            
        return name_to_string_id

    
    def search(self, terms: list[str], species: int = 9606) -> Dict:

        # First map the gene names to STRING IDs
        string_ids = self.map_ids(terms, species)
        
        if not string_ids:
            raise DatabaseQueryError("No genes could be mapped to STRING IDs")
        
        response = self.query_db(
            endpoint='json/interaction_partners',
            params={
                'identifiers': '\r'.join(string_ids.values()),
                'species': species,
                'required_score': 400,
                'network_type': 'physical',
            },
            method='POST'
        )
        return response.json()
    #https://string-db.org/api/[output-format]/network?identifiers=[your_identifiers]&[optional_parameters]