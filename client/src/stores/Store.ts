import { writable } from 'svelte/store'

export const pathnameStore = writable<string>('')
export const authPopupStore = writable<string>('')
export const currentUserIdStore = writable<string>('')
export const currentAgentIdStore = writable<string>('')
export const userEmailStore = writable<string>('')

export const bearerTokenStore = writable<string>('')

export function setBearerToken(token) {
  bearerTokenStore.set(token);
}

export function removeTokenAndId() {
  bearerTokenStore.set(null);
  currentAgentIdStore.set(null);
  currentUserIdStore.set(null);
}

export function removeBearerToken() {
  bearerTokenStore.set(null);
  currentUserIdStore.set(null);
}

export function getBearerToken() {
  let token;
  bearerTokenStore.subscribe(value => {
    token = value;
  });
  return token;
}

export function addBearerTokenToHeaders(headers = {}) {
  const token = getBearerToken();
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}