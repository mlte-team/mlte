#!/usr/bin/env bash
DEMO_FOLDER="${1:-.}"

# Remove everything from temp stores to avoid outdated data.
rm -r ${DEMO_FOLDER}/store/models
mkdir -p ${DEMO_FOLDER}/store/models

# Run all notebooks.
for file in ${DEMO_FOLDER}/*.ipynb
do
  poetry run pytest --nbmake "$file"
done
