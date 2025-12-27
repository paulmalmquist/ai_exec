import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000'
});

api.interceptors.request.use((config) => {
  const username = import.meta.env.VITE_AUTH_USER || 'admin';
  const password = import.meta.env.VITE_AUTH_PASS || 'admin';
  config.auth = { username, password };
  return config;
});

export default api;
