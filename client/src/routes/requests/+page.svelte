<script lang="ts">
    import { goto } from '$app/navigation'
    import { saveCurrentUrl } from '../../utils/utils'
    import { pathnameStore } from '../../stores/Store'
    import type { Request } from '../../types/types'
    import { onMount } from 'svelte'

    type RequestData = {
        status: number;
        body: Request[];
    }
    export let data: RequestData;

    const routeToDetails = (requestId: string) => {
      goto(`/requests/${requestId}`);
      saveCurrentUrl(window.location.href)
    }
    onMount(() => {
      pathnameStore.set(window.location.pathname)
    })

  </script>
  
  {#if data.body && data.body.length > 0}
    <div class="container mx-auto mt-8">
      <h1 class="text-2xl font-bold mb-4">Requests</h1>
      <table class="min-w-full bg-white border-gray-200">
        <thead>
          <tr>
            <th class="px-4 py-6 border-b border-black">Request ID</th>
            <th class="px-4 py-6 border-b border-black">User</th>
            <th class="px-4 py-6 border-b border-black">Address</th>
            <th class="px-4 py-6 border-b border-black">Approval Status</th>
            <th class="px-4 py-6 border-b border-black">Rejection Reason</th>
            <th class="px-4 py-6 border-b border-black">Date Requested</th>
            <th class="px-4 py-6 border-b border-black">Installation Type</th>
            <th class="px-4 py-6 border-b border-black">Agent ID</th>
          </tr>
        </thead>
        <tbody>
        {#each data.body as request (request.request_id)}
            <tr on:click={() => routeToDetails(String(request.request_id))} class="cursor-pointer hover:bg-gray-100 rounded-md">
                <td class="px-4 py-8 border-b border-gray-200 text-center">{request.request_id}</td>
                <td class="px-4 py-8 border-b border-gray-200 text-center">
                    {request.user.first_name} {request.user.last_name}
                </td>
                <td class="px-4 py-8 border-b border-gray-200 text-center">{request.user_address}</td>
                <td class="px-4 py-8 border-b border-gray-200 text-center">{request.approval_status}</td>
                <td class="px-4 py-8 border-b border-gray-200 text-center">{request.rejection_reason || 'N/A'}</td>
                <td class="px-4 py-8 border-b border-gray-200 text-center">
                    {new Date(request.date_requested).toLocaleDateString()}
                </td>
                <td class="px-4 py-8 border-b border-gray-200 text-center">{request.installation_type}</td>
                <td class="px-4 py-8 border-b border-gray-200 text-center">{request.agent_id}</td>
            </tr>
        {/each}
        </tbody>
      </table>
    </div>
  {:else}
    <div class="container mx-auto mt-8">
      <h1 class="text-2xl font-bold mb-4">No Requests Found</h1>
    </div>
  {/if}
  