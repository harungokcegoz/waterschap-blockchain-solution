<!-- UpdateRequest.svelte -->
<script lang="ts">
  import { writable } from 'svelte/store';
  import type { Request } from '../../../types/types';
  import Button from '../../../components/Button.svelte';
  import { onMount } from 'svelte'
  import { pathnameStore } from '../../../stores/Store'
  import { page } from '$app/stores'

  export let data: { status: number; body: Request; requestId: string };
  let imageFile: File[];
  let previousUrl: string;
  const { body } = data;
  const userInput = writable({
    userAddress: body.user_address,
    installationType: body.installation_type,
    measures: body.measures
  });

  pathnameStore.set($page.url.pathname)
  
  onMount(() => {
    previousUrl = window.localStorage.getItem('previousUrl') || '/';
  });

  async function updateRequest() {
    const { userAddress, installationType, measures } = $userInput;
    const formData = new FormData();
    formData.append('user_address', userAddress);
    formData.append('installation_type', installationType);
    formData.append('measures', JSON.stringify(measures));

    if (imageFile && imageFile.length > 0) {
      formData.append('image', imageFile[0]);
    }
    // TODO: IPFS call to get hash and pass it to the request body
    try {
      const response = await fetch(`http://localhost:8000/api/v1/requests/${data.requestId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: formData
      });
      
      if (response.ok) {
        alert('Request updated successfully');
        window.location.reload();
      } else {
        alert('Failed to update request');
      }
    } catch (error) {
      console.error(error);
    }
  }
    
  let editing = false;
    
  function toggleEditing() {
    editing = !editing;
  }
  </script>
    
  {#if data}
    <main class="container mx-auto py-14">
      <div class="buttons flex justify-between w-full">
        <a href={previousUrl} class="text-blue-500">
          <i class="fa-solid fa-arrow-left-long mr-1"></i>
          Back
        </a>

        <div>
          <Button text={editing ? 'Cancel Editing' : 'Edit Request'} onClick={toggleEditing} backgroundColor="bg-blue-500" />
        </div>
      </div>

      <div class="flex justify-center">
        <h1 class="text-2xl font-bold my-4">Request Details</h1>
      </div>
      {#if editing && body.approval_status === 'Pending'}
        <form on:submit|preventDefault={updateRequest} class="max-w-md mx-auto">
          <div class="mb-4">
            <label for="userAddress" class="block text-sm font-medium text-gray-700">User Address:</label>
            <input type="text" id="userAddress" bind:value={$userInput.userAddress} class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm">
          </div>
      
          <div class="mb-4">
            <label for="installationType" class="block text-sm font-medium text-gray-700">Installation Type:</label>
            <input type="text" id="installationType" bind:value={$userInput.installationType} class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm">
          </div>
          
          <div class="mb-4">
            <label for="measures" class="block text-sm font-medium text-gray-700"> New measure:</label>
            <input type="text" id="measures" class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm">
          </div>

          <div class="mb-4">
            <label for="imageUpload" class="block text-sm font-medium text-gray-700">Upload Image:</label>
            <input type="file" id="imageUpload" accept="image/*" class="mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 block w-full shadow-sm">
          </div>

          <div class="mt-4">
            <button type="submit" class="w-full px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Update Request</button>
          </div>
        </form>
      {:else}
      <div class="details mt-8 flex gap-24 justify-center mx-32">
        <div class="flex mt-3 gap-2 w-1/4">
          {#each body.imageUrls as imageUrl}
            <img src={imageUrl} alt="Submitted Document"
                 class="object-cover rounded-md border-2 border-blue-300" />
          {/each}
        </div>

        <div class="flex flex-col ml-10">
          <div class="">
            <p class="p-4 border-b-2"><strong>User ID:</strong> {body.user_id}</p>
            <p class="p-4 border-b-2"><strong>Approval Status:</strong> {body.approval_status}</p>
            <p class="p-4 border-b-2"><strong>Date Requested: </strong>{new Date(body.date_requested).toLocaleString()}</p>
            <p class="p-4 border-b-2"><strong>Installation Type:</strong> {body.installation_type}</p>
          </div>

          <div>
            <p class="p-4 border-b-2"><strong>User Address:</strong> {body.user_address}</p>
            <p class="p-4 border-b-2"><strong>Request ID:</strong> {data.requestId}</p>
            <p class="p-4"><strong>Measures:</strong></p>
            {#each body.measures as measure}
              <p class="p-4 border-b-2"> - {measure.measure_type}: {measure.measure_value}</p>
            {/each}
            {#if body.approval_status === 'Approved'}
              <p class="p-4 border-b-2"><strong>Date Approved:</strong> {new Date(body.date_approved).toLocaleString()}</p>
            {/if}
            {#if body.approval_status === 'Rejected'}
              <p class="p-4 border-b-2"><strong>Date Rejected:</strong> {new Date(body.date_rejected).toLocaleString()}</p>
            {/if}
          </div>
        </div>
      </div>
      {/if}
    </main>
  {:else}
    <div>No data</div>
  {/if}
  