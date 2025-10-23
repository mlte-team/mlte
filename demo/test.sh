#!/usr/bin/env bash

# Set up script to stop tests when first one fails.
set -e 

# Remove everything from temp stores to avoid outdated data.
rm -rf ./store

# Set up base artifacts, like starting card.
(source setup_store.sh)

# Run all notebooks for the current demos.
DEMOS="$@"
for demo in ${DEMOS[@]}
do 
  for file in ${demo}/*.ipynb
  do
    poetry run pytest --nbmake "$file"
  done
done
