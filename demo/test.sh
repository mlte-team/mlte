#!/usr/bin/env bash

# Set up script to stop tests when first one fails.
set -e

# Remove everything from temp stores to avoid outdated data.
rm -rf ./store

# Set up base artifacts, like starting card.
cp -r ./sample_store ./store

# Ensure proper order of notebooks.
LC_COLLATE=C

# Run all notebooks for the current demos.
DEMOS="$@"
for demo in ${DEMOS[@]}
do 
  for file in ${demo}/*.ipynb
  do
    # Avoid running this notebook when the API key is missing, as it relies on an OpenAI API key that we cannot have configured by default
    if [[ "$file" == "ReviewPro/2f_evidence_time_behavior.ipynb" ]] && [[ -z "$OPENAI_API_KEY" ]]; then
      echo "Skipping notebook that requires unset API key env var."
    else
      poetry run pytest --nbmake "$file"
    fi
  done
done
