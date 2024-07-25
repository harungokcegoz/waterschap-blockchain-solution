<script lang="ts">
    import { 
      bearerTokenStore, 
      pathnameStore, 
      currentUserIdStore, 
      currentAgentIdStore 
    } from '../stores/Store';

    const aClass = 
    'text-sky-900 border-b-4 py-4 border-transparent hover:text-blue-700 hover:border-blue-700';
    const activeClass = 'border-b-4 py-4 text-blue-700 border-blue-700';
</script>

{#if $bearerTokenStore}
    <div class="navbar text-blue-400 border-b-2 drop-shadow-sm text-sm">
        <nav class="flex justify-center gap-20 flex-grow">
            {#if $currentUserIdStore}
                <a href="/"
                   class={`${$pathnameStore === '/' ? activeClass : aClass}`}
                   data-sveltekit-preload-data
                >
                    <i class="fa-solid fa-house mr-1"></i>
                    Homepage
                </a>
                <a href="/claim" class={`${$pathnameStore === '/claim' ? activeClass : aClass}`} data-sveltekit-preload-data>
                    <i class="fa-solid fa-paper-plane mr-1"></i>
                    Claim
                </a>
                <a href={`/profile/${$currentUserIdStore}`}
                   class="{`${$pathnameStore.includes('/profile') ? activeClass : aClass} ${currentUserIdStore} ? 'disabled' : ''}`}" data-sveltekit-preload-data>
                    <i class="fa-solid fa-circle-user mr-1"></i>
                    Profile
                </a>
                <a href={`/requests/?userId=${$currentUserIdStore}`}
                    class="{`${$pathnameStore.includes('/requests') ? activeClass : aClass} ${$currentUserIdStore ? 'disabled' : ''}`}" 
                    data-sveltekit-preload-data
                >
                    <i class="fa-solid fa-bell mr-1"></i>
                    Requests
                </a>
            {/if}
            {#if $currentAgentIdStore}
                <a href="/"
                   class={`${$pathnameStore === '/' ? activeClass : aClass}`}
                   data-sveltekit-preload-data
                >
                    <i class="fa-solid fa-house mr-1"></i>
                    Homepage
                </a>
                <a href={`/agent/user-requests?agentId=${$currentAgentIdStore}`}
                    class="{`${$pathnameStore.includes('/agent/user-requests') ? activeClass : aClass} ${$currentUserIdStore ? 'disabled' : ''}`}" 
                    data-sveltekit-preload-data
                >
                    <i class="fa-solid fa-user-tie mr-1"></i>
                    User Requests
                </a>
            {/if}
        </nav>
    </div>
{/if}
