<script lang="ts">
  import { goto } from '$app/navigation';
  import { saveCurrentUrl } from '../../../utils/utils';
  import { currentAgentIdStore, pathnameStore } from '../../../stores/Store';
  import type { Request } from '../../../types/types';
  import { onMount } from 'svelte';
  import { writable, derived } from 'svelte/store';

  type RequestData = {
    status: number;
    body: Request[];
  };

  export let data: RequestData;
  $: isAgentIdPresent = !!$currentAgentIdStore;

  const routeToDetails = (requestId: string) => {
    goto(`/agent/user-requests/${requestId}`);
    saveCurrentUrl(window.location.href);
  };

  onMount(() => {
    pathnameStore.set(window.location.pathname);
  });

  const approvalStatusFilter = writable<Set<string>>(new Set());
  const sortDirection = writable<'asc' | 'desc'>('asc');
  const sortField = writable<string>('request_id');

  const filteredRequests = derived(
    [approvalStatusFilter, sortDirection, sortField],
    ([$approvalStatusFilter, $sortDirection, $sortField]) => {
      let filtered = data.body;

      if ($approvalStatusFilter.size > 0) {
        filtered = filtered.filter(request =>
          $approvalStatusFilter.has(request.approval_status.toLowerCase())
        );
      }

      filtered.sort((a, b) => {
        if (a[$sortField] < b[$sortField]) return $sortDirection === 'asc' ? -1 : 1;
        if (a[$sortField] > b[$sortField]) return $sortDirection === 'asc' ? 1 : -1;
        return 0;
      });

      return filtered;
    }
  );

  const updateSort = (field: string) => {
    if ($sortField === field) {
      sortDirection.update(current => (current === 'asc' ? 'desc' : 'asc'));
    } else {
      sortField.set(field);
      sortDirection.set('asc');
    }
  };

  const toggleApprovalStatusFilter = (status: string) => {
    approvalStatusFilter.update(filters => {
      const newFilters = new Set(filters);
      if (newFilters.has(status)) {
        newFilters.delete(status);
      } else {
        newFilters.add(status);
      }
      return newFilters;
    });
  };
</script>

{#if data.body && data.body.length > 0 && isAgentIdPresent}
  <div class="container mx-auto mt-8">
    <h1 class="text-2xl font-bold mb-4">Requests</h1>
    <div class="mb-4 flex justify-center">
      <div class="flex border rounded-md gap-10 font-bold p-6 items-center">
        <label class="block mr-10">Filter by Approval Status:</label>
        <label class="text-blue-700">
          <input class="mr-2" type="checkbox" on:change={() => toggleApprovalStatusFilter('pending')} /> Pending
        </label>
        <label class="text-green-700">
          <input class="mr-2" type="checkbox" on:change={() => toggleApprovalStatusFilter('approved')} /> Approved 
        </label>
        <label class="text-red-700">
          <input class="mr-2" type="checkbox" on:change={() => toggleApprovalStatusFilter('rejected')} /> Rejected
        </label>
      </div>
    </div>
    <table class="min-w-full bg-white border-gray-200">
      <thead>
        <tr>
          {#each ['request_id', 'user', 'user_address', 'approval_status', 'rejection_reason', 'date_requested', 'installation_type', 'agent_id'] as field}
            <th class="px-4 py-6 border-b border-black hover:cursor-pointer" on:click={() => updateSort(field)}>
              {field.split('_').map(word => word[0].toUpperCase() + word.slice(1)).join(' ')}
              {#if $sortField === field}
                {#if $sortDirection === 'asc'}
                  &uarr;
                {:else}
                  &darr;
                {/if}
              {/if}
            </th>
          {/each}
        </tr>
      </thead>
      <tbody>
        {#each $filteredRequests as request (request.request_id)}
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
{:else if !isAgentIdPresent}
  <div class="flex items-center justify-center mt-20">
    <p class="font-bold text-xl">You don't have access to reach this page</p>
  </div>
{:else}
  <div class="container mx-auto mt-8">
    <h1 class="text-2xl font-bold mb-4">No Requests Found</h1>
  </div>
{/if}
