<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800">Daily Words</h1>
        <div class="relative">
          <select 
            v-model="selectedLevel" 
            @change="updateLevel"
            class="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 leading-tight focus:outline-none focus:border-primary hover:border-gray-400"
          >
            <option value="BEGINNER">Beginner</option>
            <option value="INTERMEDIATE">Intermediate</option>
            <option value="ADVANCED">Advanced</option>
          </select>
          <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
            <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
              <path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/>
            </svg>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="bg-red-50 border-l-4 border-red-500 p-4 mb-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
          </div>
          <div class="ml-3">
            <p class="text-sm text-red-700">{{ error }}</p>
          </div>
        </div>
      </div>

      <!-- Word Cards -->
      <div v-else class="grid gap-6">
        <div v-for="word in words" :key="word.id" 
             class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
          <div class="p-6">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-2xl font-bold text-gray-900">{{ word.word }}</h3>
                <p class="mt-2 text-lg text-gray-600">{{ word.persian_meaning }}</p>
              </div>
              <button 
                @click="toggleSynonyms(word)"
                class="px-4 py-2 text-sm font-medium text-primary bg-primary/10 rounded-full hover:bg-primary/20 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary/50 transition-colors"
              >
                {{ word.showSynonyms ? 'Hide' : 'Show' }} Synonyms
              </button>
            </div>
            
            <transition 
              enter-active-class="transition ease-out duration-200"
              enter-from-class="opacity-0 transform -translate-y-2"
              enter-to-class="opacity-100 transform translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="opacity-100 transform translate-y-0"
              leave-to-class="opacity-0 transform -translate-y-2"
            >
              <div v-if="word.showSynonyms" class="mt-4">
                <div class="flex flex-wrap gap-2">
                  <span 
                    v-for="synonym in word.synonyms" 
                    :key="synonym"
                    class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-800"
                  >
                    {{ synonym }}
                  </span>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && !error && words.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V7a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No words for today</h3>
        <p class="mt-1 text-sm text-gray-500">Check back tomorrow for new words!</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { wordService } from '../services/wordService'
import { useToast } from 'vue-toastification'

export default {
  name: 'DailyWordsView',
  
  setup() {
    const words = ref([])
    const loading = ref(true)
    const error = ref(null)
    const selectedLevel = ref('BEGINNER')
    const toast = useToast()

    const fetchDailyWords = async () => {
      try {
        loading.value = true
        error.value = null
        const response = await wordService.getDailyWords()
        words.value = response.data.map(word => ({
          ...word,
          showSynonyms: false
        }))
      } catch (err) {
        error.value = 'Failed to load daily words. Please try again later.'
        console.error('Error fetching daily words:', err)
      } finally {
        loading.value = false
      }
    }

    const updateLevel = async () => {
      try {
        await wordService.updateEnglishLevel(selectedLevel.value)
        toast.success('English level updated successfully')
        await fetchDailyWords() // Refresh words for new level
      } catch (err) {
        toast.error('Failed to update English level')
        console.error('Error updating English level:', err)
      }
    }

    const toggleSynonyms = (word) => {
      word.showSynonyms = !word.showSynonyms
    }

    onMounted(fetchDailyWords)

    return {
      words,
      loading,
      error,
      selectedLevel,
      toggleSynonyms,
      updateLevel
    }
  }
}
</script>
