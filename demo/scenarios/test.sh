#!/usr/bin/env bash
CURR_FOLDER="./demo/scenarios"

# Remove everything from temp stores to avoid outdated data.
rm -r ${CURR_FOLDER}/store/models
mkdir -p ${CURR_FOLDER}/store/models

poetry run pytest --nbmake ${CURR_FOLDER}/1_requirements.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2_evidence.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2a_evidence_fairness.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2b_evidence_robustness.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2c_evidence_performance.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2d_evidence_interpretability.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2e_evidence_accuracy.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2f_evidence_interoperability.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2g_evidence_resilience.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/2h_evidence_monitorability.ipynb	
poetry run pytest --nbmake ${CURR_FOLDER}/2i_evidence_performance_time.ipynb
poetry run pytest --nbmake ${CURR_FOLDER}/3_report.ipynb
