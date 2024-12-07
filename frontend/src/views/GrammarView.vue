<template>
  <div class="grammar">
    <h1>Grammar Hints</h1>
    
    <div class="grammar-controls">
      <select v-model="selectedLevel" class="select-level">
        <option value="">Select Level</option>
        <option value="BEGINNER">Beginner</option>
        <option value="INTERMEDIATE">Intermediate</option>
        <option value="ADVANCED">Advanced</option>
      </select>
      
      <button @click="getGrammarHint" class="generate-btn">
        Get Grammar Hint
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      Generating your grammar hint...
    </div>
    
    <div v-else-if="currentHint" class="hint-content">
      <h2>{{ currentHint.topic }}</h2>
      <div class="explanation">
        <h3>Explanation</h3>
        <p>{{ currentHint.explanation }}</p>
      </div>
      
      <div class="examples">
        <h3>Examples</h3>
        <ul>
          <li v-for="(example, index) in currentHint.examples" :key="index">
            {{ example }}
          </li>
        </ul>
      </div>
      
      <div class="practice">
        <h3>Practice Exercise</h3>
        <p>{{ currentHint.practice_exercise }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const selectedLevel = ref('')
const loading = ref(false)
const currentHint = ref(null)

const getGrammarHint = async () => {
  if (!selectedLevel.value) {
    alert('Please select a level')
    return
  }
  
  loading.value = true
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/grammar/hint`,
      {
        level: selectedLevel.value
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    )
    currentHint.value = response.data
  } catch (error) {
    console.error('Failed to get grammar hint:', error)
    alert('Failed to get grammar hint. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.grammar {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.grammar-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.select-level {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.generate-btn {
  background: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.generate-btn:hover {
  background: #2980b9;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.hint-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.explanation,
.examples,
.practice {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.examples ul {
  list-style: disc;
  padding-left: 1.5rem;
}

.examples li {
  margin-bottom: 0.5rem;
}
</style>
