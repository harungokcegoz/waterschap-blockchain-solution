<script lang="ts">
  export let text: string;
  export let onClick = () => {};
  export let type: string = '';
  export let disabled: boolean = false;
  export let icon: 'arrow-right' | 'signout' | 'arrow-left' | '' = '';
  export let backgroundColor: string = 'bg-blue-600';
</script>

<button
  class={`border py-3 px-6 text-white border-white rounded-lg 
  ${backgroundColor} hover:bg-sky-700 gap-2`}
  on:click={onClick}
  {disabled}
>

    <div class="icon text-sm flex items-center gap-4">
      <div class="text">
        {text}
      </div>
      {#if icon === 'arrow-right'}
        <i class="fa-solid fa-angle-right"></i>
      {:else if icon === 'signout'}
        <i class="fa-solid fa-arrow-right-from-bracket"></i>
      {:else if icon === 'arrow-left'}
        <div class="order-first">
          <i class="fa-solid fa-angle-left"></i>
        </div>
      {/if}
    </div>

</button>
