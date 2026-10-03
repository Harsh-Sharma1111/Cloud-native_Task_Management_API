import client from './client';

export const authApi = {
  login: async (credentials) => {
    const response = await client.post('/auth/login', credentials);
    return response.data;
  },
  register: async (credentials) => {
    const response = await client.post('/auth/register', credentials);
    return response.data;
  },
};
