<script lang="ts">
  import { writable } from 'svelte/store';
  import Button from './Button.svelte';
  import Cookies from 'js-cookie';
  import { onMount } from 'svelte'
  import { page } from '$app/stores';  
  
  const steps = [
    `<section class="mx-auto max-w-2xl px-6 py-8">
      <h1 class='text-2xl font-semibold mb-4'> Welcome to Aa & Maas Waterschap.<h1> 
      <p class='text-gray-900 leading-relaxed'> 
      This is a simple onboarding popup to help you get started with the application. You can close this popup at any time by clicking the 'X' button in the top right corner. 
      <p> 
      <p class='text-gray-900 leading-relaxed'> 
      If you are already onboarded and have seen this popup before, this popup won't show up again. To get more information, you can click next to see further steps.
      <p>
    </section>`,
    `<section class="mx-auto max-w-2xl px-6 py-8">
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
    </section>`,
    `<section class="mx-auto max-w-2xl px-6 py-8">
      <h1 class='text-2xl font-semibold mb-4'>Login & Registration<h1> 
      <p class='text-gray-900 leading-relaxed'> 
        To be able to benefit from the services provided by Project Water, you need to be registered and logged in. If you are not registered yet, you can click on the register button to create an account. If you are already registered, you can click on the login button to log in to your account.
      <p> 
      <p class='text-gray-900 leading-relaxed'> 
        Once you are logged in, you can access the services provided by Project Water, such as claiming rewards, viewing your balance, and participating in rainwater-saving initiatives. 
      <p>
      <div class="flex justify-center mt-8 gap-4">
        <a href="/web3login" class="border py-3 px-6 text-white border-white rounded-lg bg-blue-500 hover:bg-sky-700">Go to Login Page</a>
        <a href="/registration" class="border py-3 px-6 text-white border-white rounded-lg bg-blue-500 hover:bg-sky-700">Go to Registration Page</a>
      </div>
    </section>`,
    `<section class="mx-auto max-w-2xl px-6 py-8">
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

      <div class="flex justify-center mt-8">
        <a href="/claim" class="border py-3 px-6 text-white border-white rounded-lg bg-blue-500 hover:bg-sky-700">Go to Claim Page & Make A New Claim Today</a>
      </div>
    </section>`,
  ];

  const currentStep = writable(0);
  const showPopup = writable(false);


  if (!(Cookies.get('isOnboarded') === 'true')) {
    onMount(() => {
      showPopup.set(true);
    });
  }

  function nextStep() {
    currentStep.update(n => n + 1);
  }

  function previousStep() {
    currentStep.update(n => n - 1);
  }

  function closePopup() {
    showPopup.set(false);
    Cookies.set('isOnboarded', 'true', 365); 
  }
</script>

{#if $showPopup && $page.url.pathname !== '/login' && $page.url.pathname !== '/registration' && $page.url.pathname !== '/claim' && $page.url.pathname !== '/web3login'}
  <div class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
    <div class="flex flex-col bg-white p-10 rounded-lg shadow-lg w-1/3 h-[850px] justify-between">
      <div class="wrapper">
        <div class="xmark float-end hover:cursor-pointer" on:click={closePopup}>
          <i class="fa-solid fa-xmark"></i>
        </div>
        
        <div class="flex justify-center space-x-2 mb-8">
          {#each steps as _, index}
            <div class="w-8 h-8 flex items-center justify-center rounded-full text-white {index === $currentStep ? 'bg-blue-600' : 'bg-gray-400'}">
              {index + 1}
            </div>
          {/each}
        </div>
      </div>

      <div class="wrapper">
        <div class="text-lg">
          {@html steps[$currentStep]}
        </div>
      
        <div class="mt-10 flex justify-between">
          <Button text="Previous" onClick={previousStep} disabled={$currentStep === 0} backgroundColor="bg-gray-500" icon='arrow-left'/>
          {#if $currentStep < steps.length - 1}
            <Button text="Next" onClick={nextStep} icon="arrow-right" />
          {:else}
            <Button text="Finish" onClick={closePopup} icon="arrow-left" />
          {/if}
        </div>
      </div>
    </div>
  </div>
{/if}
