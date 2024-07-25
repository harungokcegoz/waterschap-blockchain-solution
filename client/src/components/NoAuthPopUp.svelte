<script>
  import { onMount } from 'svelte'
  import Button from './Button.svelte';
  import Register from '../routes/registration/+page.svelte';
  import Login from '../routes/login/+page.svelte';
  import Web3Login from '../routes/web3login/+page.svelte';
  import { authPopupStore } from '../stores/Store';
  
  onMount(() => {
    window.localStorage.setItem('showModal', '');
  })

</script>

{#if $authPopupStore==='web3login'}
  <Web3Login />
{:else} 
  <div class="flex flex-col justify-center items-center h-screen">
    <p class="text-xl mb-10">
      You need to login to reach all content. If you are not a member please register first.
    </p>
    <div class="buttons flex gap-2">
      <Button text="Web3Login" onClick={() => {authPopupStore.set('web3login')}} backgroundColor="bg-sky-600"/>
      <Button text="Login" onClick={() => {window.location.href = '/login'}} backgroundColor="bg-sky-600"/>
      <Button text="Register" onClick={() => {window.location.href = '/registration'}} backgroundColor="bg-sky-600"/>
    </div>
  </div>
{/if}