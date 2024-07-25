<script lang="ts">
	import Button from '../../components/Button.svelte';
	import { authPopupStore, userEmailStore } from '../../stores/Store';
	import { goto } from '$app/navigation';

	let email = '';
	let firstName = '';
	let lastName = '';
	let address = '';
	let phoneNumber = '';
	const rewardRequested = false;
	let showAdditionalFields = false;

	$: email = $userEmailStore;

	async function registerUser() {

	  const userData = {
	    first_name: firstName,
	    last_name: lastName,
	    address,
	    phone_number: phoneNumber,
	    email,
	    reward_requested: rewardRequested.toString(),
			wallet_address: ''
	  };

	  const response = await fetch('http://localhost:8000/api/v1/users/', {
	    method: 'POST',
	    headers: {
	      'Content-Type': 'application/json'
	    },
	    body: JSON.stringify(userData)
	  });

	  if (response.ok) {
	    alert('User registration successful');
			authPopupStore.set('web3login')
			await goto('/web3login');
	  } else {
	    const errorData = await response.json();
	    console.error('Registration failed:', errorData);
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
		<h1 class="text-xl font-semibold mb-12 py-4 border-b-2 border-gray-200">User Registration</h1>
		<form class="max-w-lg">
			<div class="mb-4">
				<label class="block text-gray-700 text-sm font-bold mb-2" for="email">Email:</label>
				<input
					class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-normal focus:outline-2 focus:shadow-outline"
					type="email" id="email" bind:value="{email}" required />
			</div>
			{#if !showAdditionalFields}
				<div class="text-right flex gap-3 items-center justify-between mt-10">
					<div>
						<span class="text-xs">Do you already have an account? Then you can login from
							<a href="/web3login" class="underline text-blue-500">here.</a>
						</span>
					</div>
					<div class="right">
						<Button
						text="Next"
						backgroundColor="bg-blue-500"
						onClick={() => {showAdditionalFields = true}}
						disabled={!email}
						icon="arrow-right"
					/>
					</div>
				</div>

			{:else}
				<!-- Additional fields -->
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="firstName">First Name:</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-normal focus:outline-2 focus:shadow-outline"
						type="text" id="firstName" bind:value="{firstName}" required />
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="lastName">Last Name:</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-normal focus:outline-2 focus:shadow-outline"
						type="text" id="lastName" bind:value="{lastName}" required />
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="address">Address:</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-normal focus:outline-2 focus:shadow-outline"
						type="text" id="address" bind:value="{address}" required />
				</div>
				<div class="mb-4">
					<label class="block text-gray-700 text-sm font-bold mb-2" for="phoneNumber">Phone Number:</label>
					<input
						class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-normal focus:outline-2 focus:shadow-outline"
						type="tel" id="phoneNumber" bind:value="{phoneNumber}" required />
				</div>
				<div class="text-right float-right mt-10">
					<Button
						text="Register"
						type="submit"
						backgroundColor="bg-blue-500"
						disabled={!email || !firstName || !lastName || !address || !phoneNumber}
						icon="arrow-right"
						onClick={registerUser}
					/>
				</div>
			{/if}
		</form>
	</main>
</div>
