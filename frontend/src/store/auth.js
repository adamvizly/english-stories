import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  
  actions: {
    async loginWithEmail(email, password) {
      this.loading = true
      this.error = null
      try {
        // Create form data
        const formData = new URLSearchParams()
        formData.append('username', email)  // FastAPI expects 'username' field
        formData.append('password', password)

        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/login`,
          formData,
          {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }
        )
        this.token = response.data.access_token
        this.user = response.data.user
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async loginWithGoogle(credential) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/google`, {
          token: credential
        })
        this.token = response.data.access_token
        this.user = response.data.user
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Google login failed'
        throw error
      } finally {
        this.loading = false
      }
    },

    async signup(email, password, name) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/signup`, {
          email,
          password,
          name
        })
        this.token = response.data.access_token
        this.user = response.data.user
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        this.error = error.response?.data?.detail || 'Signup failed'
        throw error
      } finally {
        this.loading = false
      }
    },
    
    async logout() {
      this.token = null
      this.user = null
      this.error = null
      localStorage.removeItem('token')
    }
  }
})
