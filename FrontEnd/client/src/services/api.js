import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  login: (credentials) => api.post('/login', credentials),
  register: (userData) => api.post('/register', userData),
  getProfile: () => api.get('/profile'),
  updateProfile: (data) => api.put('/profile', data),
};

export const productsAPI = {
  getAll: () => api.get('/produce_listings'),
  getById: (id) => api.get(`/produce_listings/${id}`),
  create: (data) => api.post('/produce_listings', data),
  update: (id, data) => api.put(`/produce_listings/${id}`, data),
  delete: (id) => api.delete(`/produce_listings/${id}`),
};

export const userProfileAPI = {
  getAll: () => api.get('/user_profiles'),
  getById: (id) => api.get(`/user_profiles/${id}`),
  create: (data) => api.post('/user_profiles', data),
  update: (id, data) => api.put(`/user_profiles/${id}`, data),
};

export const matchesAPI = {
  getAll: () => api.get('/matches'),
  getById: (id) => api.get(`/matches/${id}`),
  create: (data) => api.post('/matches', data),
};

export const messagesAPI = {
  getAll: () => api.get('/messages'),
  getById: (id) => api.get(`/messages/${id}`),
  create: (data) => api.post('/messages', data),
};

export const swipeAPI = {
  create: (data) => api.post('/swipe_actions', data),
  getAll: () => api.get('/swipe_actions'),
};