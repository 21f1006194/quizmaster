<template>
  <div class="about-container">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <h1 class="hero-title">About Quiz Master</h1>
        <p class="hero-subtitle">
          A comprehensive multi-user quiz platform designed for modern learning and exam preparation
        </p>
      </div>
    </section>

    <!-- Project Overview -->
    <section class="overview-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Project Overview</h2>
          <div class="title-underline"></div>
        </div>
        <div class="overview-content">
          <p class="overview-text">
            Quiz Master is a sophisticated multi-user quiz platform designed for comprehensive exam preparation 
            across multiple subjects and chapters. Built with modern web technologies, it provides an intuitive 
            learning experience with advanced analytics and performance tracking capabilities.
          </p>
        </div>
      </div>
    </section>

    <!-- Project Information -->
    <section class="project-info-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Project Information</h2>
          <div class="title-underline"></div>
        </div>
        <div class="project-info">
          <div class="info-card">
            <h3>Course Details</h3>
            <p><strong>Course:</strong> Modern Application Development II</p>
            <p><strong>Program:</strong> BS Degree Program</p>
            <p><strong>Institution:</strong> IIT Madras</p>
          </div>
          <div class="info-card">
            <h3>Student Information</h3>
            <p><strong>Name:</strong> Jishnu Jayaprakash</p>
            <p><strong>Roll Number:</strong> 21f1006194</p>
            <p><strong>Project:</strong> Quiz Master Platform</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Contact Section -->
    <section class="contact-section">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Get Started</h2>
          <div class="title-underline"></div>
        </div>
        <div class="contact-content">
          <p class="contact-text">
            Ready to experience the future of quiz-based learning? Join Quiz Master today and 
            take your exam preparation to the next level.
          </p>
          <div class="contact-buttons">
            <router-link to="/register" class="btn btn-primary">Get Started</router-link>
            <router-link to="/" class="btn btn-secondary">Learn More</router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.about-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.hero-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

/* Container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Section Headers */
.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
}

.title-underline {
  width: 80px;
  height: 4px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: 0 auto;
  border-radius: 2px;
}

/* Overview Section */
.overview-section {
  padding: 5rem 0;
  background: white;
}

.overview-text {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #555;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

/* Project Info Section */
.project-info-section {
  padding: 5rem 0;
  background: white;
}

.project-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.info-card {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 15px;
  border-left: 4px solid #667eea;
}

.info-card h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
}

.info-card p {
  margin: 0.5rem 0;
  color: #555;
}

.info-card strong {
  color: #333;
}

/* Contact Section */
.contact-section {
  padding: 5rem 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.contact-text {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.contact-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 0.75rem 2rem;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
  display: inline-block;
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

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .features-grid,
  .tech-grid,
  .roles-grid {
    grid-template-columns: 1fr;
  }

  .contact-buttons {
    flex-direction: column;
    align-items: center;
  }

  .btn {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 1rem;
  }

  .hero-title {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .feature-card,
  .role-card {
    padding: 2rem 1.5rem;
  }
}
</style>
