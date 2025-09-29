Steps to prepare a demo environment for UI interaction:

1. Execute the Requirements and Demos steps (and optionally the Python Version Support step if needed) in the Setup section in https://mlte.readthedocs.io/en/latest/development/#setup. 
2. Execute all notebooks in the subfolder for the required demo, so that the results can be seen in the notebooks themselves. This can be done in VSCode, or in another program that runs Jupyter Notebooks. Be sure to run the notebooks in the virtual environment created at the beginning, so that all dependencies are installed.
   > Optionally, this can be done with the command `make demo-test` from the root of the repo, which deletes the demo store and runs and tests all notebooks in the background.
3. Ensure that the Docker daemon is running.
4. Execute run_environment.sh from demo/ to get the frontend and backend working.
