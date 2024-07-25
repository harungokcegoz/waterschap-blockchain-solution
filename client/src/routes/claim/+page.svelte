<script lang='ts'>
  import Button from '../../components/Button.svelte'
  import { page } from '$app/stores'
  import { bearerTokenStore, pathnameStore, currentUserIdStore, addBearerTokenToHeaders } from '../../stores/Store'
  import { get, writable } from 'svelte/store'
  import { useImageUploadIpfs } from '../../hooks/useImageUploadIpfs'
  import { goto } from '$app/navigation'
  import type { Measure } from '../../types/types'
  import { onMount } from 'svelte'

  pathnameStore.set($page.url.pathname)

  export let userAddress: string

  let selectedType = '1'
  let file: File | null = null
  let cid: string | null = null
  let filePreviewUrl: string | null = null
  let uploadStatus = '';
  let showModal = writable(false);

  const { isLoading, uploadImage } = useImageUploadIpfs()

  const measureTypes = [
    { type: 'Rain Barrel', unit: 'Liters' },
    { type: 'Green Roof', unit: 'Square meters' }
  ]

  const measureRows = writable<Measure[]>([{ measure_type: '', measure_value: '' }])

  function addMeasureRow() {
    measureRows.update(rows => [...rows, { measure_type: '', measure_value: '' }])
  }

  function removeMeasureRow(index: number) {
    measureRows.update(rows => rows.filter((_, i) => i !== index))
  }

  function updateMeasureValue(measureType: string): string {
    const selectedType = measureTypes.find(type => type.type === measureType)
    return selectedType ? selectedType.unit : ''
  }

  function selectType(type: string) {
    selectedType = type
  }

  const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    if (target.files && target.files[0]) {
      file = target.files[0]
      filePreviewUrl = URL.createObjectURL(file)
      uploadStatus = '';
    }
  }

  const handleUpload = async () => {
    if (file) {
      cid = await uploadImage(file)
      if (cid) {
        console.log(`Image uploaded successfully. CID: ${cid}`)
        uploadStatus = 'uploaded'
      } else {
        uploadStatus = ''
      }
    } else {
      console.error('No file selected')
    }
  }

  function getInstallationType(type: string): string {
    return type === '1' ? 'By Technician' : 'Self'
  }

  async function createNewRequest() {
    if (!cid || get(measureRows).length === 0 || get(measureRows).some(row => !row.measure_type || !row.measure_value)) {
      showModal.set(true);
      return;
    }

    try {
      const measures = get(measureRows).map(row => ({
        measure_type: row.measure_type,
        measure_value: row.measure_value
      }))

      let userId = get(currentUserIdStore)

      const requestFormData = {
        user_id: userId,
        user_address: userAddress,
        approval_status: 'Pending',
        rejection_reason: '',
        date_requested: new Date().toISOString(),
        installation_type: getInstallationType(selectedType),
        image_hashes: [cid],
        agent_id: 1,  // Use actual agent_id
        measures,
        date_approved: null,
        date_rejected: null
      }

      const headers = addBearerTokenToHeaders({
        'Content-Type': 'application/json'
      })

      const response = await fetch('http://localhost:8000/api/v1/requests/', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestFormData)
      })

      if (response.ok) {
        alert('Request creation successful')
        await goto(`/requests/?userId=${$currentUserIdStore}`)
      } else {
        const errorData = await response.json()
        console.log('Request creation failed:', errorData)
      }
    } catch (error) {
      console.error('Error creating request:', error)
    }
  }

  onMount(async () => {
    pathnameStore.set(window.location.pathname)
    try {
      const response =
        await fetch(`http://localhost:8000/api/v1/users/${$currentUserIdStore}/address`)

      if (!response.ok) {
        throw new Error('Failed to fetch user info')
      }

      userAddress = await response.json()
    } catch (error) {
      console.error('Error fetching user info:', error)
    }
  })

  function closeModal() {
    showModal.set(false);
  }

</script>

{#if $bearerTokenStore}
  <div class="claim-form mx-80 my-10 justify-center ring-1 p-10 ring-gray-200 shadow-lg rounded-lg no-scrollbar">
    <!-- Header Section -->
    <div class="mb-10">
      <h1 class="text-3xl font-bold text-center">Make a New Claim</h1>
      <hr class="mt-4 border-t-2 border-gray-300">
    </div>
    <div class="claim-form__content mt-16 grid grid-cols-2 gap-10">
      <!-- Image Uploader Section -->
      <div class="image-uploader border-4 border-blue-500 border-dashed p-10 rounded-xl">
        <div class="image-uploader__content flex flex-col justify-center items-center min-h-96 gap-5">
          <div class="image-uploader__content__image w-1/3">
            <img src={filePreviewUrl || "https://miro.medium.com/v2/resize:fit:512/1*sjvJLkqNLyeLv1KkeFiD4Q.png"} alt="upload-box" />
          </div>
          <div class="image-uploader__content__button">
            <input
              type="file"
              name="file"
              on:change={handleFileChange}
              class="hidden"
              id="fileInput" />
            <label for="fileInput" class="rounded-xl bg-blue-500 px-6 py-2 text-white cursor-pointer">
              Browse files
            </label>
          </div>
          <h2 class="mt-10 font-light text-grey-500">*Only PNG and JPEG files are supported </h2>
          <Button text="Upload" onClick={handleUpload} backgroundColor="bg-blue-500" />
          {#if $isLoading}
            <p>Uploading...</p>
          {/if}
          {#if uploadStatus === 'uploaded'}
            <p class="text-lg text-green-600">Uploaded successfully!</p>
          {/if}
        </div>
      </div>
      <!-- Info Input Section -->
      <div class="basic-info flex flex-col gap-5 mr-10">
        <h1 class="text-2xl font-bold">Installation Info</h1>
        <div class="measure-rows flex flex-col">
          {#each $measureRows as measureRow, index}
            <div class="flex items-center space-x-4" key={index}>
              <div class="dropdown inline-block relative">
                <select
                  class="block appearance-none bg-white border border-gray-400 hover:border-gray-500
                                    px-4 py-2 pr-8 rounded shadow leading-tight focus:outline-none focus:shadow-outline"
                  bind:value={measureRow.measure_type}>
                  <option value="">Select Measure Type</option>
                  {#each measureTypes as measureType}
                    <option value={measureType.type}>{measureType.type}</option>
                  {/each}
                </select>
                <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
                  <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
                    <path d="M9 11V5l7 6-7 6v-6z" />
                  </svg>
                </div>
              </div>
              <input
                type="text"
                class="appearance-none border rounded py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                placeholder={`Enter value in ${updateMeasureValue(measureRow.measure_type)}` }
                bind:value={measureRow.measure_value} />
              <button class="remove-button" on:click={() => removeMeasureRow(index)}>
                <svg class="fill-current h-6 w-6 text-red-600" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 6h18v2H3V6zm2 4h14v12H5V10zm4-6h6v2H9V4z" />
                </svg>
              </button>
            </div>
          {/each}
        </div>
        <div class="mt-4">
          <Button text="Add Measure Row" backgroundColor="bg-blue-500" onClick={addMeasureRow} />
        </div>
        <div class="selector">
          <label for="installation-type" class="block mb-2 text-sm font-bold">Installation Type</label>
          <div id="installation-type" class="flex ring-1 ring-gray-200 rounded-xl w-fit">
            <button
              class={`px-4 py-2 rounded-l-xl ${selectedType === '1' ? 'bg-blue-500 text-white' :
                             'bg-white text-blue-500'}`}
              on:click={() => selectType('1')}
            >
              By Technician
            </button>
            <button
              class={`px-4 py-2 rounded-r-xl ${selectedType === '2' ? 'bg-blue-500 text-white' :
                             'bg-white text-blue-500'}`}
              on:click={() => selectType('2')}
            >
              Self
            </button>
          </div>
        </div>
        <div class="button flex justify-end">
          <Button text="Submit Claim" icon='arrow-right' backgroundColor="bg-blue-500" onClick={createNewRequest} />
        </div>
      </div>
    </div>
  </div>
{/if}
{#if $showModal}
  <div class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
    <div class="bg-white p-8 rounded-lg shadow-lg">
      <h2 class="text-2xl font-bold mb-4">Incomplete Form</h2>
      <p class="mb-4">Please fill in all fields and upload an image before submitting.</p>
      <div class="button flex justify-end">
        <Button text="Close" onClick={closeModal} backgroundColor="bg-red-500" />
      </div>
    </div>
  </div>
{/if}