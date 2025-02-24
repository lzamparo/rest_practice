import pytest
from data_io.bio_data_query import PubMedClient, StringDBClient
# set up fixtures
@pytest.fixture
def pubmed_term():
    return {'terms': ["CRISPR Cas9"], 'fields': ['tiab']}

@pytest.fixture
def nash_term():
    return {'terms': ["Nonalcoholic Steatohepatitis", "NASH", "LILRB2"], 'fields': ['tiab', 'tiab', 'tw']}

@pytest.fixture
def string_big_hits():
    return (["BRCA1", "TP53", "PTEN"], {'BRCA1': '9606.ENSP00000418960', 'TP53': '9606.ENSP00000269305', 'PTEN': '9606.ENSP00000361021'})

@pytest.fixture
def string_nash_potential_target():
    return ["LILRB2"]

@pytest.fixture
def ensembl_convert_pair():
    return ("ENSP00000375629", "LILRB2")

def test_pubmed_success(pubmed_term):
    pubmed = PubMedClient()
    terms = pubmed_term['terms'][0]
    crispr, cas9 = terms.split()
    pubmed_results = pubmed.search(query=pubmed_term)
    tokenized_results = pubmed_results.split()
    assert crispr in tokenized_results and cas9 in tokenized_results


def test_pubmed_target(nash_term):
    pubmed = PubMedClient()
    pubmed_results = pubmed.search(query=nash_term, retmax=50)
    assert pubmed_results is not None


def test_string_map_success(string_big_hits):
    gene_names, expected_results_dict = string_big_hits
    string_db = StringDBClient()
    string_results = string_db.map_ids(gene_names=gene_names, species=9606)
    for gene in gene_names:
        assert string_results[gene] == expected_results_dict[gene]

def test_string_target(string_nash_potential_target):
    string_db = StringDBClient()
    string_results = string_db.search(terms=string_nash_potential_target)
    assert string_results is not None
    for result in string_results:
        assert result['preferredName_A'] == string_nash_potential_target[0]
        assert result['preferredName_B'] != string_nash_potential_target[0]

