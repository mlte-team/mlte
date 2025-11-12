# Creating a new Demo

A demo is a set of Jupyter notebooks that walk through the MLTE IMT process. Demos are to be named and populated as follows. The number naming is used to signify the order in which the notebooks should be ran.

0. `session.py`
    - Each notebook will have to create a session module to handle setting up the `MLTE` context along with any other global values to be available throughout the demo. At a minimum, this module should set the context (model, version) and the store location.
    - An example can be found at `demo/GardenBuddy/session.py`
1. `all notebooks`
    - All notebooks will have to setup the `MLTE` context before their operation. This is done by importing the previously created session module.
    - All files outside of notebooks including the session module, data, or re-used functionality should be included within the folder for the demo.
2. `1_requirements.ipynb`
    - Defines the  `MLTE` [Negotiation Card](negotiation_card.md), an example card can be found at `demo/sample_store/models/OxfordFlower/card.default.json`. This can be created manually within the notebook, or loaded from a `.json` file of a card.
    - Defines the `TestSuite`, more `TestSuite` information can be found in [Using `MLTE`](using_mlte.md).
3. `2<x>_evidence_<quality_atribute>`
    - `<x>` being letters starting at `a` and continually incrementing, for example `2a_evidence_fairness`, `2b_evidence_robustness`, `2c_evidence_resilience`.
    - Each notebook should gather evidence for all the `TestCase`s that test a quality attribute scenario from the [Negotiation Card](negotiation_card.md) that relate to the quality attribute in the name of the notebook.
    - Each of these notebooks will be also used as an entry in the Sample Test Catalog to give an example of the `Test Case`s evaluated in the notebook. The second cell must contain a JSON block with information that will be used to populate the Test Catalog entry. All fields are required.
        - `Tags`: System-defined tags that are used in catalog search to group the catalog entries. Current options are found in `mlte/frontend/nuxt-app/composables/state.ts`as the const `useTagOptions`. These will be updated to be a custom list in the near future at which point a list of options will be found in `mlte/store/custom_list/tags`.
        - `Quality Attribute`: High-level quality attribute category that the notebook is validating. Options can be found in `mlte/store/custom_list/quality_attributes` and should match the quality attribute in the notebook name.
        - `Description`: Description of the scenario that this notebook is testing.
        - `Inputs`: Inputs to the model that are being tested.
        - `Outputs`: Expected output from the test.
            ```json
            {
                "tags": ["General"],
                "quality_attribute": "Detect OOD inputs and shifts in output",
                "description": "During normal operation, the ML pipeline will log errors when out of distribution data is observed. The ML pipeline will create a log entry with a tag. During normal operation, ML pipeline will log errors when the output distribution changes. The ML pipeline will create a log entry with a tag.",
                "inputs": "Existing ML model, sample image data that has out of bounds input, and that produces output confidence error",
                "output": "Log with input issues tagged",
            }
            ```
4. `3_report.ipynb`
    - Validate all test cases and generate a report to communicated the results of the evaluation.
    - If manual validation is needed for some of the test cases (they can't be automated), split into these three notebooks INSTEAD:
        - 4.1. `3a_automatic_validation.ipynb`
                - Create a `TestSuiteValidator` and validate the evidence collected
        - 4.2. `3b_manual_validation.ipynb`
                - Validate all test cases that need to be manually validated by the user, this may not apply in all cases.
        - 4.3. `3c_report.ipynb`
                - Generate a report to communicate the results of the evaluation.

## Populating the Sample Test Catalog

When demo notebooks have been created or edited and need to be added to the sample test catalog, it can be done automatically with the following command. This requires the demo dependencies to be installed and will go through all demos to update the entire sample catalog.

```bash
$ make build-sample-catalog
```

This is also done when `make qa` is ran, and will be checked to ensure all entries are updated within the CI.
