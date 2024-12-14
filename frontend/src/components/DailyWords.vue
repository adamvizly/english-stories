<template>
  <div class="daily-words">
    <h2 class="text-2xl font-bold mb-6">Daily Words</h2>
    
    <div v-if="loading" class="flex justify-center items-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
    </div>

    <div v-else-if="error" class="text-red-500 p-4 rounded-lg bg-red-50">
      {{ error }}
    </div>

    <div v-else class="grid gap-4">
      <div v-for="word in words" :key="word.id" 
           class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
        <div class="flex justify-between items-start">
          <div>
            <h3 class="text-xl font-semibold text-primary">{{ word.word }}</h3>
            <p class="text-lg mt-2 text-gray-700">{{ word.persian_meaning }}</p>
          </div>
          <button @click="toggleSynonyms(word)" 
                  class="text-sm px-3 py-1 rounded-full bg-primary/10 text-primary hover:bg-primary/20 transition-colors">
            {{ word.showSynonyms ? 'Hide' : 'Show' }} Synonyms
          </button>
        </div>
        
        <transition name="fade">
          <div v-if="word.showSynonyms" class="mt-4">
            <p class="text-sm text-gray-600">Synonyms:</p>
            <div class="flex flex-wrap gap-2 mt-1">
              <span v-for="synonym in word.synonyms" :key="synonym"
                    class="px-2 py-1 text-sm bg-gray-100 rounded-full text-gray-700">
                {{ synonym }}
              </span>
            </div>
          </div>
        </transition>
      </div>
    </div>

    <div v-if="words.length === 0" class="text-center py-8 text-gray-500">
      No words available for today. Check back tomorrow!
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { wordService } from '@/services/wordService'

export default {
  name: 'DailyWords',
  
  setup() {
    const words = ref([])
    const loading = ref(true)
    const error = ref(null)

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

    const toggleSynonyms = (word) => {
      word.showSynonyms = !word.showSynonyms
    }

    onMounted(fetchDailyWords)

    return {
      words,
      loading,
      error,
      toggleSynonyms
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
