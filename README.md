# Analysis notebooks for the presentation "Una questione di qualità: l'uso dei connettivi nelle produzioni scritte di studenti italofoni".

These analyses have been presented at University of Basel, on 13-14 November 2024.

The research questions are:

* Does the use of connectives (in terms of number of tokens, RTTR, sophistication and range) change as a function of training in writing?
* Does number of connectives, variety (RTTR) or sophistication of connectives used correlate with holistic judgements of textual coherence?
* Does accuracy in using connectives correlates with holistic judgements of textual coherence?
  * If so, which are the most 'problematic' connectives?
  * Which are the most 'problematic' discourse relations?

This repo contains two analysis notebooks:
* `RQ1.ipynb` answers research question 1 and extends analysis done for Bienati & Frey (in print) and available at https://gitlab.inf.unibz.it/commul/lca/lcr22_itaca
* `RQ2_3.ipynb` contains code to answer research questions 2 and 3.

And a python script:
* `process_ratings.py` cleans the holistic ratings of textual coherence. It is recommended to run the `process.ratings.py` in advance so to have all materials ready for the analysis.

To run `process_ratings.py`, make sure you have Python installed.
Then:

1. open a new terminal
2. create a virtual environment (e.g., `python3 -m venv .venv`)
2. acrivate the virtual environment (`source .venv/bin/activate`)
3. install pandas (`pip install pandas`)
4. create an 'output' folder (`mkdir output`)

The scripts creates a clean version of the ratings and related documentation.

To run the notebooks, you need to have R and Jupyter Notebooks installed.
Make sure that all required packages are installed. If not, install them using `install.packages()`.

For any feedback or issues, please use the "Issues" tab, or contact me at arianna (dot) bienati (at) eurac (dot) edu.
