import type { Load } from '@sveltejs/kit'
import type { Request } from '../../../../types/types'
import { addBearerTokenToHeaders } from '../../../../stores/Store'
import { updateClientWithImageUrls } from '../../../../utils/utils'

export const load: Load = async ({ fetch, params }) => {
  const { id } = params as { id: string }

  try {
    if (!id) {
      throw new Error('Request ID is missing')
    } else if (Number.isNaN(parseInt(id))) {
      throw new Error('Request ID is invalid')
    }

    const headers = addBearerTokenToHeaders({
      'Content-Type': 'application/json'
    })

    const response = await fetch(`http://localhost:8000/api/v1/agent/requests/${id}`,
      { headers })

    if (!response.ok) {
      throw new Error('Failed to fetch request information')
    }

    const request: Request = await response.json()

    return {
      status: 200,
      body: await updateClientWithImageUrls(request),
      requestId: id
    }
  } catch (error) {
    return {
      status: 500,
      body: { message: error.message }
    }
  }
}
