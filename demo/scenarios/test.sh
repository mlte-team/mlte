#!/usr/bin/env bash

# Remove everything from temp stores to avoid outdated data.
rm -r ./store/models
mkdir -p ./store/models

poetry run pytest --nbmake ./demo/scenarios/1_requirements.ipynb
poetry run pytest --nbmake ./demo/scenarios/2_evidence.ipynb
poetry run pytest --nbmake ./demo/scenarios/2a_evidence_fairness.ipynb
poetry run pytest --nbmake ./demo/scenarios/2b_evidence_robustness.ipynb
poetry run pytest --nbmake ./demo/scenarios/2c_evidence_performance.ipynb
poetry run pytest --nbmake ./demo/scenarios/2d_evidence_interpretability.ipynb
poetry run pytest --nbmake ./demo/scenarios/2e_evidence_accuracy.ipynb
poetry run pytest --nbmake ./demo/scenarios/2f_evidence_interoperability.ipynb
poetry run pytest --nbmake ./demo/scenarios/2g_evidence_resilience.ipynb
poetry run pytest --nbmake ./demo/scenarios/2h_evidence_monitorability.ipynb	
poetry run pytest --nbmake ./demo/scenarios/2i_evidence_performance_time.ipynb
poetry run pytest --nbmake ./demo/scenarios/3_report.ipynb
