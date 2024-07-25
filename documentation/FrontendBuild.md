# Frontend Build Documentation
The frontend of this application was developed using `SvelteKit`, a `Server Side Rendering (SSR)` framework. While `SvelteKit` is a `JavaScript` framework, this project utilizes `TypeScript` and `TailwindCSS` for UI and styling.

## Running the Application
Typically, to run this application (as with other `Vite` applications), navigate to the directory containing the `package.json` file and execute the following command:

```bash
npm run dev
```

Alternatively, you can use the appropriate run script specified in the `package.json` file. *-if it has changed-*

## Running with Web3 Login

To enable the `web3login` feature *(the social login functionality)* on the frontend, it is needed to run the **Docker image** located in the `/client/docker` directory. This requires an additional script to run the Docker container. Running these additional scripts individually can reduce the **developer experience** significantly. To streamline this process, you can use the ``./frontendBuild.sh`` script, which installs all necessary dependencies, runs the Docker container, and then starts the frontend locally with a single command:

```bash
bash backendBuild.sh
```

Simply run this script from the directory where the ``frontendBuild.sh`` file is located to start the frontend effortlessly.

#### `Note: To run the Docker image(s), ensure that the Docker application is running. Otherwise, the containers will not be created.`