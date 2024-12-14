import api from './api'

export const wordService = {
  getDailyWords() {
    return api.get('/daily-words/')
  },

  updateEnglishLevel(level) {
    return api.patch('/users/english-level', { level })
  }
}
