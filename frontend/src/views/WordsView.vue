<template>
  <div class="words-container">
    <h1>Words</h1>
    
    <div class="ai-word-generation">
      <h3>Generate Word with AI</h3>
      <div class="ai-word-buttons">
        <button 
          @click="generateAIWord('BEGINNER')" 
          class="btn-generate beginner"
        >
          Beginner Word
        </button>
        <button 
          @click="generateAIWord('INTERMEDIATE')" 
          class="btn-generate intermediate"
        >
          Intermediate Word
        </button>
        <button 
          @click="generateAIWord('ADVANCED')" 
          class="btn-generate advanced"
        >
          Advanced Word
        </button>
      </div>
    </div>

    <div class="words-list">
      <h2>Your Words</h2>
      <div v-if="loading" class="loading">Loading words...</div>
      <div v-else-if="words.length === 0" class="no-words">
        No words available. Generate some!
      </div>
      <div v-else class="word-grid">
        <div v-for="(word, index) in words" :key="index" class="word-card">
          <h3>{{ word.word }}</h3>
          <p><strong>Persian:</strong> {{ word.persian_meaning }}</p>
          <p v-if="word.synonyms && word.synonyms.length">
            <strong>Synonyms:</strong> {{ word.synonyms.join(', ') }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { wordService } from '../services/wordService'

const words = ref([])
const loading = ref(false)

const generateAIWord = async (level = 'BEGINNER') => {
  loading.value = true
  try {
    const response = await wordService.generateAIWord(level)
    words.value.unshift(response.data)
  } catch (error) {
    console.error('Error generating AI word:', error)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  // Optional: Fetch existing words if needed
})
</script>

<style scoped>
.words-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 10px;
}

h1, h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.ai-word-generation {
  background-color: #f0f0f0;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  text-align: center;
}

.ai-word-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 10px;
}

.btn-generate {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  color: white;
}

.btn-generate.beginner {
  background-color: #3498db;
}

.btn-generate.intermediate {
  background-color: #2ecc71;
}

.btn-generate.advanced {
  background-color: #e74c3c;
}

.words-list {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.word-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.word-card {
  background-color: #f9f9f9;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  padding: 15px;
  text-align: center;
}

.word-card h3 {
  color: #333;
  margin-bottom: 10px;
}

.loading, .no-words {
  text-align: center;
  color: #777;
  padding: 20px;
}
</style>
