<script lang="ts">
  import Button from './Button.svelte'
  import SecondaryNav from './SecondaryNav.svelte'
  import { bearerTokenStore, currentUserIdStore, pathnameStore, removeTokenAndId } from '../stores/Store'
  import { goto } from '$app/navigation'
  import { page } from '$app/stores'

  function logout() {
    removeTokenAndId();
    goto('/')
    pathnameStore.set($page.url.pathname)
  }
</script>

<header class="">
  <div class="wrapper flex justify-between px-20 bg-sky-400 border-b-2 border-gray-100 gap-10 items-center h-24">
    <div class="logo">
      <a href="/">
        <img src="/logo.png" alt="" class="w-34 h-16" />
      </a>
    </div>
    {#if $bearerTokenStore}
      <div class="flex items-center gap-20">
        <div class="p-2 border-b-2 border-red-600 text-blue-900">
          {#if $currentUserIdStore}
            <span>Household Account</span>
          {:else}
            <span>Agent Account</span>
          {/if}
        </div>
        <Button text="Sign Out" backgroundColor="bg-blue-700" icon="signout" onClick={logout} />
      </div>
    {/if}
    {#if !$currentUserIdStore && !$bearerTokenStore}
      <div class="flex gap-5">
        <Button text="User Login" backgroundColor="bg-blue-600" onClick={() => goto('/web3login')} />
        <Button text="Registration" backgroundColor="bg-blue-700" onClick={() => goto('/registration')} />
      </div>
    {/if}
  </div>
  <SecondaryNav />
</header>

