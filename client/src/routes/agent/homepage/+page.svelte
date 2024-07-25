<script lang="ts">
    import { page } from '$app/stores';
    import { pathnameStore, currentAgentIdStore } from '../../../stores/Store';
    import Button from '../../../components/Button.svelte';
    import { goto } from '$app/navigation';
  
    pathnameStore.set($page.url.pathname);
  
    async function goToUserRequestsPage() {
      await goto(`/agent/user-requests?agentId=${$currentAgentIdStore}`);
    }
  </script>
  
  <main class="w-full">
    <div class="flex flex-col justify-center items-center header bg-blue-900 text-white py-5">
      <h1>Welcome to the Agent Portal</h1>
    </div>

    <div class="bg-gray-100 rounded-lg">
      <section class="mx-auto max-w-2xl px-6 py-8">
        <h2 class="text-xl font-semibold mb-4">Your Mission</h2>
        <p class="text-gray-900 leading-relaxed">
          As an agent, you play a crucial role in verifying the validity of user-submitted data
          and rewarding their water-saving efforts with WAT tokens. Your diligence ensures
          the integrity of the program and incentivizes continued participation.
        </p>

        <div class="max-w-screen-lg mx-auto">
          <div class="bg-gray-100 shadow-md rounded-2xl py-8 px-6 my-8 text-center">
            <h2 class="text-xl font-semibold text-blue-800 mb-4">Your Role in Water Conservation</h2>
            <div class="storyline-bar flex items-center justify-between">
              <div class="step">
                <i class="fas fa-check-circle text-green-500 text-2xl"></i>
                <p>Review Requests</p>
              </div>
              <div class="connector"></div>
              <div class="step">
                <i class="fas fa-tasks text-blue-500 text-2xl"></i>
                <p>Verify Request Data</p>
              </div>
              <div class="connector"></div>
              <div class="step">
                <i class="fas fa-award text-yellow-500 text-2xl"></i>
                <p class="text-center">Reward Users <br> with WAT Tokens</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <div class="bg-gray-200 rounded-lg">
      <section class="mx-auto max-w-2xl px-6 py-8">
        <h2 class="text-xl font-semibold mb-4">Review Process</h2>
        <p class="text-gray-900 leading-relaxed">
          Carefully assess each request, examining submitted data and evidence. Approve valid
          requests and reward users with WAT tokens. For invalid or incomplete requests,
          provide clear feedback and guidance.
        </p>

        <div class="flex flex-col justify-center items-center container max-w-screen-lg mx-auto px-4 pb-8">
          <h2 class="text-center mt-8">Manage Water Conservation Efforts</h2>
          <p class="text-center mb-8">Efficiently review and reward user contributions to water conservation.</p>
          <Button
            text="Review Requests"
            backgroundColor="bg-blue-500"
            icon="arrow-right"
            onClick={goToUserRequestsPage}
          />
        </div>
      </section>
    </div>

    <div class="footer bg-blue-900 text-white py-5 text-center">
      <p>&copy; 2024 Aa &amp; Maas Waterschap. All rights reserved.</p>
    </div>
  </main>

  <style>
    .storyline-bar {
      gap: 2rem; /* Adjust spacing between steps */
    }
    .step {
      @apply flex flex-col items-center;
    }
    .connector {
      flex-grow: 1;
      height: 2px;
      background-color: lightgray;
    }
  </style>
  