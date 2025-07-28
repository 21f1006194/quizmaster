import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import UserDashboard from '@/views/UserDashboard.vue'
import AdminQuiz from '@/views/AdminQuiz.vue'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/admin/home',
      name: 'adminDashboard',
      component: AdminDashboard,
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/quiz',
      name: 'adminQuiz',
      component: AdminQuiz,
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/quiz-edit/:quizId',
      name: 'adminQuizEdit',
      component: () => import('../views/AdminQuizEdit.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/admin/users',
      name: 'adminUsers',
      component: () => import('../views/AdminUsersView.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/user/dashboard',
      name: 'userDashboard',
      component: UserDashboard,
      meta: { requiresAuth: true, role: 'user' },
    },
    {
      path: '/user/home',
      name: 'userHome',
      component: UserDashboard,
      meta: { requiresAuth: true, role: 'user' },
    },

    {
      path: '/user/attempt-quiz/:quizId',
      name: 'AttemptQuiz',
      component: () => import('../views/AttemptQuiz.vue'),
      props: true
    },
    {
      path: '/user/quiz-result/:quizId',
      name: 'QuizResult',
      component: () => import('../views/QuizResult.vue'),
      props: true
    },
    {
      path: '/user/result',
      name: 'ResultView',
      component: () => import('../views/ResultView.vue'),
      meta: { requiresAuth: true, role: 'user' },
    },
    {
      path: '/user/summary',
      name: 'UserSummaryView',
      component: () => import('../views/UserSummaryView.vue'),
      meta: { requiresAuth: true, role: 'user' },
    },
    {
      path: '/admin/summary',
      name: 'AdminSummaryView',
      component: () => import('../views/AdminSummaryView.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore(); // Get user authentication data
  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.role;

  if (to.path.startsWith('/public/')) {
    return next();
  }

  if (to.path.startsWith('/user/') && !isAuthenticated) {
    return next('/login');
  }

  if (to.path.startsWith('/admin/') && userRole !== 'admin') {
    return next('/login');
  }

  next();
});

export default router
