export type User = {
  first_name: string
  last_name: string
  address: string
  phone_number: string
  email: string
  reward_requested: boolean
}

export type Measure = {
  measure_type: string
  measure_value: string
}

export type Request = {
  request_id: number
  user: {
    first_name: string;
    last_name: string;
  }
  user_id: number
  user_address: string
  measures:Measure[]
  approval_status: string
  rejection_reason: string
  date_requested: string
  date_approved: string
  date_rejected: string
  installation_type: string
  image_hashes: string[]
  agent_id: number
}