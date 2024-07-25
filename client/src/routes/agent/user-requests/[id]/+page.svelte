<script lang="ts">
  import type { Request } from '../../../../types/types'
  import { onMount } from 'svelte'
  import Button from '../../../../components/Button.svelte'
  import { addBearerTokenToHeaders, currentAgentIdStore, pathnameStore } from '../../../../stores/Store'
  import { goto } from '$app/navigation'
  import { getImageUrlFromCID } from '../../../../utils/utils'

  export let data: { status: number; body: Request; requestId: number }
  import GoogleMapVisual from '../../../../components/GoogleMapVisual.svelte'
  import Header from '../../../../components/Header.svelte'
  import { page } from '$app/stores'

  pathnameStore.set($page.url.pathname)

  let client = data.body
  let showApprovePopup = false
  let showRejectPopup = false
  let declineReason = ''
  let previousUrl: string
  let isAgentIdPresent = false

  $: isAgentIdPresent = !!$currentAgentIdStore

  onMount(() => {
    previousUrl = window.localStorage.getItem('previousUrl') || '/'
  })


  function openApprovePopup() {
    showApprovePopup = true
  }

  function openDeclinePopup() {
    showRejectPopup = true
  }

  function closeDeclinePopup() {
    showRejectPopup = false
  }

  function closeApprovePopup() {
    showApprovePopup = false
  }

  async function updateApprovalStatus(newStatus: string, declineReason?: string) {
    const approvalUpdate = {
      approval_status: newStatus,
      rejection_reason: declineReason,
      date_approved: newStatus === 'Approved' ? new Date().toISOString() : 'null',
      date_rejected: newStatus === 'Rejected' ? new Date().toISOString() : 'null'
    }

    try {
      const headers = addBearerTokenToHeaders({
        'Content-Type': 'application/json'
      })

      const response = await fetch(`http://localhost:8000/api/v1/requests/${client.request_id}`, {
        method: 'PATCH',
        headers: headers,
        body: JSON.stringify(approvalUpdate)
      })

      if (!response.ok) {
        throw new Error('Failed to update the approval status')
      }

      if (newStatus === 'Approved' || newStatus === 'Rejected') {
        await goto(previousUrl)
      } else {
        closeApprovePopup()
        closeDeclinePopup()
      }

      if (newStatus === 'Approved') {
        client.date_approved = approvalUpdate.date_approved
      } else if (newStatus === 'Rejected') {
        client.date_rejected = approvalUpdate.date_rejected
        approvalUpdate.rejection_reason = declineReason
      }

    } catch (error) {
      console.error('Error updating approval status:', error)
    } finally {
      closeApprovePopup()
      closeDeclinePopup()
    }
  }
</script>

{#if isAgentIdPresent}
  <main class="container mx-auto py-14">
    <a href={previousUrl} class="text-blue-500">
      <i class="fa-solid fa-arrow-left-long mr-1"></i>
      Back
    </a>
    <div class="max-w-6xl border mx-auto p-12 bg-white rounded-lg shadow-md mt-10">

      {#if client}
        <h2 class="text-2xl font-semibold text-blue-800 mb-4">Request Details</h2>
        <div class="grid grid-cols-2 gap-4 text-gray-700 gap-24">
          <div class="col-span-1">
            <label class="font-bold text-lg">Name:</label>
            <p>{client.user.first_name} {client.user.last_name}</p>
          </div>

          <div class="col-span-1">
            <label class="font-bold text-lg">Date Requested:</label>
            <p>{new Date(client.date_requested).toLocaleString()}</p>
          </div>

          <div class="col-span-1">
            <label class="font-bold text-lg">Installation Type & Value:</label>
            {#each client.measures as measure}
              <li class="ml-2 font-light"> {measure.measure_type}: {measure.measure_value}</li>
            {/each}
          </div>

          <div class="col-span-1">
            <label class="font-bold text-lg">Approval Status:</label>
            <p class="text-sm bg-blue-100 text-blue-800 px-3 py-1 ml-3 inline-flex rounded-full">
              {client.approval_status}
            </p>
            {#if client.approval_status === 'Approved'}
              <div class="mt-2">
                <label class="font-bold text-lg">Approval Date:</label>
                <p class="text-sm bg-blue-100 text-blue-800 px-3 py-1 ml-3 inline-flex rounded-full">
                  {new Date(client.date_approved).toLocaleString()}
                </p>
              </div>
            {/if}
            {#if client.approval_status === 'Rejected'}
              <div class="mt-2">
                <label class="font-bold text-lg">Rejection Reason:</label>
                <p class="text-red-500 bg-gray-100 px-3 py-1 rounded">{client.rejection_reason}</p>
              </div>
              <div class="mt-2">
                <label class="font-bold text-lg">Rejection Date:</label>
                <p class="text-sm bg-red-100 text-red-800 px-3 py-1 ml-3 inline-flex rounded-full">
                  {new Date(client.date_rejected).toLocaleString()}
                </p>
              </div>
            {/if}
          </div>
        </div>
        <div class="mt-6">
          <h3 class="text-lg font-semibold text-blue-800 text-lg mt-12">Images:</h3>
          <div class="flex space-x-2 mt-3">
            {#each client.imageUrls as imageUrl}
              <img src={imageUrl} alt="Submitted Document"
                   class="w-1/3 object-cover rounded-md border-2 border-blue-300" />
            {/each}
          </div>

          <div class="col-span-2 sm:col-span-1 mt-8">
            <label class="font-bold text-lg mt-5">Address:</label>
            <p class="my-5"><i>{client.user_address}</i></p>
            <GoogleMapVisual address={client.user_address} />
          </div>
        </div>
        <div class="mt-6 flex justify-end">
          <Button text="Approve" onClick={() => openApprovePopup()} />
          <Button text="Reject" onClick={() => openDeclinePopup()} />
        </div>
      {:else}
        <h1>Loading...</h1>
      {/if}
    </div>
  </main>


  {#if showApprovePopup}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div class="bg-white p-14 rounded-lg shadow-xl max-w-6xl mx-auto">
        <p class="text-gray-800 text-xl mb-10">Are you sure to approve the request?</p>
        <div class="flex items-center justify-center gap-3">
          <Button text="Yes" onClick={() => updateApprovalStatus('Approved')} />
          <Button text="No" onClick={() => closeApprovePopup()} />
        </div>
      </div>
    </div>
  {/if}

  {#if showRejectPopup}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
      <div class="bg-white p-14 rounded-lg shadow-xl max-w-6xl mx-auto">
        <p class="text-gray-800 text-xl mb-4">Are you sure?</p>
        <label for="">Please put a reason for rejection</label>
        <input class="text-gray-700 p-2 mt-3 rounded border border-gray-300 w-full mb-10" type="text"
               bind:value={declineReason} placeholder="Enter rejection reason" />
        <div class="flex items-center justify-center gap-3">
          <Button text="Yes" onClick={() => updateApprovalStatus('Rejected', declineReason)} />
          <Button text="No" onClick={() => closeDeclinePopup()} />
        </div>
      </div>
    </div>
  {/if}
{:else}
  <div class="flex items-center justify-center mt-20">
    <p class="font-bold text-xl">You don't have access to reach this page</p>
  </div>
{/if}
