import axios from 'axios';

const API_URL = 'http://localhost:8000';
const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // Allows sending/receiving cookies
  xsrfCookieName: 'csrftoken', // Tells Axios to look for a cookie named 'csrftoken'
  xsrfHeaderName: 'X-CSRFToken', // Tells Axios to put that value in the 'X-CSRFToken' header
});

// Add request interceptor for debugging
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method.toUpperCase(), config.url);
    console.log('Data:', config.data);
    return config;
  },
  (error) => {
    console.error('Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.data);
    return response;
  },
  (error) => {
    console.error('Response Error:', error.response?.status, error.response?.data);
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (username, password, rememberMe = false) => {
    const response = await api.post('/login/', {
      username,
      password,
      remember_me: rememberMe,
    });
    return response.data;
  },

  signup: async (name, username, email, password, confirmPassword) => {
    const response = await api.post('/signup/', {
      name,
      username,
      email,
      password,
      confirm_password: confirmPassword,
    });
    return response.data;
  },

  logout: async () => {
    const response = await api.post('/logout/');
    return response.data;
  },

  checkAuth: async () => {
  try {
    const response = await api.get('/api/check-auth/');
    return response.data.isAuthenticated;
  } catch (error) {
    return false;
  }
},
};

// Update financeAPI object:
export const financeAPI = {
  getDashboard: async () => {
    const response = await api.get('/api/dashboard/');
    return response.data;
  },

  addIncome: async (amount, source, date) => {
    const response = await api.post('/income/add/', {
      amount,
      source,
      date,
    });
    return response.data;
  },

  deleteIncome: async (id) => {
    await api.get(`/income/delete/${id}/`);
  },

  addExpense: async (amount, description, date) => {
    const response = await api.post('/expense/add/', {
      amount,
      description,
      date,
    });
    return response.data;
  },

  deleteExpense: async (id) => {
    await api.get(`/expense/delete/${id}/`);
  },
};

export default api;