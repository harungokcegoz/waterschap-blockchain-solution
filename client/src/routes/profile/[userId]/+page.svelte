<script lang="ts">
  import type { User } from '../../../types/types';
  import { page } from '$app/stores';
  import { bearerTokenStore, pathnameStore } from '../../../stores/Store';
  
  pathnameStore.set($page.url.pathname);
  
  export let data;

  let user: User = data.body
  let walletBalance = 0
  let activeTab: string = 'wallet'
</script>

{#if $bearerTokenStore}
  <div class="grid w-full grid-cols-5 justify-center">
    <aside class="border-r-2 h-screen">
      <nav class="space-y-2">
        <button
          class="block w-full p-5 text-left border-b-2"
          class:border-blue-400={activeTab === 'wallet'}
          on:click={() => (activeTab = 'wallet')}>
            <i class="fa-solid fa-wallet mr-1"></i>
            Wallet
          </button
        >
        <button
          class="block w-full p-4 px-5 text-left border-b-2"
          class:border-blue-400={activeTab === 'personal'}
          on:click={() => (activeTab = 'personal')}>
            <i class="fa-solid fa-circle-info mr-1"></i>
            Personal Information
          </button
        >
      </nav>
    </aside>

    <main class="col-span-4">
      {#if activeTab === 'wallet'}
        <div class="wrapper border-b-2 border-gray-200 w-full">
          <h1 class="text-xl font-semibold py-12 mt-1.5 ml-10">
            Wallet Information
          </h1>
        </div>

<!--        TODO: adjust how the balance is extracted from within the User info -->
<!--        currently showing the following error on user.blockchain info: -->
<!--        Svelte: Property blockchain_info does not exist on type User   -->
        <p class="mt-10 ml-10">Balance: {user.blockchain_info.balance.balance} {user.blockchain_info.balance.balance === 1 ? 'Water Token (WAT)' : 'Water Tokens (WAT)'}</p>
      {:else if activeTab === 'personal'}
        <div class="wrapper border-b-2 border-gray-200 w-full">
          <h1 class="text-xl font-semibold py-12 mt-1.5 ml-10">
            Personal Information
          </h1>
        </div>
  
        <div class="personal-information mt-10 ml-10">
          <div class="mb-4">
            <span class="block text-sm font-bold">First Name:</span>
            <p>{user.first_name}</p>
          </div>
          <div class="mb-4">
            <span class="block text-sm font-bold">Last Name:</span>
            <p>{user.last_name}</p>
          </div>
          <div class="mb-4">
            <span class="block text-sm font-bold">Address:</span>
            <p>{user.address}</p>
          </div>
          <div class="mb-4">
            <span class="block text-sm font-bold">Phone Number:</span>
            <p>{user.phone_number}</p>
          </div>
          <div class="mb-4">
            <span class="block text-sm font-bold">Email:</span>
            <p>{user.email}</p>
          
          </div>
          <div class="mb-4">
            <span class="block text-sm font-bold">Reward Requested:</span>
            <p>{user.reward_requested ? 'Yes' : 'No'}</p>
          </div>
        </div>
      {/if}
    </main>
  </div>
{/if}
