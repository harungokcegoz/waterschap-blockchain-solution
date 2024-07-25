import { get } from 'svelte/store';
import { addBearerTokenToHeaders, bearerTokenStore, currentUserIdStore } from '../../stores/Store'
import type { Load } from '@sveltejs/kit';

export const load: Load = async ({ fetch }) => {
  const userId = get(currentUserIdStore);

  try {
    const headers = addBearerTokenToHeaders({
      'Content-Type': 'application/json'
    })

    const response = await fetch(`http://localhost:8000/api/v1/users/${userId}/address`,
      { headers })

    if (!response.ok) {
      throw new Error('Failed to fetch user address');
    }

    const userAddress: string = await response.json();

    return {
      props: {
        userAddress
      }
    };
  } catch (error) {
    return {
      status: 500,
      body: { message: error.message }
    };
  }


};
