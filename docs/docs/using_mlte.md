# Using `MLTE`

This section walks users through how to set up and run the `MLTE` Python package, as well as offering examples of how to use `MLTE` in machine learning projects.

## Installation

If you already have Python installed you can install `MLTE` with

```bash
$ pip install mlte
```
or

```bash
$ conda install mlte
```

To use the web UI (frontend/backend functionality), the `frontend` optional dependencies are needed; and to use relational database storage, the `rdbs` optional dependencies are needed. To install all optional dependencies:

```bash
$ pip install mlte[frontend,rdbs]
```

If you are new to Python and haven't installed it, we recommend starting with <a href="https://www.python.org/about/gettingstarted/" target="_blank">Python for Beginners</a>.

## Running the Backend and User Interface

The web-based user interface (UI or frontend) allows you to create and edit system artifacts, such as the Negotiation Card, and review existing models and test catalogs. It requires authentication for access and allows admins to manage users. To access the UI, first you need to start the backend server.

### Backend

Running the backend can be done with the following command:

```bash
$ mlte backend
```

Some common flags used with the backend include the following:

 - **Artifact store**: the default artifact store will store any artifacts in a non-persistent, in-memory store. To change the store type, use the `--store-uri` flag. Please see the [Store URIs](#store-uris) section for details about each store type and corresponding URI. Note that this flag will also set the internal user store, used to handle users and permissions needed for the UI. To use a relational database to store artifacts, you will need to set up the database engine separately; see the [Using a Relational DB](#using-a-relational-db-engine-backend) section below for details. As an example, to run the backend with a store located in a folder called `store` relative to the folder where you are running mlte, you can run the backend like this:

    ```bash
    $ mlte backend --store-uri fs://store
    ```

 - **Test catalog stores**: Optionally, you can specify one or more test catalog stores to be used by the system. This is done with the `--catalog-uris` flag, which is similar to the flag for artifact stores. Unlike that flag, however, catalogs need to have an ID, and this flag allows you to specify more than one test catalog if required. The value of this flag is a string with a dictionary with the ids and the actual store URIs. For example, to run the backend with two catalogs, one called "cat1" and another one called "cat2", the first one being in memory and the second one being in a local folder called `store`, you would run this command:

    ```bash
    $ mlte backend --catalog-uris '{"cat1": "memory://", "cat2": "fs://store"}'
    ```

 - **Token key**: The backend comes with a default secret for signing authentication tokens. In real deployments, you should define a new secret to be used for token signing instead of the default one. This can be done by either passing it as a command line argument with the `--jwt-secret` flag, or creating an `.env` file with the secret string on the variable `JWT_SECRET_KEY="<secret_string>"`

 - **Allowed origins**: In order for the frontend to be able to communicate with the backend, the frontend needs to be allowed as an origin in the backend. This can be done by specifying the `--allowed-origins` flag when starting the backend. When run through the `MLTE` package, the frontend will be hosted at `http://localhost:8080`. This address is configured to be allowed by default, so the flag does not need to be used by default, but if the frontend is hosted on another address then this flag needs to be set with the correct address.

 A sample artifact store is included in this repo, currently containing only a sample negotiation card artifact. To start the backend with this store, run it using the following command from the root of this repo:

 ```bash
$ mlte backend --store-uri fs://demo/sample_store
```

### Frontend

Once the backend is running, you can run the frontend with the following command:

```bash
$ mlte ui
```

After this, go to the hosted address (defaults to `http://localhost:8000`) to view the `MLTE` UI homepage. You will need to log in to access the functionality in the UI, which you can do by using the default user. You can later use the UI to set up new users as well.

**NOTE**: you should change the default user's password as soon as you can if you are not on a local setup.

* Default user: admin
* Default password: admin1234

## Store URIs

The following are the types of store URIs used by the system.

- **In Memory Store** (``memory://``): a temporary, in memory store, useful for quick tests. Items stored here are not permanent. The URI for this store is simply the given string without any parameters.

- **File System Store** (``fs://<store_path>``): a local file system store. The  ``<store_path>`` parameter has to be a path to an existing folder in your local system. The store will be created in subfolders inside it. This makes it easy to review the store contents by just opening the JSON files with their information.

- **Database Engine Store** (``<db_engine>://<db_user>:<db_password>@<db_host>/<db_name>``): a store in a relational database (DB) engine. By default, only PostgreSQL (``<db_engine> = postgresql``) is supported, but other engines can be added by simply installing the proper DBAPI drivers. See this <a href="https://docs.sqlalchemy.org/en/20/dialects/index.html" target="_blank">page</a> for details on supported drivers, and see section below on [Using a Relational DB](#using-a-relational-db-engine-backend) for more details on the other parameters for this URI.

- **HTTP Store** (``http://<user>:<password>@<host>:<port>``): this points to a store handled by a remote `MLTE` backend, which in turn will have a local store of one of the other three types. The ``<user>`` and ``<password>`` have to be valid credentials created by the `MLTE` frontend. The ``<host>`` and ``<port>`` point to the server where the `MLTE` backend is running (defaults to ``localhost`` and ``8080``). Refer to the [Running the Backend and User Interface](#running-the-backend-and-user-interface) section for instructions on setting up the `MLTE` backend and frontend.

### Using a Relational DB Engine Backend

To use a relational DB engine as a store, you first need to set up your DB engine separately. `MLTE` comes with DBAPI drivers installed for PostgreSQL; for other DB engines, you need to install the corresponding Python package drivers first.

To install your DB engine, you need to follow the specific instructions depending on the engine type. Usually the steps will include:

1. Download the DB engine installer (e.g., for PostgreSQL, get it from their <a href="https://www.postgresql.org/download/" target="_blank">downloads page</a>), and execute the installation as required for the DB engine.
   - Alternatively, you can download a docker container image with the proper database engine set up.
1. Ensure the DB engine is running (start a container if applicable).
1. Use the DB's tools to create a user with DB creation permissions to be used by `MLTE`; or create a regular user for `MLTE`, and create the DB for `MLTE` manually using an existing user that can do that.
   - If using a container, this may just require you to specify environment variables for the container, which will create and set up the user automatically.

Then, you can just pass the URI for the DB store when running the `MLTE` backend, or when using `set_store` and using `MLTE` as a library.

An example of running the backend with PostgreSQL, a user called `mlte_user` with password `mlte_pass`, and database called `mlte` (which can exist previously or will be created by `MLTE` if possible):

```bash
$ mlte backend --store-uri postgresql://mlte_user:mlte_pass@localhost/mlte
```

Example for setting the store inside code when you are using `MLTE` as a library:

```python
set_store("postgresql://mlte_user:mlte_pass@localhost/mlte")
```

## Setting up a `MLTE` session

Before most operations can be done using `MLTE`, a context and artifact store need to be set. When using `MLTE` as a library, there are two commands that can be executed once in a script to set this global state. They can be imported using

```python
from mlte.session import set_context, set_store
```

They are described and used in the following way:

- ``set_context("model_name", "model_version")``: this command indicates the model and version you will be working on for the rest of the script. It is mostly used to point to the proper location in the store when saving and loading artifacts. The model name and version can be any string.

- ``set_store("store_uri")``: this command indicates the location of the artifact store you will be using for the rest of the script. There are four store types, with the structure described in the [Store URIs](#store-uris) section.

Alternatively, these two things can also be set by environment variables before starting your Python script. If needed, these values can later be overriden in the script usng the set methods above.

- ``MLTE_CONTEXT_MODEL`` and ``MLTE_CONTEXT_VERSION`` to set the model and version.
- ``MLTE_ARTIFACT_STORE_URI`` to set the artifact store URI.

## Negotiate Model Quality Requirements

Now that you have the `MLTE` infrastructure set up, your team can hold a negotiation to discuss requirements with stakeholders. This should include system/product owners, software engineers, data scientists, and anyone else involved in the project. 

- The negotiation facilitator should review the instructions and content of the Negotiation Card, which can be found in the `MLTE` UI as described [above](#frontend). You can also refer to its [contents](negotiation_card.md).
- The negotiation is a collaborative discussion where all involved parties aim to agree on project requirements and discuss technical details.
- Once the negotiation is complete and the Negotiation Card is filled in as much as possible (it does not have to all be filled out at once), development can begin. The Negotiation Card gives the team a reference for project goals and allows them to plan out their development cycles appropriately.

## Testing Models with `MLTE` (IMT and SDMT)

While the `MLTE` [framework](index.md) has two distinct model testing steps - Internal Model Testing (IMT) and System Dependent Model Testing (SDMT) - both testing steps are identical in their mechanics. The difference is that generally teams will have a short `TestSuite` with very few `TestCase`s during IMT, and they will have a robust and extensive `TestSuite` during SDMT. Examples of this disparity can be seen by comparing notebooks between the <a href="https://github.com/mlte-team/mlte/tree/master/demo/simple" target="_blank">simple demo folder</a> and the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenario" target="_blank">scenario demo folder</a>. A brief overview of the two testing steps is below, or you can skip ahead to the [Model Testing](#model-testing) section.

### Internal Model Testing (IMT)

Internal Model Testing (IMT) is the process of initially evaluating a model with regard to the negotiated requirements. Teams use IMT tests after initial model development has been completed. The `MLTE` process assumes that ML development is an iterative process, so teams are encouraged to repeat IMT until they verify that model performance exceeds their specified thresholds.

### System Dependent Model Testing (SDMT)

After completing both IMT and a second negotiation, teams should have a robust Negotiation Card that includes information on all relevant dimensions for the overall system to function, with a focus on model and system-integration goals. In the second negotiation, teams use Quality Attribute Scenarios to help them determine relevant `TestCase`s and build out an appropriate `TestSuite` for Systen Dependent Model Testing (SDMT).

Teams can search the Test Catalog to find examples of how different quality attributes were tested by other teams. Note that `MLTE` comes with a sample test catalog simply for reference. The goal is for organizations to create and populate their own Test catalogs over time.

### Model Testing
When teams have a model that is ready for testing at either the IMT or SDMT stage, they will follow these steps to do so:

1. Define a `TestSuite`.
3. Collect `Evidence`.
4. Validate results.
5. Examine findings.

### 1. Define a `TestSuite`

A `TestSuite` is an artifact made up of a collection (or suite) of tests that the completed model must pass in order to be acceptable for use in the system into which it will be integrated. The `MLTE` `TestSuite` is  made up of smaller units, which we call a `TestCase`. Each `TestCase` includes a name or title, a goal, a link to a corresponding quality attribute in the Negotiation Card, a threshold, and finally a measurement. Measurements are optional and can be ignored, allowing teams to create and execute them later on in the development or evaluation process. Here is an example of a `TestCase`:

```python
TestCase(
        identifier="accuracy",
        goal="Understand if the model is useful for this case",
        qas_list=["qas1"],
        validator=Real.greater_or_equal_to(0.98),
        measurement=ExternalMeasurement(
            output_evidence_type=Real, function=accuracy_score
        )
)
```

To see a simple example of a `TestSuite`, refer to the `2_test_suite.ipynb` notebook in the <a href="https://github.com/mlte-team/mlte/tree/master/demo/simple" target="_blank">simple demo folder</a>. To see an example of a more extensive `TestSuite` including quality attribute scenarios, see the requirements notebook in the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">scenario demo folder</a>. All demos and corresponding instructions can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo folder</a>.

### 2. Collect `Evidence`

After building the `TestSuite`, `MLTE` requires developers to collect evidence to attest to whether or not the model realizes its stated goals. Each invididual piece of data produced by running a `Measurement` is an `Evidence`. Once `Evidence` is produced, developers persist them to an artifact store to maintain them across sessions. 

To generate `Evidence`, developers have two options: (1) they can specify `Measurement`s as part of their `TestSuite` as described [above](#1-define-a-testsuite), or (2) they can define `Measurement`s later on in the process. 

To see evaluation workflow 1 where `Measurement`s are defined in the `TestSuite`, see the <a href="https://github.com/mlte-team/mlte/tree/master/demo/simple" target="_blank">simple demo folder</a>. Below is an excerpt from evaluation workflow 2 where `Measurement`s are defined later on, and you can reference the full workflow in the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenario" target="_blank">scenario demo folder</a>.

```python
from mlte.measurement.external_measurement import ExternalMeasurement
from mlte.evidence.types.real import Real

# Evaluate, identifier has to be the same one defined in the TestSuite.
measurement = ExternalMeasurement(
    "overall accuracy", Real, calculate_model_performance_basic_acc
)
result = measurement.evaluate(df_results)

# Inspect value
print(result)

# Save to artifact store
result.save(force=True)
```

### 3. Validate Results

After collecting `Evidence`, refer back to the previously defined `TestSuite` to create a `TestSuiteValidator`. Doing so will validate each `TestCase` and generate output with the results of that validation, whcih is called `TestResults`. Here is an illustration of what that looks like in code:

```python
from mlte.validation.test_suite_validator import TestSuiteValidator

# Load validator for default TestSuite id
test_suite_validator = TestSuiteValidator()

# Load all Evidence and validate TestCases
test_results = test_suite_validator.load_and_validate()

# We want to see the validation results in the Notebook, regardless of them being saved.
test_results.print_results()

# TestResults also supports persistence
test_results.save(force=True)
```

### 4. Examine Findings

To communicate results and examine findings, `MLTE` produces a report. The `MLTE` report imports aspects of the Negotiation Card to ensure communication of findings based on the agreed upon project requirements. Reports can be viewed in the `MLTE` UI; here is an example of how to generate one:

```python
from mlte.report.artifact import (
    Report,
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
)
from mlte.negotiation.artifact import NegotiationCard

report = Report(
    test_results_id=test_results.identifier,
    comments=[
        CommentDescriptor(
            content="This model should not be used for nefarious purposes."
        )
    ],
    quantitative_analysis=QuantitiveAnalysisDescriptor(
        content="Insert graph here."
    ),
)

negotiation_card = NegotiationCard.load()
report = report.populate_from(negotiation_card)

report.save(force=True, parents=True)
```

If a team is at the [IMT](#internal-model-testing-imt) step of the `MLTE` process, they will likely need to continue developing and improving the model and conducting several iterations of evaluation before they are ready to move onto the second negotiation with their larger project team.

If a team is at the [SDMT](#system-dependent-model-testing-sdmt) step of the `MLTE` process, it is still likely that they will have to conduct several iterations but that refinements will be smaller than those executed during IMT. Once the model performs as desired, teams can consider the evaluation complete and ready to communicate with stakeholders.

More demonstration code can be found in the `MLTE` <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo folder</a>.

## More Information

To reference diagrams or read in more depth about the framework, see our documentation [landing page](index.md). You can check out our [development guide](development.md) if you're interested in contributing, and if you want even more details about `MLTE`, feel free to check out our <a href="https://ieeexplore.ieee.org/document/10173876" target="_blank">paper</a>!