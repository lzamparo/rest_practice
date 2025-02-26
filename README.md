REST api plus Gemeni 
======================
An exercise in querying different REST apis, and pulling them together for composing queries to Gemini for hypothesis generation.

## The idea
Imagine you're looking to think about generating hypotheses: you're studying a disease, you have some protein that's implicated, you sense that there's something worth pursuing.
But how do you flesh this out into a larger hypothesis that's (a) plausible and (b) supported by some other evidence?  It's 2025, let's try to off-load some of the literature search
and curation to LLMs.

### How to run it?
1. Install `uv`
2. clone the repo, cd into the repo
3. run `uv sync` to re-create the `venv`
4. configure credentials to use the Google Gemeni API (e.g setting up `GOOGLE_API_KEY` as an environment var)
5. use the notebook in `src/drive)_hypothesis_generation.ipynb`

### In src
- module for REST api IO and data transformation
- module for packaging and querying the Gemini API directly 

### In tests
- Minimal set of unit tests to ensure the various components work. 
- The Gemeni queries should probably should be mocked, or at least have the response interface better defined so I can avoid hitting the api in tests.
