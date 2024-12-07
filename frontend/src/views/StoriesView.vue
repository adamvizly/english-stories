<template>
  <div class="stories">
    <h1>English Stories</h1>
    
    <div class="story-controls">
      <select v-model="selectedLevel" class="select-level">
        <option value="">Select Level</option>
        <option value="BEGINNER">Beginner</option>
        <option value="INTERMEDIATE">Intermediate</option>
        <option value="ADVANCED">Advanced</option>
      </select>
      
      <input 
        v-model="topic" 
        placeholder="Enter a topic..." 
        class="topic-input"
      />
      
      <button @click="generateStory" class="generate-btn">
        Generate Story
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      Generating your story...
    </div>
    
    <div v-else-if="currentStory" class="story-content">
      <h2>{{ currentStory.title }}</h2>
      <p>{{ currentStory.content }}</p>
      <div class="vocabulary">
        <h3>Vocabulary</h3>
        <ul>
          <li v-for="(def, word) in currentStory.vocabulary" :key="word">
            <strong>{{ word }}</strong>: {{ def }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const selectedLevel = ref('')
const topic = ref('')
const loading = ref(false)
const currentStory = ref(null)

const generateStory = async () => {
  if (!selectedLevel.value) {
    alert('Please select a level')
    return
  }
  
  loading.value = true
  try {
    const response = await axios.post(
      `${import.meta.env.VITE_API_URL}/stories/`,
      {
        level: selectedLevel.value,
        topic: topic.value || undefined
      },
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      }
    )
    currentStory.value = response.data
  } catch (error) {
    console.error('Failed to generate story:', error)
    alert('Failed to generate story. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.stories {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.story-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.select-level,
.topic-input {
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

.story-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.vocabulary {
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.vocabulary ul {
  list-style: none;
  padding: 0;
}

.vocabulary li {
  margin-bottom: 0.5rem;
}
</style>
