<template>
  <div class="stories">
    <h1>English Stories</h1>
    
    <div class="story-controls">
      <select v-model="selectedLevel" class="select-level">
        <option value="">Select Level</option>
        <option value="beginner">Beginner</option>
        <option value="intermediate">Intermediate</option>
        <option value="advanced">Advanced</option>
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
      <p class="story-text">{{ currentStory.content }}</p>
      
      <div v-if="currentStory.grammar_notes?.length" class="grammar-notes">
        <h3>Grammar Notes</h3>
        <div 
          v-for="(note, index) in currentStory.grammar_notes" 
          :key="index" 
          class="grammar-note"
        >
          <h4>{{ note.concept }}</h4>
          <p class="explanation">{{ note.explanation }}</p>
          <div class="examples">
            <p><strong>Examples:</strong></p>
            <ul>
              <li v-for="(example, i) in note.examples" :key="i">
                {{ example }}
              </li>
            </ul>
          </div>
        </div>
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
        title: `${topic.value || 'Random'} Story`,
        content: '',
        level: selectedLevel.value.toLowerCase(),
        topic: topic.value || 'random'
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

.select-level {
  min-width: 150px;
}

.topic-input {
  flex: 1;
}

.generate-btn {
  padding: 0.5rem 1rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.generate-btn:hover {
  background-color: #45a049;
}

.loading {
  text-align: center;
  margin: 2rem 0;
  font-style: italic;
  color: #666;
}

.story-content {
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.story-content h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.story-text {
  line-height: 1.8;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.grammar-notes {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 2px solid #e0e0e0;
}

.grammar-notes h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.grammar-note {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
}

.grammar-note h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.explanation {
  color: #444;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.examples {
  background: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
}

.examples ul {
  list-style: disc;
  padding-left: 1.5rem;
  margin-top: 0.5rem;
}

.examples li {
  margin-bottom: 0.5rem;
  color: #444;
}
</style>
