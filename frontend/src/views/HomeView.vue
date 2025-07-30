<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToLogin = () => {
  router.push('/login')
}

const navigateToRegister = () => {
  router.push('/register')
}

const features = [
  {
    icon: '📅',
    title: 'Daily Reminders',
    description: 'Stay on track with personalized daily quiz reminders and progress notifications.'
  },
  {
    icon: '📊',
    title: 'Monthly Reports',
    description: 'Comprehensive monthly performance reports with detailed insights and trends.'
  },
  {
    icon: '📈',
    title: 'Detailed Analytics',
    description: 'Advanced analytics dashboard with performance metrics and learning patterns.'
  },
  {
    icon: '🏆',
    title: 'Leaderboard',
    description: 'Compete with others and track your ranking on interactive leaderboards.'
  },
  {
    icon: '⚡',
    title: 'Instant Feedback',
    description: 'Get immediate results with detailed answer keys and explanations for better learning.'
  },
  {
    icon: '📚',
    title: 'Diverse Topics',
    description: 'Access quizzes across multiple subjects and topics to expand your knowledge base.'
  }
]
</script>

<template>
  <div class="home-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            Master Your Knowledge with
            <span class="highlight">Quiz Master</span>
          </h1>
          <p class="hero-subtitle">
            A quiz platform designed to enhance your learning experience with 
            personalized analytics, progress tracking, and competitive features.
          </p>
          <div class="hero-buttons">
            <button @click="navigateToLogin" class="btn btn-primary">
              Login
            </button>
            <button @click="navigateToRegister" class="btn btn-secondary">
              Register
            </button>
          </div>
        </div>
        <div class="hero-image">
          <img src="/quiz_master_cover.png" alt="Quiz Master" class="cover-image" />
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="container">
        <h2 class="section-title">Why Choose Quiz Master?</h2>
        <div class="features-grid">
          <div 
            v-for="feature in features" 
            :key="feature.title"
            class="feature-card"
          >
            <div class="feature-icon">{{ feature.icon }}</div>
            <h3 class="feature-title">{{ feature.title }}</h3>
            <p class="feature-description">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <h2 class="cta-title">Ready to Start Your Learning Journey?</h2>
        <p class="cta-subtitle">
          Join thousands of learners who are already improving their knowledge with Quiz Master.
        </p>
        <div class="cta-buttons">
          <button @click="navigateToRegister" class="btn btn-primary btn-large">
            Get Started Free
          </button>
          <button @click="navigateToLogin" class="btn btn-outline btn-large">
            Sign In
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Hero Section */
.hero-section {
  padding: 4rem 2rem;
  min-height: 80vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-text {
  color: white;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 1.5rem;
}

.highlight {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 2.5rem;
  opacity: 0.9;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
}

.cover-image {
  max-width: 100%;
  height: auto;
  border-radius: 20px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease;
}

.cover-image:hover {
  transform: translateY(-10px);
}

/* Buttons */
.btn {
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
}

.btn-primary {
  background: linear-gradient(45deg, #ffd700, #ffed4e);
  color: #333;
  box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: #333;
  transform: translateY(-2px);
}

.btn-outline {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-outline:hover {
  background: white;
  color: #333;
  transform: translateY(-2px);
}

.btn-large {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
}

/* Features Section */
.features-section {
  padding: 5rem 2rem;
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: white;
  padding: 2.5rem 2rem;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
  display: block;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.feature-description {
  color: #666;
  line-height: 1.6;
  font-size: 1rem;
}

/* CTA Section */
.cta-section {
  padding: 5rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  text-align: center;
  color: white;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.cta-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-content {
    grid-template-columns: 1fr;
    gap: 2rem;
    text-align: center;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }

  .hero-buttons {
    justify-content: center;
  }

  .section-title {
    font-size: 2rem;
  }

  .cta-title {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 2rem 1rem;
  }

  .features-section,
  .cta-section {
    padding: 3rem 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .section-title,
  .cta-title {
    font-size: 1.75rem;
  }
}
</style>
