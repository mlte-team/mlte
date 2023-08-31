# Frontend

A frontend for the mlte package. Provides a visual way to explore artifacts stores and create/edit negotiation cards.

## Getting Started
To start the web frontend, run the command below. Then follow the link to view the homepage.

```bash
$ mlte ui
```

In order for the frontend to be able to communicate with the store you will need to allow the frontend as an origin.
This can be done by specifying the `--allowed-origins` flag when running the store. 
When ran through the mlte package, the frontend will be hosted at `http://localhost:8000` so the store command will look something like this:

```bash
$ mlte store --backend-uri fs://store --allowed-origins http://localhost:8000
```

## Development
Development will require Node.js. Development was done using v18.14.2, the latest LTS version can be found here: https://nodejs.org/en

To begin initialize the development environment for the frontend, navigate to `/src/mlte/frontend/nuxt-app` and run:

```bash
$ npm install
$ npx gulp compile
$ npx gulp init
```

Now the environment is setup and the frontend can be ran:

```bash
$ npm run dev
```

This will run the frontend at `http://localhost:3000` so be sure to specify that as an allowed origin when running the store:

```bash
$ mlte store --backend-uri fs://store --allowed-origins http://localhost:3000
```

When ready to publish a new version of the package, be sure to build the nuxt app:

```bash
$ npm run build
```

This will create the static app in the `.output` folder that will then be ran with the `mlte-ui` command. 

## Source Formatting and Linting

We format and lint all .vue, .js, and .ts files in this project with the [`ESLint`](https://eslint.org/). ESLint can be run locally from the root of the nuxt application.

```bash
$ npm run lint
```

## Static Type Checking
All typescript code takes advantage of static typing. This type checking can be done by running

```bash
$ npx vue-tsc
```