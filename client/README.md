## Setting up the project

  

Run the initial installation of dependencies using Node Package Manager, or another package manager of your choice

  

```bash

# If using Node Package Manager

npm install
  

# If using other package managers

pnpm install

# or

yarn install

```

  

## Developing

  

Once you've installed dependencies using your package manager, start a development server:

  

```bash

# start the server only
npm run dev


# or start the server and open the app in a new browser tab

npm run dev -- --open

```

  

## Building

  

To create a production version of your app:

  

```bash

npm run build

```

  

You can preview the production build with `npm run preview`.

  

> To deploy your app, you may need to install an [adapter](https://kit.svelte.dev/docs/adapters) for your target environment.

  
  

***

  

## Web3Auth (`@web3auth/modal`) x vechain Login Adapter

  

<p  align="center">

<a  href="https://web3auth.io/docs/sdk/pnp/web/modal">

<img alt="Web3Auth SDK" src="https://img.shields.io/badge/Web3Auth-SDK-blue">

</a>

<a  href="https://community.web3auth.io">

<img alt="Web3Auth Community" src="https://img.shields.io/badge/Web3Auth-Community-cyan">

</a>

</p>

  

[//]: # (<h1  align="center">)

  

[//]: # ( Web3Auth &#40;`@web3auth/modal`&#41; x vechain Example)

  

[//]: # (</h1>)

  

<p  align="center">

Here are instructions on how to create an account using Web3Auth with Vechain in our svelte application

using an RPC-Proxy Server.

</p>

  

## 🚀 How to Use

  

To get started, follow these steps:

  

1. **Configure Web3Auth Client:**

<br>Go to https://dashboard.web3auth.io/ and create a new project.

2. **Add .env file:**

Create `.env` file and add in your client ID generated in step 1.

3. **Install dependencies:**

```bash

cd blockchain-water-vechain/client

npm install

```

4.  **Run RPC-Proxy:**

-  For the Testnet environment, use the following command:

```bassh

npm run docker:start:testnet

```

- For the Mainnet environment, use the following command:

```bash

npm run docker:start:mainnet

```

5. **Start the App and open the browser window automatically**

```bash

npm run dev --open

```
