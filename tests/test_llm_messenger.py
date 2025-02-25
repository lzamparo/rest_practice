import pytest
from src.hypotheses.llm_messenger import LLMMessenger


@pytest.fixture(scope="session")
def llm_messenger():
    return LLMMessenger()


@pytest.fixture
def get_hypothesis_instructions_fixture(llm_messenger):
    return llm_messenger._get_hypothesis_instructions(
        file_path="./data/hypothesis_prompt"
    )


@pytest.fixture
def get_string_evidence():
    return [
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000366024', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-G', 'ncbiTaxonId': 9606, 'score': 0.999, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.955, 'dscore': 0.5, 'tscore': 0.982}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000379873', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-A', 'ncbiTaxonId': 9606, 'score': 0.984, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.405, 'dscore': 0.5, 'tscore': 0.953}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000259951', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-F', 'ncbiTaxonId': 9606, 'score': 0.983, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.549, 'dscore': 0.5, 'tscore': 0.933}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000399168', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-B', 'ncbiTaxonId': 9606, 'score': 0.981, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.549, 'dscore': 0.5, 'tscore': 0.925}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000497910', 'preferredName_A': 'LILRB2', 'preferredName_B': 'B2M', 'ncbiTaxonId': 9606, 'score': 0.979, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.96, 'dscore': 0.5, 'tscore': 0}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000362524', 'preferredName_A': 'LILRB2', 'preferredName_B': 'ANGPTL2', 'ncbiTaxonId': 9606, 'score': 0.963, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.483, 'dscore': 0, 'tscore': 0.932}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000391592', 'preferredName_A': 'LILRB2', 'preferredName_B': 'PTPN6', 'ncbiTaxonId': 9606, 'score': 0.943, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.457, 'dscore': 0.9, 'tscore': 0}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000364898', 'preferredName_A': 'LILRB2', 'preferredName_B': 'SYK', 'ncbiTaxonId': 9606, 'score': 0.9, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0, 'dscore': 0.9, 'tscore': 0}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000365402', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-C', 'ncbiTaxonId': 9606, 'score': 0.89, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.549, 'dscore': 0.5, 'tscore': 0.555}",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000359345', 'preferredName_A': 'LILRB2', 'preferredName_B': 'RPL5', 'ncbiTaxonId': 9606, 'score': 0.755, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0, 'dscore': 0, 'tscore': 0.755}",
    ]


@pytest.fixture
def get_positive_string_test():
    return (
        "HLA-G likely interacts physically with LILRB2",
        "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000366024', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-G', 'ncbiTaxonId': 9606, 'score': 0.999, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.955, 'dscore': 0.5, 'tscore': 0.982}",
    )


@pytest.fixture
def get_negative_string_test():
    return (
        "HLA-F likely interacts physically with LILRB2",
        [
            "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000366024', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-G', 'ncbiTaxonId': 9606, 'score': 0.4, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.3, 'dscore': 0.1, 'tscore': 0.212}",
            "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000379873', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-A', 'ncbiTaxonId': 9606, 'score': 0.3, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 025, 'dscore': 0.1, 'tscore': 0.222}",
            "{'stringId_A': '9606.ENSP00000375629', 'stringId_B': '9606.ENSP00000259951', 'preferredName_A': 'LILRB2', 'preferredName_B': 'HLA-F', 'ncbiTaxonId': 9606, 'score': 0.1, 'nscore': 0, 'fscore': 0, 'pscore': 0, 'ascore': 0, 'escore': 0.1, 'dscore': 0.03, 'tscore': 0.111}",
        ],
    )


## test below here


def test_positive_string(get_positive_string_test, llm_messenger):
    query, context = get_positive_string_test
    instructions = [
        "please provide an answer that begis with yes or no, with justification that follows"
    ]
    response = llm_messenger.generate_response(
        query=query, context=context, instructions=instructions
    )
    assert ("Yes" in response.text) or ("yes" in response.text)


def test_negative_string(get_negative_string_test, llm_messenger):
    query, context = get_negative_string_test
    instructions = [
        "please provide an answer that begis with yes or no, with justification that follows"
    ]
    response = llm_messenger.generate_response(
        query=query, context=context, instructions=instructions
    )
    assert ("No" in response.text) or ("no" in response.text)


def test_retrieve_detailed_instructions(get_hypothesis_instructions_fixture):
    instructions = get_hypothesis_instructions_fixture
    assert len(instructions) > 0
