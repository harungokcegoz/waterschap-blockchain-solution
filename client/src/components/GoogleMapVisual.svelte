<script lang="ts">
  import { onMount } from 'svelte';
  import axios from 'axios';

  export let address: string;

  $: location = { lat: 0, lng: 0 };
  const apiKey = 'AIzaSyDztUSLsvXXxrCExXSnwAHJqlzmRY6tjyA';
  onMount(async () => {
    const response = 
    await axios.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${address}&key=${apiKey}`);
    location = response.data.results[0].geometry.location;
  });

  </script>

  <iframe src={`https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${location.lat},${location.lng}`} width="100%" height="500" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
