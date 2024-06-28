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

## Using MLTE as a library

### Subpackages

`MLTE` contains the following subpackages:

- **Properties**: Properties are any attribute of the trained model, the procedure used to train it (including training data), or its ability to perform inference. A property is ‘abstract’ in the sense that there may be many ways in which it might be assessed. Developers will consider priorities, tradeoffs, and weaknesses of their model in the context of the system and prioritize properties for testing.  

- **Measurement**: Measurements are functions that assess phenomena related to the property of interest. For example, the total local process memory consumption is a *measurement* that measures the *property* of Training Memory Cost. 

- **Spec**: Specifications (Specs) are collections of properties and their associated measurements. Specs help organize the *`MLTE`* properties so that models can be easily re-evaluted. They are created by selecting the characteristics the model must exhibit to be considered acceptable. 

- **Report**: A *`MLTE`* report encapsulates all of the knowledge gained about the model and the system as a consequence of the evaluation process. The report renders as a web page and is opened automatically in an available window of the default browser. 

### Import

*`MLTE`* can be imported like any Python pacakge using the standard conventions.

```python
from mlte.property ... #importing from properties subpackage
from mlte.measurement ... #importing from measurement subpackage
from mlte.spec ... #importing from spec subpackage
from mlte.report ... #importing from report subpackage
```

### Setting a MLTE session

Before most operations can be done on MLTE, a context and store need to be set. When using MLTE as a library, there are two commands that can be executed once on a script to set this global state. They can be imported like so:

```python
from mlte.session import set_context, set_store
```

They are used in the following way:
- ``set_context("model_name", "model_version")``: this command indicates the model and version you will be working on for the rest of the script. It is mostly used to point to the proper location in the store when saving and loading artifacts. The model name and version can be any string.
- ``set_store("store_uri")``: this command indicates the location of the artifact store you will be using for the rest of the script. There are four store types, with the following URI structure:
  - **In Memory Store** (``memory://``): a temporary, in memory store, useful for quick tests. Artifacts stored here are not permanent. The URI for this store is simply the given string, without any parameters.
  - **File System Store** (``fs://<store_path>``): a local file system artifact store. The  ``<store_path>`` parameter has to be a path to an existing folder in your local system. The store will be created in subfolders inside it. This makes it easy to review the artifacts by just opening the JSON files with their information.
  - **Database Engine Store** (``<db_engine>://<db_user>:<db_password>@<db_host>/<db_name>``): a store in a relational database engine. By default, only PostgreSQL (``<db_engine> = postgresql``) is supported, but other engines can be added by simply installing the proper DBAPI drivers. See this page for details on supported drivers: https://docs.sqlalchemy.org/en/20/dialects/index.html . See section below on Using a Relational DB for more details on the other parameters on this URI.
  - **HTTP Store** (``http://<user>:<password>@<host>:<port>``): this points to a store handled by a remote MLTE backend, which in turn will have a local store of one of the other three types. The ``<user>`` and ``<password>`` have to be valid credentials created by the MLTE frontend. The ``<host>`` and ``<port>`` point to the server where the MLTE backend is running (defaults to ``localhost`` and ``8080``). See the following section for instructions on setting up the MLTE backend and frontend.


## Running the User Interface

To run the user interface (UI or frontend), first you need to start the backend server. Running the backend can be done with the following command:

```bash
$ mlte backend
```

However, by default this will store any artifacts in a non-persistent, in-memory store. You also have the option to use a folder to store artifacts, or a relational database, using the `--store-uri` flag. For the latter, see the appropriate section below. For the former, you have to specify a relative or absolute folder path with the `fs://` prefix. For example, to run the backend with a store located in a folder called `store` relative to the folder where you are running mlte, you can run the backend like this:

```bash
$ mlte backend --store-uri fs://store
```

Once the backend is running, you can run the frontend with the following command:

```bash
$ mlte ui
```

After this, go to the hosted address (defaults to `http://localhost:8000`) to view the `MLTE` UI homepage. You will need to log in to access the functionality in the UI. You can start using the default user. You can later use the UI to set up new users as well.

NOTE: you should change the default user's password as soon as you can, if you are not on a local setup.

* Default user: admin
* Default password: admin1234

For more information on how to use the UI, see our how-to guide on [using `MLTE`](using_mlte.md).

## Backend Considerations

The backend comes with a default secret for signing authentication tokens. In real deployments, you should define a new secret to be used for token signing, instead of the default one. This can be done by either creating an `.env` file with the secret string on the variable `JWT_SECRET_KEY="<secret_string>"`, or passing it as a command line argument with the `--jwt-secret` flag.

In order for the frontend to be able to communicate with the backend the frontend need to be allowed as an origin. This can be done by specifying the `--allowed-origins` flag when starting the backend. When ran through the mlte package, the frontend will be hosted at `http://localhost:8000`. This address is configured to be allowed by default, so the flag does not need to be used by default, but if the frontend is hosted on another address, this flag needs to be set with the correct address.


### Using a Relational DB Engine Backend

To use a relational DB engine as a store, you first need to set up your DB engine separately. MLTE comes with DBAPI drivers installed for PostgreSQL; for other DB engines, you need to install the corresponding Python package drivers first.

To install your DB engine, you need to follow the specific instructions depending on the engine type. Usually the steps will include:

1. Download the DB engine installer (e.g., for PostgreSQL, download it from https://www.postgresql.org/download/)
1. Execute the installation as required for the DB engine.
1. Ensure the DB engine is running.
1. Create a user with DB creation permissions to be used by MLTE (or create a regular user, and create the DB for MLTE manually using a user that can do that).

Then, you can just pass the URI for the DB store when running the MLTE backend, or when using `set_store` and using MLTE as a library.

Example of running the backend with PostgreSQL, a user called `mlte_user` with password `mlte_pass`, and database called `mlte`:

```bash
$ mlte backend --store-uri postgresql://mlte_user:mlte_pass@localhost/mlte --allowed-origins http://localhost:8000
```

Example for setting the store inside code when you are using MLTE as a library:

`set_store("postgresql://mlte_user:mlte_pass@localhost/mlte")`

## Next Steps

Once you're set up, we recommend referencing our how-to guide on [using `MLTE`](using_mlte.md). You can also look at the full [`MLTE` framework](mlte_framework.md) or check out our [development](development.md) guide if you're interested in contributing.
