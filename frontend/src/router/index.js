import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Stories',
    component: () => import('../views/StoriesView.vue')
  },
  {
    path: '/words',
    name: 'Words',
    component: () => import('../views/DailyWordsView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
