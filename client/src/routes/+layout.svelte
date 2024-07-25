<script lang="ts">
  import '../app.css';
  import Header from '../components/Header.svelte'
  import '@fortawesome/fontawesome-free/css/all.min.css'
  import OnboardingPopup from '../components/OnboardingPopup.svelte'
</script>

<div class="wrapper font-lato no-scrollbar h-screen">
  <Header />
  <OnboardingPopup />
  
  <slot />
 
</div>

<style>
  * {
    overflow: hidden; /* Hide scrollbars */
  }
  .no-scrollbar {
    -ms-overflow-style: none; /* for Internet Explorer, Edge */
    scrollbar-width: none; /* for Firefox */
    overflow-y: scroll;
  }
  .no-scrollbar::-webkit-scrollbar {
    display: none; /* Safari and Chrome */
  }
</style>