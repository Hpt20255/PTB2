import axios from 'axios';
import { EquationData, ApiResponse } from '../types';

// Get API URL from environment variables
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 seconds timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`, config.data);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging and error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status}`, response.data);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API service functions
export const equationApi = {
  // Create new equation
  create: async (coefficients: { a: number; b: number; c: number }): Promise<ApiResponse<EquationData>> => {
    try {
      const response = await api.post('/api/equation', coefficients);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        return error.response.data;
      }
      throw new Error(`Network error: ${error.message}`);
    }
  },

  // Get all equations
  getAll: async (): Promise<ApiResponse<EquationData[]>> => {
    try {
      const response = await api.get('/api/equation');
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        return error.response.data;
      }
      throw new Error(`Network error: ${error.message}`);
    }
  },

  // Get equation by ID
  getById: async (id: number): Promise<ApiResponse<EquationData>> => {
    try {
      const response = await api.get(`/api/equation/${id}`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        return error.response.data;
      }
      throw new Error(`Network error: ${error.message}`);
    }
  },

  // Update equation
  update: async (id: number, coefficients: { a: number; b: number; c: number }): Promise<ApiResponse<EquationData>> => {
    try {
      const response = await api.put(`/api/equation/${id}`, coefficients);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        return error.response.data;
      }
      throw new Error(`Network error: ${error.message}`);
    }
  },

  // Delete equation
  delete: async (id: number): Promise<ApiResponse<EquationData>> => {
    try {
      const response = await api.delete(`/api/equation/${id}`);
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        return error.response.data;
      }
      throw new Error(`Network error: ${error.message}`);
    }
  },

  // Test API connection
  ping: async (): Promise<any> => {
    try {
      const response = await api.get('/ping');
      return response.data;
    } catch (error: any) {
      if (error.response?.data) {
        return error.response.data;
      }
      throw new Error(`Network error: ${error.message}`);
    }
  }
};

export default api;