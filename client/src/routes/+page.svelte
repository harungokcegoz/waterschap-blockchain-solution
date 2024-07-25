<script lang="ts">
  import { page } from '$app/stores'
  import {
    addBearerTokenToHeaders,
    currentAgentIdStore,
    currentUserIdStore,
    pathnameStore
  } from '../stores/Store'
  import Button from '../components/Button.svelte'
  import { goto } from '$app/navigation'
  import { onMount } from 'svelte'
  import type { User } from '../types/types'
  import AgentHomepage from './agent/homepage/+page.svelte'

  pathnameStore.set($page.url.pathname)

  let user: User

  $: isUserIdPresent = !!$currentUserIdStore;
  $: isAgentIdPresent = !!$currentAgentIdStore;

  onMount(async () => {
    try {
      const headers = addBearerTokenToHeaders({
        'Content-Type': 'application/json'
      })

      const response = await fetch(`http://localhost:8000/api/v1/users/${$currentUserIdStore}`,
        { headers })

      if (!response.ok) {
        throw new Error('Failed to fetch user information')
      }
      
      user = await response.json()
    } catch (error) {
      console.error('Error fetching user information:', error)
    }
  })

  async function goToClaimPage() {
    await goto('/claim')
  }

</script>

<main class="w-full">
  {#if !isAgentIdPresent}
    <div class="flex flex-col justify-center items-center header bg-blue-900 text-white py-5">
      <h1 class="mb-4">Welcome to Project Water for Aa &amp; Maas Waterschap</h1>
      {#if user?.first_name}
        <p>Welcome back, <b>{user.first_name} {user.last_name}</b></p>
        <p class="mt-15 ml-10">
          Your current balance is: {user.blockchain_info.balance.balance}
          {user.blockchain_info.balance.balance === 1 ? 'Water Token (WAT)' : 'Water Tokens (WAT)'}
        </p>
      {/if}
    </div>

    <!-- Explanation of the problem and its importance -->
    <div class="bg-gray-100 rounded-lg">
      <section class="mx-auto max-w-2xl px-6 py-8">
        <h2 class="text-2xl font-semibold mb-4">Problem Statement</h2>
        <p class="text-gray-900 leading-relaxed">
          The Netherlands is facing serious challenges with groundwater levels dropping due to long dry periods and
          increased water use. This leads to water shortages during dry spells and compacted soil that can't support
          vegetation. Additionally, heavy rains cause flooding, and rainwater is then lost to treatment plants instead of
          having the chance to refill the groundwater.
        </p>
        <p class="text-gray-900 leading-relaxed mt-4">
          To tackle this, we need to improve water retention and boost groundwater levels. A key strategy is to retain
          rainwater in urban areas so it can soak into the soil. This helps reduce pressure on sewers and replenish
          groundwater, building long-term resilience. We're taking an innovative approach by using blockchain technology to
          incentivize homeowners to participate in rainwater-saving initiatives. Our plan outlines strategic actions to
          ensure a sustainable and water-secure future for the Netherlands.
        </p>
      </section>
    </div>

    <!-- Explanation of how to claim a reward -->
    <div class="bg-gray- rounded-lg">
      <section class="mx-auto max-w-2xl px-6 py-8">
        <h2 class="text-2xl font-semibold mb-4">Claim your reward</h2>
        <p class="text-gray-900 leading-relaxed">
          To claim your reward, start by heading to the "Claim" page to start filling in your first claim request today.
          The first available measures are rain barrels and green rooftops. Simply fill in the claim form with the
          required information, including uploading a picture of your measure for verification.
        </p>
        <p class="text-gray-900 leading-relaxed mt-4">
          Once you've submitted your new claim request, a waterschap agent will review your submission, and if all
          information is correct and complete, the agent will approve your request. If approved, your account balance
          will increase based on the measures you included in the claim. To view your token balance, you can find it either
          at the top of the homepage or on your profile page in the "Wallet" section. By following these steps, you can
          easily claim your reward and see your watertoken balance increase once your submission is approved.
        </p>

        {#if isUserIdPresent}
          <div class="flex justify-center mt-8">
            <Button
              text="Go to Claim Page & Make A New Claim Today"
              backgroundColor="bg-blue-500"
              icon="arrow-right"
              onClick={goToClaimPage}
            />
          </div>
        {/if}
      </section>
    </div>

    <div class="footer bg-blue-900 text-white py-5 text-center">
      <p>&copy; 2024 Aa &amp; Maas Waterschap. All rights reserved.</p>
    </div>
  {:else}
    <AgentHomepage />
  {/if}

</main>

