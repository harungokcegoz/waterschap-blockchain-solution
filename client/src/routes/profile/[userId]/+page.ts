import type { User } from '../../../types/types'
import type { Load } from '@sveltejs/kit'
import { addBearerTokenToHeaders } from '../../../stores/Store'

export const load: Load = async ({ fetch, params }) => {
  const { userId } = params as { userId: string }

  try {
    if (!userId) {
      throw new Error('User ID is missing')
    } else if (isNaN(parseInt(userId))) {
      throw new Error('User ID is invalid')
    }

    const headers = addBearerTokenToHeaders({
      'Content-Type': 'application/json'
    })

    const response = await fetch(`http://localhost:8000/api/v1/users/${userId}`,
      { headers })
    const user: User = await response.json()

    if (!response.ok) {
      throw new Error('Failed to fetch user information')
    }

    return {
      status: 200,
      body: user
    }
  } catch (error) {
    return {
      status: 500,
      body: { message: error.message }
    }
  }
}
