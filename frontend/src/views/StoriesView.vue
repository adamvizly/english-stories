<template>
  <div class="stories">
    <h1>English Stories</h1>
    
    <div class="view-controls">
      <button 
        @click="currentView = 'list'"
        :class="{ active: currentView === 'list' }"
        class="view-btn"
      >
        View Stories
      </button>
      <button 
        @click="currentView = 'create'"
        :class="{ active: currentView === 'create' }"
        class="view-btn"
      >
        Create New Story
      </button>
    </div>

    <!-- Create New Story View -->
    <div v-if="currentView === 'create'" class="create-view">
      <div class="story-controls">
        <h2>Generate New Story</h2>
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
        {{ loadingMessage }}
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

    <!-- List Stories View -->
    <div v-else class="list-view">
      <div class="filters">
        <select v-model="filterLevel" class="select-level">
          <option value="">All Levels</option>
          <option value="BEGINNER">Beginner</option>
          <option value="INTERMEDIATE">Intermediate</option>
          <option value="ADVANCED">Advanced</option>
        </select>
        
        <input 
          v-model="filterTopic" 
          placeholder="Filter by topic..." 
          class="topic-input"
        />
        
        <button @click="fetchStories" class="filter-btn">
          Apply Filters
        </button>
      </div>

      <div v-if="loading" class="loading">
        {{ loadingMessage }}
      </div>

      <div v-else-if="stories.length" class="stories-list">
        <div v-if="currentStory" class="story-content">
          <button class="close-btn" @click="currentStory = null">×</button>
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

        <div class="story-cards">
          <div v-for="story in stories" :key="story.id" class="story-card" @click="viewStory(story)">
            <h3>{{ story.title }}</h3>
            <div class="story-meta">
              <span class="level-badge" :class="story.level.toLowerCase()">
                {{ story.level }}
              </span>
              <span class="topic-badge">{{ story.topic }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="!loading" class="no-stories">
        No stories found. Try generating a new one!
      </div>
    </div>

    <div v-if="dailyWords.length" class="daily-words">
      <h2>Daily Words</h2>
      <div 
        v-for="(wordData, index) in dailyWords" 
        :key="index" 
        class="word-card"
      >
        <h3>{{ wordData.word }}</h3>
        <p><strong>Meaning:</strong> {{ wordData.persian_meaning }}</p>
        <div v-if="wordData.synonyms && wordData.synonyms.length" class="synonyms">
          <strong>Synonyms:</strong>
          <span>{{ wordData.synonyms.join(', ') }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'

export default {
  setup() {
    const topic = ref('')
    const loading = ref(false)
    const currentStory = ref(null)
    const stories = ref([])
    const dailyWords = ref([])
    const filterLevel = ref('')
    const filterTopic = ref('')
    const loadingMessage = ref('')
    const selectedLevel = ref('')
    const currentView = ref('list')

    const generateStory = async () => {
      if (!selectedLevel.value) {
        alert('Please select a level')
        return
      }
      
      loading.value = true
      loadingMessage.value = 'Generating your story...'
      try {
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/stories/`,
          {
            title: `${topic.value || 'Random'} Story`,
            content: '',
            level: selectedLevel.value, 
            topic: topic.value || 'random'
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

    const fetchStories = async () => {
      loading.value = true
      loadingMessage.value = 'Loading stories...'
      try {
        let url = `${import.meta.env.VITE_API_URL}/stories/`
        const params = new URLSearchParams()
        if (filterLevel.value) {
          params.append('level', filterLevel.value)
        }
        if (filterTopic.value) params.append('topic', filterTopic.value)
        if (params.toString()) url += `?${params.toString()}`

        const response = await axios.get(url)
        stories.value = response.data
      } catch (error) {
        console.error('Failed to fetch stories:', error)
        alert('Failed to load stories. Please try again.')
      } finally {
        loading.value = false
      }
    }

    const fetchDailyWords = async () => {
      loading.value = true
      loadingMessage.value = 'Loading daily words...'
      try {
        const response = await axios.get(
          `${import.meta.env.VITE_API_URL}/daily-words/`
        )
        // Ensure the response is an array of word objects
        dailyWords.value = response.data || []
      } catch (error) {
        console.error('Failed to fetch daily words:', error)
        alert('Failed to load daily words. Please try again.')
        dailyWords.value = [] // Ensure it's an empty array on error
      } finally {
        loading.value = false
      }
    }

    const viewStory = (story) => {
      currentStory.value = story
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    onMounted(() => {
      fetchStories()
      fetchDailyWords()
    })

    return {
      topic,
      loading,
      currentStory,
      stories,
      dailyWords,
      filterLevel,
      filterTopic,
      loadingMessage,
      selectedLevel,
      currentView,
      generateStory,
      fetchStories,
      fetchDailyWords,
      viewStory
    }
  }
}
</script>

<style scoped>
.stories {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.view-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.view-btn {
  padding: 0.75rem 1.5rem;
  font-size: 1.1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  background-color: #f5f5f5;
  color: #666;
  transition: all 0.2s;
}

.view-btn.active {
  background-color: #2196F3;
  color: white;
}

.view-btn:hover:not(.active) {
  background-color: #e0e0e0;
}

.filters,
.story-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f5f5f5;
  border-radius: 8px;
  flex-wrap: wrap;
}

.select-level,
.topic-input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.select-level {
  min-width: 150px;
}

.topic-input {
  flex: 1;
  min-width: 200px;
}

.generate-btn,
.filter-btn {
  padding: 0.75rem 1.5rem;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  min-width: 120px;
}

.generate-btn {
  background-color: #4CAF50;
}

.filter-btn {
  background-color: #2196F3;
}

.generate-btn:hover {
  background-color: #45a049;
}

.filter-btn:hover {
  background-color: #1976D2;
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
  margin-bottom: 2rem;
  position: relative;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
  padding: 0.5rem;
  line-height: 1;
  border-radius: 50%;
}

.close-btn:hover {
  background-color: #e0e0e0;
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

.story-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  margin-top: 2rem;
}

.story-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  height: 100%;
}

.story-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.story-meta {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.level-badge,
.topic-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
}

.level-badge {
  color: white;
}

.level-badge.beginner {
  background-color: #4CAF50;
}

.level-badge.intermediate {
  background-color: #2196F3;
}

.level-badge.advanced {
  background-color: #9C27B0;
}

.topic-badge {
  background-color: #f5f5f5;
  color: #666;
}

.no-stories {
  text-align: center;
  color: #666;
  margin-top: 2rem;
  font-style: italic;
}

.daily-words {
  margin-top: 2rem;
}

.word-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
}

.word-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.synonyms {
  margin-top: 1rem;
}

@media (max-width: 600px) {
  .filters,
  .story-controls {
    flex-direction: column;
  }

  .topic-input {
    width: 100%;
  }

  .story-cards {
    grid-template-columns: 1fr;
  }
}
</style>
