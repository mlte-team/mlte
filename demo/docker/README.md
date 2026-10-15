This folder contains files to create and run a self-contained pair of docker images that contain the frontend and the backend, with the backend one containing the full stores for all existing demos. This makes it easy to use these two containers to review the results of the demo without setting up a local environment.

There are two ways to build the images:

1. Locally
  - Set up a local MLTE environment (see general readme)
  - Build the images with `bash build.sh`
  - Be sure to run the commands in the section below from inside this folder
2. From Github
  - Pre-requisite: the repository has an action to manually create and push the images to the Github Registry. The assumption is that this has already been done.
  - Copy the `docker-compose.yaml` to another folder (or simply download it from the repo without cloning), and then be sure to run commands below from the folder where that file is.

In either case, to run the containers and see the demo data:

1. Run the containers with `docker compose up`
2. Explore the stores with a browser pointing to `http://localhost:8000`, with the default user and password (see general readme)
3. Use Ctrl+C and `docker compose down` to fully stop and remove the containers when done
