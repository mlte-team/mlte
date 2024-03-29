# Getting Started

Or, how to set up the `MLTE` infrastructure.

## Introduction

`MLTE` is a framework (a process to follow) and an infrastructure (a Python package) for machine learning model and system evaluation. This section focuses on setting up the infrastructure, which is an integral part of following the `MLTE` [framework](mlte_framework.md).

## Installation

If you already have Python installed you can install *`MLTE`* with

```bash
$ pip install mlte-python
```
or

```bash
$ conda install mlte-python
```
If you are new to Python and haven't installed it, we recommend starting with <a href="https://www.python.org/about/gettingstarted/" target="_blank">Python for Beginners</a>.

## Subpackages

`MLTE` contains the following subpackages:

- **Properties**: Properties are any attribute of the trained model, the procedure used to train it (including training data), or its ability to perform inference. A property is ‘abstract’ in the sense that there may be many ways in which it might be assessed. Developers will consider priorities, tradeoffs, and weaknesses of their model in the context of the system and prioritize properties for testing.  

- **Measurement**: Measurements are functions that assess phenomena related to the property of interest. For example, the total local process memory consumption is a *measurement* that measures the *property* of Training Memory Cost. 

- **Spec**: Specifications (Specs) are collections of properties and their associated measurements. Specs help organize the *`MLTE`* properties so that models can be easily re-evaluted. They are created by selecting the characteristics the model must exhibit to be considered acceptable. 

- **Report**: A *`MLTE`* report encapsulates all of the knowledge gained about the model and the system as a consequence of the evaluation process. The report renders as a web page and is opened automatically in an available window of the default browser. 


## Import

*`MLTE`* can be imported like any Python pacakge using the standard conventions.

```python
from mlte.properties ... #importing from properties subpackage
from mlte.measurement ... #importing from measurement subpackage
from mlte.spec ... #importing from spec subpackage
from mlte.report ... #importing from report subpackage
```

## Running the User Interface

To run the user interface (UI), run the following in your command line:
```bash
$ mlte ui
```

In order for the frontend to be able to communicate with the store you will need to allow the frontend as an origin.
This can be done by specifying the `--allowed-origins` flag when running the store. 
When ran through the mlte package, the frontend will be hosted at `http://localhost:8000` so the store command will look something like this:

```bash
$ mlte store --backend-uri fs://store --allowed-origins http://localhost:8000
```

Once you run it, go to the hosted address to view the `MLTE` UI homepage. For more information on how to use the UI, see our how-to guide on [using `MLTE`](using_mlte.md).

## Using a Relational DB Engine Backend

To use a relational DB engine as a backend for the store, you first need to set up your DB engine separately. MLTE comes with DBAPI drivers installed for PostgreSQL; for other DB engines, you need to install the corresponding Python package drivers first.

To install your DB engine, you need to follow the specific instructions depending on the engine type. Usually the steps will include:
1. Download the DB engine installer (e.g., for PostgreSQL, download it from https://www.postgresql.org/download/)
1. Execute the installation as required for the DB engine.
1. Ensure the DB engine is running.
1. Create a user with DB creation permissions to be used by MLTE (or create a regular user, and create the DB for MLTE manually using a superuser).

Then, you can just pass the URI for the DB backend when running the MLTE store, or when using `set_store` and using MLTE as a library.

Example of running the store backend with PostgreSQL, a user called `mlte_user` with password `mlte_pass`, and database called `mlte`:

```bash
$ mlte store --backend-uri postgresql://mlte_user:mlte_pass@localhost/mlte --allowed-origins http://localhost:8000
```

Example for setting the store inside code when you are using MLTE as a library:

`set_store("postgresql://mlte_user:mlte_pass@localhost/mlte")`

## Next Steps

Once you're set up, we recommend referencing our how-to guide on [using `MLTE`](using_mlte.md). You can also look at the full [`MLTE` framework](mlte_framework.md) or check out our [development](development.md) guide if you're interested in contributing.
