<script lang="ts">
  import Button from '../../components/Button.svelte'
  import { authPopupStore, bearerTokenStore, currentAgentIdStore } from '../../stores/Store'
  import { goto } from '$app/navigation'

  let email = 'Aa&Maas@waterschap.com'
  let password = 'password'

  async function handleLogin() {
    const userData = {
      email,
      password
    }

    const response = await fetch('http://localhost:8000/api/v1/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    })

    if (response.ok) {
      const responseData = await response.json();
      bearerTokenStore.set(responseData.access_token);
      currentAgentIdStore.set(responseData.agent_id);
      await goto('/')
      alert(`User login successful`);
    } else {
      const errorData = await response.json();
      console.error('Login failed:', errorData);
    }
  }

</script>

<div class="flex gap-10 justify-center mt-32">
  <main class="w-1/3 px-20 py-16 ring-1 rounded-lg ring-gray-200 drop-shadow-sm">
    <button class="text-blue-400 text-sm"
            on:click={() => {
				authPopupStore.set('');
				window.location.href = '/';
			}}>
      <i class="fa-solid fa-arrow-left mr-1"></i>
      Back
    </button>
    <h1 class="text-xl font-semibold mb-12 py-4 border-b-2 border-gray-200">Agent Dashboard Login</h1>
    <form class="max-w-lg">
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="email">Email:</label>
        <input
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-normal focus:outline-2 focus:shadow-outline"
          type="email" id="email" bind:value="{email}" required />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 text-sm font-bold mb-2" for="password">Password:</label>
        <input
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-normal focus:outline-2 focus:shadow-outline"
          type="password" id="password" bind:value="{password}" required />
      </div>
      <div class="text-right flex gap-3 items-center justify-end mt-10">
        <div class="right">
          <Button
            text="Login"
            backgroundColor="bg-blue-500"
            disabled={!email || !password}
            icon="arrow-right"
            onClick={handleLogin}
          />
        </div>
      </div>
    </form>
  </main>
</div>