import type { Actions } from './$types';

// Exported actions object
export const _actions: Actions = {
  default: async (event) => {
    const { firstName, lastName, address, phoneNumber, email, password, rewardRequested } = event;

    const userData = {
      firstName,
      lastName,
      address,
      phoneNumber,
      email,
      password,
      rewardRequested
    };

    const response = await fetch('http://localhost:8000/api/v1/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(userData)
    });

    if (response.ok) {
      const responseData = await response.json();
      alert('User registration successful');
    } else {
      const errorData = await response.json();
      console.error('Registration failed:', errorData);
      alert('Registration failed failed'); // Display error message to the user
    }
  }
}