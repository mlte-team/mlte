## Distribution Docker Setup

This readme briefly explains how to use this set of dockerfiles for a Docker-based deployment. It will be later integrated into the main documentation.

 - This set of Docker files are not intended to be packaged inside a MLTE distributable, but to be manually deployed on a server for deployment.
 - These Docker files assume a MLTE package is created, either locally or published yo PyPi, and build images based on this, OR the MLTE images are available in DockerHub.

 The steps to do a deployment based on these files are:

 1. Pre-requisite: have docker and docker compose installed in the deployment server.
 1. Pre-requisite: if you want to build the containers from a wheel from the current code in your local repo, run ``bash build.sh`` from the root of this repo.
 1. Copy all files in this folder to the server to be deployed, in the same folder structure: ``./docker/deployment``
 1. Create proper .env configuration files for all components in the system:
    1. Modify the ``.env.posgres`` file with appropriate values for this deployment for ``POSTGRES_USER``, ``POSTGRES_PASSWORD``, and ``POSTRGRES_DB``, as defined in the official PostgreSQL Docker Hub image.
    1. Modify the ``.env.backend`` file with the proper config for the deployed Backend:
       - ``JWT_SECRET_KEY`` should be configured to a deployment-specific secret.
       - ``STORE_URI`` should have the ``postgresql://`` prefix, and the rest should match the user, password and DB name in the ``.env.postgres`` file.
 1. Select whether to use the wheel or the published images in DockerHub.
   - If using a wheel, on the deployment server run `build_from_wheel.sh` from inside this folder. This also requires you to copy the /dist folder in this repo's root, and put it in the same relative location to this folder.
   - If using the published wheel package from PyPi, run `build_from_pypi.sh` from inside this folder.

To run the system:
 1. On the deployment server, run ``bash start.sh`` to run the system. You can "CTRL+C" and it will continue running in the background.
    - To see the logs, run ``bash logs.sh``
    - To stop it if needed, run ``bash stop.sh``
