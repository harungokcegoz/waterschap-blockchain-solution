import type { Load } from '@sveltejs/kit';
import type { Request } from '../../../types/types';
import { addBearerTokenToHeaders } from '../../../stores/Store';

export const load: Load = async ({ fetch, url }) => {
  const agentId = url.searchParams.get('agentId');

  try {
    if (!agentId) {
      throw new Error('Agent ID is missing');
    } else if (Number.isNaN(parseInt(agentId))) {
      throw new Error('Agent ID is invalid');
    }

    const headers = addBearerTokenToHeaders({
      'Content-Type': 'application/json'
    })

    const response = await fetch(`http://localhost:8000/api/v1/agents/${agentId}/requests`,
      { headers })

    if (!response.ok) {
      throw new Error('Failed to fetch request information');
    }

    const request: Request = await response.json();

    return {
      status: 200,
      body: request,
    }
  } catch (error) {
    return {
      status: 500,
      body: { message: error.message }
    }
  }
}
