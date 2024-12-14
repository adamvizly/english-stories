import axios from 'axios'

const API_URL = '/api/auth'

export const login = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/login`, { email, password })
    localStorage.setItem('token', response.data.access_token)
    return response.data
  } catch (error) {
    throw error.response?.data || new Error('Login failed')
  }
}

export const signup = async (email, password) => {
  try {
    const response = await axios.post(`${API_URL}/signup`, { email, password })
    localStorage.setItem('token', response.data.access_token)
    return response.data
  } catch (error) {
    throw error.response?.data || new Error('Signup failed')
  }
}

export const googleAuth = async () => {
  try {
    const response = await axios.post(`${API_URL}/google`)
    localStorage.setItem('token', response.data.access_token)
    return response.data
  } catch (error) {
    throw error.response?.data || new Error('Google authentication failed')
  }
}

export const getCurrentUser = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/me`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  } catch (error) {
    throw error.response?.data || new Error('Failed to fetch user')
  }
}

export const logout = () => {
  localStorage.removeItem('token')
}
