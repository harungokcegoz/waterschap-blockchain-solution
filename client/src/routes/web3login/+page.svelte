<script lang="ts">
  import { onMount } from 'svelte'
  import { ethers } from '@vechain/ethers'
  import {
    bearerTokenStore,
    authPopupStore,
    currentUserIdStore,
    userEmailStore,
    addBearerTokenToHeaders
  } from '../../stores/Store'
  import { goto } from '$app/navigation'

  // IMP START - SDK Initialisation
  // IMP START - Dashboard Registration
  // App registered at https://web3auth.io/dashboard
  const clientId = import.meta.env.VITE_APP_CLIENT_ID

  let provider = null;
  let loggedIn = false;
  let web3auth;
  let privateKeyProvider;

  onMount(async () => {
    try {
      const moduleConnex = await import('@vechain/connex')
      const connex = new moduleConnex.Connex({
        node: import.meta.env.VITE_APP_VECHAIN_NODE,
        network: import.meta.env.VITE_APP_NET
      })

      const Web3AuthBase = await import('@web3auth/base')
      const { CHAIN_NAMESPACES, WEB3AUTH_NETWORK } = Web3AuthBase

      const chainConfig = {
        chainId: connex.thor.genesis.id,
        rpcTarget: 'http://127.0.0.1:8545',
        chainNamespace: CHAIN_NAMESPACES.EIP155,
        displayName: 'Vechain',
        blockExplorerUrl: 'https://explore-testnet.vechain.org/',
        ticker: 'VET',
        tickerName: 'VeChain'
      }

      const ethereumPrivateKeyProviderPkg = await import('@web3auth/ethereum-provider')
      const { EthereumPrivateKeyProvider } = ethereumPrivateKeyProviderPkg

      privateKeyProvider = new EthereumPrivateKeyProvider({
        config: { chainConfig }
      })

      const Web3AuthPkg = await import('@web3auth/modal')

      web3auth = new Web3AuthPkg.Web3Auth({
        clientId,
        web3AuthNetwork: WEB3AUTH_NETWORK.SAPPHIRE_DEVNET,
        privateKeyProvider
      })

      // IMP END - SDK Initialisation

      await web3auth.initModal()
      provider = web3auth.provider

      if (web3auth.connected) {
        loggedIn = true
        console.log('web3auth connected: ', web3auth.connected)
      }

    } catch (error) {
      console.error('Error during initialisation:', error)
    }

    await login();
  })

  async function login() {
    try {
      const web3authProvider = await web3auth.connect();
      provider = web3authProvider;
      if (web3auth.connected) {
        loggedIn = true;
      }
      let userInfo = await web3auth.getUserInfo();
      let userIdToken = userInfo.idToken;
      let userEmail = userInfo.email;
      let userId;

      console.log(userInfo)

      const emailRequest = {
        email: userEmail
      }

      // TODO find a better approach for this endpoint that doesn't compromise security
      const response = await fetch(`http://localhost:8000/api/v1/users/get-by-email`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(emailRequest)
      });

      const userData = await response.json();

      if (userData.found === false) {
        console.log('User not found in database, redirecting to registration');
        userEmailStore.set(userEmail);
        authPopupStore.set('register');
        await goto('/registration')
      } else {
        userId = userData.user_id;

        const TokenData = {
          user_id: userId
        }

        const response = await fetch('http://localhost:8000/api/v1/web3login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(TokenData)
        });

        const web3token = await response.json()

        bearerTokenStore.set(web3token.access_token);
        currentUserIdStore.set(userData.user_id);

        const walletAddress = await getAccounts();
        if (!userData.wallet_address && walletAddress) {
          await updateWalletAddress(userId, walletAddress);
        }
        await goto('/');
      }
    } catch (error) {
      console.error('Error handling login', error)
    }
  }

  async function updateWalletAddress(userId: String, walletAddress: String) {
    const userWalletUpdate = {
      wallet_address: walletAddress
    }

    try {
      const headers = addBearerTokenToHeaders({
        'Content-Type': 'application/json'
      })

      const response = await fetch(`http://localhost:8000/api/v1/users/${userId}/wallet`, {
        method: 'PATCH',
        headers: headers,
        body: JSON.stringify(userWalletUpdate),
      });

      if (response.ok) {
        console.log('Wallet address updated successfully');
      } else {
        console.error('Failed to update wallet address');
      }
    } catch (error) {
      console.error('Error updating wallet address:', error);
    }
  }

  // likely won't need this separate function, as the user info can be retrieved directly from web3auth
  async function getUserInfo() {
    const user = await web3auth.getUserInfo();
    console.log(user)
  }

  // TODO look into how logout can be used on the sign out button
  async function logout() {
    await web3auth.logout();
    provider = null;
    loggedIn = false;
    console.log('logged out');
  }

  // likely won't need this function any
  async function getAccounts() {
    if (!provider) {
      console.log('provider not initialized yet');
      return;
    }
    /** @type {string[]} */
    const [address] = (await web3auth.provider.sendAsync({
      method: 'eth_accounts',
    }));
    console.log(address);
    return address;
  }

  // likely won't need this function as we use vorj to get the balance
  async function getBalance() {
    if (!provider) {
      console.log('provider not initialized yet');
      return;
    }

    /** @type {string[]} */
    const [address] = (await web3auth.provider.sendAsync({
      method: 'eth_accounts',
    }));

    /** @type {import('@vechain/ethers')} */
    const balance = (await web3auth.provider.sendAsync({
      method: 'eth_getBalance',
      params: [address, 'latest'],
    }));

    console.log(ethers.utils.formatEther(balance));
  }

</script>
