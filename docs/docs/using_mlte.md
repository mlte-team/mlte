# Using `MLTE`

`MLTE` is a process and an infrastructure (a Python package) for machine learning model and system evaluation.

## Installation

If you already have Python installed you can install `MLTE` with

```bash
$ pip install mlte-python
```
or

```bash
$ conda install mlte-python
```
If you are new to Python and haven't installed it, we recommend starting with <a href="https://www.python.org/about/gettingstarted/" target="_blank">Python for Beginners</a>.

## Running the Backend and User Interface

The web-based user interface (UI or frontend) allows you to create and edit system artifacts, such as the Negotiation Card, and review existing models and test catalogs. It requires authentication for access and allows admins to manage users. To access the UI, first you need to start the backend server. See details for running each component.

### Backend

Running the backend can be done with the following command:

```bash
$ mlte backend
```

Some common flags used with the backend include the following:

 - **Artifact store**: the default artifact store will store any artifacts in a non-persistent, in-memory store. To change the store type, use the `--store-uri` flag. Please see the [Store URIs](#store-uris) section for details about each store type and corresponding URI. Note that this flag will also set the internal user store, used to handle users and permissions needed for the UI. To use a relational database to store artifacts, you will need to set up the database engine separately; see the [Using a Relational DB](#using-a-relational-db-engine-backend) section below for details. For example, to run the backend with a store located in a folder called `store` relative to the folder where you are running mlte, you can run the backend like this:

    ```bash
    $ mlte backend --store-uri fs://store
    ```

 - **Test catalog stores**: Optionally, you can specify one or more test catalog stores to be used by the system. This is done with the `--catalog-uris` flag, which is similar to the flag for artifact stores. Unlike that flag, however, catalogs need to have an ID, and this flag allows you to specify more than one test catalog if required. The value of this flag is a string with a dictionary with the ids and the actual store URIs. For example, to run the backend with two catalogs, one called "cat1" and another one called "cat2", the first one being in memory and the second one being in a local folder called `store`, you would run this command:

    ```bash
    $ mlte backend --catalog-uris '{"cat1": "memory://", "cat2": "fs://store"}'
    ```

 - **Token key**: The backend comes with a default secret for signing authentication tokens. In real deployments, you should define a new secret to be used for token signing instead of the default one. This can be done by either passing it as a command line argument with the `--jwt-secret` flag, or creating an `.env` file with the secret string on the variable `JWT_SECRET_KEY="<secret_string>"`

 - **Allowed origins**: In order for the frontend to be able to communicate with the backend, the frontend needs to be allowed as an origin in the backend. This can be done by specifying the `--allowed-origins` flag when starting the backend. When run through the `MLTE` package, the frontend will be hosted at `http://localhost:8080`. This address is configured to be allowed by default, so the flag does not need to be used by default, but if the frontend is hosted on another address then this flag needs to be set with the correct address.

 A sample artifact store is included in this repo, currently containing only a sample negotiation card artifact. To start the backend with this store, run it in this way from the root of this repo:

 ```bash
$ mlte backend --store-uri fs://demo/sample_store
```

### Frontend

Once the backend is running, you can run the frontend with the following command:

```bash
$ mlte ui
```

After this, go to the hosted address (defaults to `http://localhost:8000`) to view the `MLTE` UI homepage. You will need to log in to access the functionality in the UI, which you can do by using the default user. You can later use the UI to set up new users as well.

**NOTE**: you should change the default user's password as soon as you can, if you are not on a local setup.

* Default user: admin
* Default password: admin1234

For more information on how to use the UI, see our how-to guide on [using `MLTE`](using_mlte.md).

## Store URIs

The following are the types of store URIs used by the system.

- **In Memory Store** (``memory://``): a temporary, in memory store, useful for quick tests. Items stored here are not permanent. The URI for this store is simply the given string, without any parameters.

- **File System Store** (``fs://<store_path>``): a local file system store. The  ``<store_path>`` parameter has to be a path to an existing folder in your local system. The store will be created in subfolders inside it. This makes it easy to review the store contents by just opening the JSON files with their information.

- **Database Engine Store** (``<db_engine>://<db_user>:<db_password>@<db_host>/<db_name>``): a store in a relational database (DB) engine. By default, only PostgreSQL (``<db_engine> = postgresql``) is supported, but other engines can be added by simply installing the proper DBAPI drivers. See this <a href="https://docs.sqlalchemy.org/en/20/dialects/index.html" target="_blank">page</a> for details on supported drivers, and see section below on [Using a Relational DB](#using-a-relational-db-engine-backend) for more details on the other parameters on this URI.

- **HTTP Store** (``http://<user>:<password>@<host>:<port>``): this points to a store handled by a remote `MLTE` backend, which in turn will have a local store of one of the other three types. The ``<user>`` and ``<password>`` have to be valid credentials created by the `MLTE` frontend. The ``<host>`` and ``<port>`` point to the server where the `MLTE` backend is running (defaults to ``localhost`` and ``8080``). See the following section for instructions on setting up the `MLTE` backend and frontend.

### Using a Relational DB Engine Backend

To use a relational DB engine as a store, you first need to set up your DB engine separately. `MLTE` comes with DBAPI drivers installed for PostgreSQL; for other DB engines, you need to install the corresponding Python package drivers first.

To install your DB engine, you need to follow the specific instructions depending on the engine type. Usually the steps will include:

1. Download the DB engine installer (e.g., for PostgreSQL, get it from their <a href="https://www.postgresql.org/download/" target="_blank">downloads page</a>), and execute the installation as required for the DB engine.
   - Alternatively, you can download a docker container image with the proper database engine set up.
1. Ensure the DB engine is running (starting a container if applicable).
1. Use the DB's tools to create a user with DB creation permissions to be used by `MLTE`; or create a regular user for `MLTE`, and create the DB for `MLTE` manually using an existing user that can do that.
   - If using a container, this may just require you to specify environment variables for the container, which will create and set up the user automatically.

Then, you can just pass the URI for the DB store when running the `MLTE` backend, or when using `set_store` and using `MLTE` as a library.

Example of running the backend with PostgreSQL, a user called `mlte_user` with password `mlte_pass`, and database called `mlte` (which can exist previously or will be created by `MLTE` if possible):

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

- The negotiation facilitator should review the instructions and content of the Negotiation Card, which can be found in the `MLTE` user interface as described above. You can also refer to its [contents](negotiation_card.md).
- The negotiation is a collaborative discussion where all involved parties aim to agree on project requirements and discuss technical details.
- Once the negotiation is complete and the Negotiation Card is filled in as much as possible (it does not have to all be filled out at once), development can begin. The Negotiation Card gives the team a reference for project goals and allows them to plan out their development cycles appropriately.

## Internal Model Testing (IMT)

After initial model development has been completed, the team should have a model that is ready for preliminary testing. In IMT, the development team evaluates how the model performs against the baselines for the defined performance metrics for each system goal. Evaluation in `MLTE` follows this process:

1. Initialize the `MLTE` context.
2. Define a specification.
3. Collect evidence.
4. Validate results.
5. Examine findings.

### 1. Initialize the MLTE Context

`MLTE` contains a global context that manages the currently active session. Initializing the context tells `MLTE` how to store all of the artifacts that it produces. 

```python
set_context("OxfordFlower", "0.0.1")
set_store(f"local://{store_path}")
```
*Note that this code is demonstrative and does not include all imports and context; for a comprehensive example of `MLTE` code, see the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

### 2. Define a `Specification`

A `Specification` (or `Spec`) represents the requirements the model must meet in order to be acceptable for use in the system into which it will be integrated. Full `Spec` definition will be completed in [SDMT](#system-dependent-model-testing-sdmt); in IMT, we use it in a preliminary fashion so the development team can do an initial round of model testing. However, the process is the same for both stages. Here we define a `Spec` using storage cost and fairness as properties.

```python
from mlte.spec.spec import Spec
from mlte.qa_category.costs.storage_cost import StorageCost
from mlte.qa_category.fairness.fairness import Fairness

from mlte.measurement.storage import LocalObjectSize
from demo.scenarios.values.multiple_accuracy import MultipleAccuracy

spec = Spec(
    properties={
        Fairness(
            "Important check if model performs well accross different
            populations"
        ): {
            "accuracy across gardens": 
            MultipleAccuracy.all_accuracies_more_or_equal_than(
                0.9
            )
        },
        StorageCost("Critical since model will be in an embedded device"): {
            "model size": LocalObjectSize.value().less_than(150000000)
        }
    }
)
spec.save(parents=True, force=True)
```

### 3. Collect Evidence

After building the `Spec`, `MLTE` allows you to collect evidence to attest to whether or not the model realizes the desired properties. In this example, we wrap the output from `accuracy_score` with a custom `Result` type to cope with the output of a third-party library that is not supported by a MLTE builtin.

```python
from demo.scenarios.values.multiple_accuracy import MultipleAccuracy
from mlte.measurement.external_measurement import ExternalMeasurement

# Evaluate accuracy, identifier has to be the same one defined in the Spec.
accuracy_measurement = ExternalMeasurement(
    "accuracy across gardens", MultipleAccuracy, 
    calculate_model_performance_acc
)
accuracy = accuracy_measurement.evaluate(split_data[0], split_data[1])

# Inspect value
print(accuracy)

# Save to artifact store
accuracy.save(force=True)
```

*Note that this example does not include data and model training code, but those can be found in the full `MLTE` <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

### 4. Validate Results

Now that we have evidence and a `Spec`, we can create a `SpecValidator` and add all the `Value`s we have. With that we can generate a `ValidatedSpec` which contains validated results or *findings*.

```python
from mlte.spec.spec import Spec
from mlte.validation.spec_validator import SpecValidator
from mlte.value.artifact import Value

# Load the specification
spec = Spec.load()

# Add all values to the validator.
spec_validator = SpecValidator(spec)
spec_validator.add_values(Value.load_all())

# Validate requirements and get validated details.
validated_spec = spec_validator.validate()
validated_spec.save(force=True)

# We want to see the validation results in the Notebook, 
# regardless of them being saved.
validated_spec.print_results()
```

### 5. Examine Findings

To communicate results and examine findings, `MLTE` produces a report. While IMT is intended to be an initial and preliminary evaluation, the report is an artifact that will aid in the second [negotiation point](#negotiate-model-requirements-beyond-task-efficacy). You can import content from your negotiation card using the `MLTE` UI, and the fields can be customized as needed. The report is most easily generated using the UI, but can also be produced via code as demonstrated below.

```python
import time
from mlte.report import Report, Dataset, User, UseCase, Limitation

def unix_timestamp() -> str:
    return f"{int(time.time())}"

def build_report() -> Report:
    report = Report()
    report.metadata.project_name = "Your Project"
    report.metadata.authors = ["Jane Doe", "Joe Smith"]
    report.metadata.timestamp = unix_timestamp()

    report.model_details.name = "IrisClassifier"

    report.model_specification.domain = "Classification"
    report.model_specification.data = [
        Dataset("Dataset0", "https://github.com/mlte-team", 
        "This is one training dataset."),
        Dataset("Dataset1", "https://github.com/mlte-team", 
        "This is the other one we used."),
    ]

    report.considerations.users = [
        User("Botanist", "A professional botanist."),
        User("Explorer", "A weekend-warrior outdoor explorer."),
    ]
    return report
```
*Note that this example only includes a few of the report fields; a full `MLTE` report in code can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

Once the descriptive portions of the report are defined, you can render the report to examine your findings.

```python
from mlte.report.artifact import (
    Report,
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
)
from mlte.negotiation.artifact import NegotiationCard

report = Report(
    validated_spec_id=validated_spec.identifier,
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

IMT is an iterative process - the development team will likely repeat it several times given the exploratory nature of many machine learning projects.

## Negotiate Model Requirements Beyond Task Efficacy

After completing IMT, development teams should have a sense of how their model performs on the core project performance metric against the chosen baseline. After they have this additional information, the team conducts another negotiation amongst everyone involved in the project: stakeholders, software engineers, data scientists, and anyone else involved such as a project manager ot system/product owner.

- The emphasis of this negotiation is to review the discussion from [requirements negotiation](#negotiate-model-quality-requirements) and update it based on the intial evaluation that was performed in [IMT](#internal-model-testing-imt).
- It is also important to ensure that the development team has all the information they need to build a `Specification` (`Spec`) after this negotiation.
- It is likely that the first negotiation only resulted in some sections of the Negotiation Card being filled out, and a goal of this second negotiation should be to complete more of the sections and have a better picture of what project success will be.

Once the negotiation is complete and the contents of the Negotiation Card have been updated, the development team will conduct a comprehensive round of testing as part of System Dependent Model Testing.

## System Dependent Model Testing (SDMT)

SDMT ensures that a model will function as intended when it is part of a larger system. Using the updated Negotiation Card, development teams must define a `Specification` (`Spec`) that evaluates all relevant dimensions for the overall system to function. This follows the same process described in [IMT](#internal-model-testing-imt), with more emphasis on building out the specification. 

Teams can search the Test Catalog to find examples of how different quality attributes were tested by other teams. Note that MLTE comes with a sample test catalog simply for reference. The goal is for organizations to create and populate their own Test catalogs over time.

### Define a System-Oriented `Specification`

A `Spec` represents the requirements and corresponding thresholds (or validators) the completed model must meet in order to be acceptable for use in the system into which it will be integrated.

- Teams design a specification by selecting and prioritizing the model requirements that are important to their project from the list of `MLTE` [*properties*](properties.md). 
- To validate that a requirement for a property is met by an ML model and system, `MLTE` uses *measurements*, which correspond to properties. Selecting measurements that correspond to properties is part of `Spec` definition.

```python
from mlte.spec.spec import Spec

# The Properties we want to validate, associated with our scenarios.
from mlte.qa_category.costs.storage_cost import StorageCost
from mlte.qa_category.fairness.fairness import Fairness
from mlte.qa_category.robustness.robustness import Robustness
from mlte.qa_category.costs.predicting_memory_cost import PredictingMemoryCost

# The Value types we will use to validate each condition.
from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.memory import LocalProcessMemoryConsumption
from mlte.value.types.image import Image
from mlte.value.types.real import Real
from demo.scenarios.values.multiple_accuracy import MultipleAccuracy
from demo.scenarios.values.ranksums import RankSums
from demo.scenarios.values.multiple_ranksums import MultipleRanksums
from demo.scenarios.properties.resilience import Resilience
from demo.scenarios.properties.accuracy import Accuracy
from demo.scenarios.values.string import String


# The full spec. Note that the Robustness Property contains conditions for 
# both Robustness scenarios.
spec = Spec(
    properties={
        Fairness(
            "Important check if model performs well accross 
            different populations"
        ): {
            "accuracy across gardens": 
            MultipleAccuracy.all_accuracies_more_or_equal_than(
                0.9
            )
        },
        Robustness("Robust against blur and noise"): {
            "ranksums blur2x8": RankSums.p_value_greater_or_equal_to(0.05 / 3),
            "ranksums blur5x8": RankSums.p_value_greater_or_equal_to(0.05 / 3),
            "ranksums blur0x8": RankSums.p_value_greater_or_equal_to(0.05 / 3),
            "multiple ranksums for clade2": MultipleRanksums.all_p_values_greater_or_equal_than(
                0.05
            ),
            "multiple ranksums between clade2 and 3": 
            MultipleRanksums.all_p_values_greater_or_equal_than(
                0.05
            ),
        },
        StorageCost("Critical since model will be in an embedded device"): {
            "model size": LocalObjectSize.value().less_than(150000000)
        },
        PredictingMemoryCost(
            "Useful to evaluate resources needed when predicting"
        ): {
            "predicting memory": 
            LocalProcessMemoryConsumption.value().average_consumption_less_than(
                512000.0
            )
        }
    }
)
spec.save(parents=True, force=True)
```

### Collecting Evidence

After building the `Spec`, teams must collect evidence to attest to whether or not the model realizes the desired properties. Here we show one way to collect evidence. Note that this example does not include data and model training code, but those can be found in the full `MLTE` <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.

```python
from mlte.measurement.storage import LocalObjectSize
from mlte.value.types.integer import Integer

store_measurement = LocalObjectSize("model size")
size: Integer = store_measurement.evaluate(MODELS_DIR)
print(size)
size.save(force=True)
```

## Communicate ML Evaluation Results

To communicate results and examine findings, `MLTE` produces a report that encapsulates all knowledge gained about the model and the system as a consequence of the evaluation process. Teams can import content from the Negotiation Card using the `MLTE` UI, and the fields can be customized as needed. The report is most easily generated using the UI, but can also be defined via code as demonstrated below.

```python
from mlte.report.artifact import (
    Report,
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
)
from mlte.negotiation.artifact import NegotiationCard

report = Report(
    validated_spec_id=validated_spec.identifier,
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
*Note that this example only includes a few of the report fields; a full `MLTE` report in code can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo" target="_blank">demo notebooks</a>.*

If the model performs as desired, teams can consider the evaluation complete. However, it is very common that teams will need to iterate through [IMT](#internal-model-testing-imt) and [SDMT](#system-dependent-model-testing-sdmt) several times before they are satisfied with the results and ready to communicate with stakeholders.

## More Information

To reference diagrams or read in more depth about the process, see [`MLTE` Process](index.md). You can check out our [development](development.md) guide if you're interested in contributing, and if you want even more details about `MLTE`, feel free to check out our <a href="https://ieeexplore.ieee.org/document/10173876" target="_blank">paper</a>!