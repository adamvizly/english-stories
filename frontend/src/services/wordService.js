import axios from './axios'

export const wordService = {
  generateAIWord(level = 'BEGINNER') {
    return axios.post('/words/generate', null, {
      params: { level }
    })
  }
}
