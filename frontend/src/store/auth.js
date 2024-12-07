import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token
  },
  
  actions: {
    async loginWithGoogle(credential) {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/auth/google`, {
          token: credential
        })
        this.token = response.data.access_token
        localStorage.setItem('token', this.token)
        return true
      } catch (error) {
        console.error('Google login failed:', error)
        return false
      }
    },
    
    async logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
