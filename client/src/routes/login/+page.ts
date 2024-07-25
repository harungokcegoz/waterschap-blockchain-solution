import type { Actions } from './$types';
import { bearerTokenStore, currentAgentIdStore } from '../../stores/Store'

export const _actions: Actions = {
  default: async (event) => {
    const { email, password } = event;

    const userData = {
      email,
      password
    };
    
    const response = await fetch('http://localhost:8000/api/v1/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });
    
    if (response.ok) {
      const responseData = await response.json();
      bearerTokenStore.set(responseData.access_token);
      currentAgentIdStore.set(responseData.agent_id);
      alert(`User login successful`);
    } else {
      const errorData = await response.json();
      console.error('Login failed:', errorData);
      alert('Login failed'); // Display error message to the user
    }
  },
};
