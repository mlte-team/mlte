# Setting Up `MLTE`

`MLTE` is a process and an infrastructure (a Python package) for machine learning model and system evaluation. This section focuses on setting up the infrastructure, which is an integral part of following the `MLTE` [process](index.md).

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

## Using `MLTE` as a library

### Importing

`MLTE` contains the following subpackages:

- **Properties**: Properties are any attribute of the trained model, the procedure used to train it (including training data), or its ability to perform inference. A property is ‘abstract’ in the sense that there may be many ways in which it might be assessed. Developers will consider priorities, tradeoffs, and weaknesses of their model in the context of the system and prioritize properties for testing.  

- **Measurement**: Measurements are functions that assess phenomena related to the property of interest. For example, the total local process memory consumption is a *measurement* that measures the *property* of Training Memory Cost. 

- **Spec**: Specifications (Specs) are collections of properties and their associated measurements. Specs help organize the *`MLTE`* properties so that models can be easily re-evaluted. They are created by selecting the characteristics the model must exhibit to be considered acceptable. 

- **Report**: A *`MLTE`* report encapsulates all of the knowledge gained about the model and the system as a consequence of the evaluation process. The report renders as a web page and is opened automatically in an available window of the default browser. 

*`MLTE`* can be imported like any Python pacakge using the standard conventions.

```python
from mlte.property ... #importing from properties subpackage
from mlte.measurement ... #importing from measurement subpackage
from mlte.spec ... #importing from spec subpackage
from mlte.report ... #importing from report subpackage
```

### Setting up a `MLTE` session

Before most operations can be done on `MLTE`, a context and artifact store need to be set. When using `MLTE` as a library, there are two commands that can be executed once in a script to set this global state. They can be imported using

```python
from mlte.session import set_context, set_store
```

They are described and used in the following way:

- ``set_context("model_name", "model_version")``: this command indicates the model and version you will be working on for the rest of the script. It is mostly used to point to the proper location in the store when saving and loading artifacts. The model name and version can be any string.

- ``set_store("store_uri")``: this command indicates the location of the artifact store you will be using for the rest of the script. There are four store types, with the structure described in the section [Store URIs](#store-uris) below.

Alternatively, these two things can also be set by environment variables before starting your Python script. If needed, these values can later be overriden in the script usng the set methods above.

- ``MLTE_CONTEXT_MODEL`` and ``MLTE_CONTEXT_VERSION`` to set the model and version.
- ``MLTE_ARTIFACT_STORE_URI`` to set the artifact store URI.

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

## Using a Relational DB Engine Backend

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

## Next Steps

Once you're set up, we recommend referencing the [`MLTE` Process](index.md) and our how-to guide on [using `MLTE`](using_mlte.md). You can also check out our [development](development.md) guide if you're interested in contributing.