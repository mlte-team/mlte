# Server Deployment Docker Setup

This readme briefly explains how to use this set of dockerfiles for a Docker-based server deployment. It will be later integrated into the main documentation. This set of Docker files are not intended to be packaged inside a MLTE distributable, but to be manually deployed on a server for deployment.

## Pre-requisites

 1. Have docker installed in the deployment server.

## Configuration
Before building the images, the proper configuration needs to be set up. For build option 3, this needs to be done before building the docker images.

 1. Create a copy of this repo in the deployment server.
 1. Modify the .env configuration files for all components in the system:
    1. Modify the `.env.postgres` file with appropriate values for this deployment for `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTRGRES_DB`, as defined in the official PostgreSQL Docker Hub image.
    1. Modify the `.env.backend` file with the proper config for the deployed Backend:
       - `JWT_SECRET_KEY` should be configured to a deployment-specific secret.
       - `STORE_URI` should have the `postgresql://` prefix, and the rest should match the user, password and DB name in the `.env.postgres` file.
    1. Modify the `.env.frontend` file with the proper config for the deployed Frontend:
       - `NUXT_PUBLIC_API_PATH` should point to the external IP of where the Backend is deployed, if this is not only used for a local deployment. Note also that the port should match the port defined in `BACKEND_PORT` in the `.env.backend` file (which it does by default). This is currently only needed for build option 2.

## Building docker images

### Build Option 1: PyPi Package
One option is to build docker images based on a published version of MLTE from PyPi. To do so:
 1. Run `build_from_pypi.sh` from inside this folder.

NOTE: this option will not currently work with external server deployments, only for local access.

### Build Option 2: Repo Code
Another option is to build the docker images from the code in the repo directly.
 1. Run `bash build.sh` from the `/docker` folder.

## Running the docker images
To run the system, from inside the `/docker/deployment` folder:
 1. Run `bash start.sh` . You can "CTRL+C" and it will continue running in the background.
    - To see the logs, run `bash logs.sh`
    - To stop it if needed, run `bash stop.sh`

To rebuild and restart the system, from inside the `/docker/deployment` folder:
 1. Run `bash rebuild_and_restart.sh`