<template>
  <div class="admin-summary">
    <h1 class="page-title">Admin Dashboard</h1>
    
    <div v-if="loading" class="loading">
      <p>Loading analytics...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="quizHistory.length === 0" class="no-data">
      <p>No quiz data available.</p>
    </div>
    
    <div v-else class="dashboard-container">
      <!-- Performance Overview Cards -->
      <div class="overview-cards">
        <div class="metric-card">
          <div class="metric-value">{{ totalQuizzes }}</div>
          <div class="metric-label">Total Quizzes</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ totalAttempts }}</div>
          <div class="metric-label">Total Attempts</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ averageScore.toFixed(1) }}%</div>
          <div class="metric-label">Average Score</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ totalTimeSpent.toFixed(1) }}min</div>
          <div class="metric-label">Total Time Spent</div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="charts-container">
        <!-- Quiz Attempts per Subject -->
        <div class="chart-section">
          <div class="chart-header">
            <h2>Quiz Attempts per Subject</h2>
            <div class="info-button" title="Shows the total number of quiz attempts for each subject. Higher bars indicate more popular subjects with greater student engagement.">
              <span>ⓘ</span>
            </div>
          </div>
          <div class="chart-wrapper">
            <canvas ref="performanceChart"></canvas>
          </div>
        </div>
        
        <!-- Mark Spread per Subject -->
        <div class="chart-section">
          <div class="chart-header">
            <h2>Mark Spread per Subject</h2>
            <div class="info-button" title="Displays the percentage score distribution (Max, Average, Min) for each subject. Helps identify which subjects have the highest/lowest performance and performance variability.">
              <span>ⓘ</span>
            </div>
          </div>
          <div class="chart-wrapper">
            <canvas ref="subjectChart"></canvas>
          </div>
        </div>
        
        <!-- Quiz Difficulty Analysis -->
        <div class="chart-section">
          <div class="chart-header">
            <h2>Quiz Difficulty Analysis</h2>
            <div class="info-button" title="Bubble chart showing quiz difficulty vs success rate. Larger bubbles indicate more attempts. Helps identify which quizzes are too easy/hard and need adjustment.">
              <span>ⓘ</span>
            </div>
          </div>
          <div class="chart-wrapper">
            <canvas ref="difficultyChart"></canvas>
          </div>
        </div>
        
        <!-- Top 3 Performers -->
        <div class="chart-section">
          <div class="chart-header">
            <h2>Top 3 Performers</h2>
            <div class="info-button" title="Shows the top 3 students who have topped the most number of quizzes. Helps identify consistently high-performing students across different subjects.">
              <span>ⓘ</span>
            </div>
          </div>
          <div class="chart-wrapper">
            <canvas ref="performersChart"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { Chart, registerables } from 'chart.js';
import api from '@/api';

// Register Chart.js components
Chart.register(...registerables);

const loading = ref(false);
const error = ref(null);
const quizHistory = ref([]);

// Chart references
const performanceChart = ref(null);
const subjectChart = ref(null);
const difficultyChart = ref(null);
const performersChart = ref(null);

// Computed properties for overview metrics
const totalQuizzes = computed(() => quizHistory.value.length);
const totalAttempts = computed(() => 
  quizHistory.value.reduce((sum, quiz) => sum + quiz.total_attempts, 0)
);
const averageScore = computed(() => {
  if (quizHistory.value.length === 0) return 0;
  const totalEarnedMarks = quizHistory.value.reduce((sum, quiz) => sum + (quiz.Avg_score * quiz.total_attempts), 0);
  const totalPossibleMarks = quizHistory.value.reduce((sum, quiz) => sum + (quiz.total_marks * quiz.total_attempts), 0);
  return (totalEarnedMarks / totalPossibleMarks) * 100;
});
const totalTimeSpent = computed(() => {
  if (quizHistory.value.length === 0) return 0;
  const totalTime = quizHistory.value.reduce((sum, quiz) => sum + quiz.Total_time_spent, 0);
  return totalTime;
});

// Process data for charts
const processChartData = () => {
  // Group by subject for subject chart
  const subjectData = {};
  quizHistory.value.forEach(quiz => {
    if (!subjectData[quiz.subject_name]) {
      subjectData[quiz.subject_name] = {
        totalAttempts: 0,
        scores: [],
        quizCount: 0
      };
    }
    subjectData[quiz.subject_name].totalAttempts += quiz.total_attempts;
    subjectData[quiz.subject_name].scores.push(quiz.Avg_score);
    subjectData[quiz.subject_name].quizCount += 1;
  });

  // Calculate mark spread for each subject
  Object.keys(subjectData).forEach(subject => {
    const scores = subjectData[subject].scores;
    subjectData[subject].maxScore = Math.max(...scores);
    subjectData[subject].minScore = Math.min(...scores);
    subjectData[subject].avgScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;
  });

  return { subjectData };
};

// Generate dynamic colors for subjects
const generateSubjectColors = (subjects) => {
  const colors = [
    'rgba(75, 192, 192, 0.8)',
    'rgba(255, 99, 132, 0.8)',
    'rgba(54, 162, 235, 0.8)',
    'rgba(255, 205, 86, 0.8)',
    'rgba(153, 102, 255, 0.8)',
    'rgba(255, 159, 64, 0.8)',
    'rgba(201, 203, 207, 0.8)',
    'rgba(255, 99, 71, 0.8)',
    'rgba(50, 205, 50, 0.8)',
    'rgba(255, 140, 0, 0.8)'
  ];
  
  const colorMap = {};
  subjects.forEach((subject, index) => {
    colorMap[subject] = colors[index % colors.length];
  });
  
  return colorMap;
};

// Create charts
const createPerformanceChart = () => {
  const ctx = performanceChart.value.getContext('2d');
  const { subjectData } = processChartData();
  
  const subjects = Object.keys(subjectData);
  const attempts = subjects.map(subject => subjectData[subject].totalAttempts);
  const subjectColors = generateSubjectColors(subjects);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: subjects,
      datasets: [
        {
          label: 'Total Attempts',
          data: attempts,
          backgroundColor: subjects.map(subject => subjectColors[subject]),
          borderColor: subjects.map(subject => subjectColors[subject].replace('0.8', '1')),
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Attempts'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: 'Quiz Attempts per Subject'
        }
      }
    }
  });
};

const createSubjectChart = () => {
  const ctx = subjectChart.value.getContext('2d');
  const { subjectData } = processChartData();
  
  const subjects = Object.keys(subjectData);
  
  // Calculate percentage scores for each subject
  const maxScores = subjects.map(subject => {
    const quiz = quizHistory.value.find(q => q.subject_name === subject && q.Avg_score === subjectData[subject].maxScore);
    return quiz ? (subjectData[subject].maxScore / quiz.total_marks) * 100 : 0;
  });
  
  const minScores = subjects.map(subject => {
    const quiz = quizHistory.value.find(q => q.subject_name === subject && q.Avg_score === subjectData[subject].minScore);
    return quiz ? (subjectData[subject].minScore / quiz.total_marks) * 100 : 0;
  });
  
  const avgScores = subjects.map(subject => {
    const totalEarnedMarks = quizHistory.value
      .filter(q => q.subject_name === subject)
      .reduce((sum, quiz) => sum + (quiz.Avg_score * quiz.total_attempts), 0);
    const totalPossibleMarks = quizHistory.value
      .filter(q => q.subject_name === subject)
      .reduce((sum, quiz) => sum + (quiz.total_marks * quiz.total_attempts), 0);
    return totalPossibleMarks > 0 ? (totalEarnedMarks / totalPossibleMarks) * 100 : 0;
  });

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: subjects,
      datasets: [
        {
          label: 'Max Score (%)',
          data: maxScores,
          backgroundColor: 'rgba(75, 192, 192, 0.8)',
          borderColor: 'rgb(75, 192, 192)',
          borderWidth: 1
        },
        {
          label: 'Average Score (%)',
          data: avgScores,
          backgroundColor: 'rgba(54, 162, 235, 0.8)',
          borderColor: 'rgb(54, 162, 235)',
          borderWidth: 1
        },
        {
          label: 'Min Score (%)',
          data: minScores,
          backgroundColor: 'rgba(255, 99, 132, 0.8)',
          borderColor: 'rgb(255, 99, 132)',
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: 'Score (%)'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: 'Mark Spread per Subject'
        }
      }
    }
  });
};

const createDifficultyChart = () => {
  const ctx = difficultyChart.value.getContext('2d');
  
  const data = quizHistory.value.map(quiz => ({
    x: (1 - (quiz.Avg_score / quiz.total_marks)) * 100, // Difficulty (higher = harder)
    y: (quiz.Avg_score / quiz.total_marks) * 100, // Success rate
    r: Math.max(quiz.total_attempts * 8, 15), // Increased radius for better visibility
    label: quiz.quiz_title,
    subject: quiz.subject_name
  }));

  // Generate dynamic colors for subjects
  const subjects = [...new Set(data.map(d => d.subject))];
  const subjectColors = generateSubjectColors(subjects);

  new Chart(ctx, {
    type: 'bubble',
    data: {
      datasets: [{
        label: 'Quiz Difficulty vs Success Rate',
        data: data,
        backgroundColor: data.map(d => subjectColors[d.subject] || 'rgba(201, 203, 207, 0.7)'),
        borderColor: data.map(d => subjectColors[d.subject]?.replace('0.8', '1') || 'rgba(201, 203, 207, 1)'),
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Difficulty Level (%)'
          },
          min: 0,
          max: 100
        },
        y: {
          title: {
            display: true,
            text: 'Success Rate (%)'
          },
          min: 0,
          max: 100
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: 'Quiz Difficulty Analysis'
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const data = context.raw;
              return [
                `Quiz: ${data.label}`,
                `Difficulty: ${data.x.toFixed(1)}%`,
                `Success Rate: ${data.y.toFixed(1)}%`,
                `Attempts: ${Math.round(data.r / 8)}`
              ];
            }
          }
        }
      }
    }
  });
};

const createPerformersChart = () => {
  const ctx = performersChart.value.getContext('2d');
  
  // Get top performers and count their wins
  const topperCounts = {};
  quizHistory.value.forEach(quiz => {
    if (quiz.top_performer) {
      const topperName = quiz.top_performer.user_name;
      topperCounts[topperName] = (topperCounts[topperName] || 0) + 1;
    }
  });

  // Sort by count and get top 3
  const sortedToppers = Object.entries(topperCounts)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 3);

  const labels = sortedToppers.map(([name]) => name);
  const counts = sortedToppers.map(([,count]) => count);

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Number of Quizzes Topped',
          data: counts,
          backgroundColor: [
            'rgba(75, 192, 192, 0.8)',
            'rgba(255, 99, 132, 0.8)',
            'rgba(54, 162, 235, 0.8)'
          ],
          borderColor: [
            'rgb(75, 192, 192)',
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)'
          ],
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Number of Quizzes'
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        title: {
          display: true,
          text: 'Top 3 Performers'
        }
      }
    }
  });
};

const loadQuizHistory = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await api.get('/admin/api/quiz_summary');
    quizHistory.value = response.data;
    console.log("quizHistory", quizHistory.value);
  } catch (err) {
    console.error('Error loading quiz history:', err);
    error.value = err.response?.data?.message || 'Failed to load quiz history';
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await loadQuizHistory();
  
  // Create charts after data is loaded
  await nextTick();
  if (quizHistory.value.length > 0) {
    createPerformanceChart();
    createSubjectChart();
    createDifficultyChart();
    createPerformersChart();
  }
});
</script>

<style scoped>
.admin-summary {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2.5rem;
}

.loading, .error, .no-data {
  text-align: center;
  padding: 40px;
  font-size: 1.2rem;
  color: #666;
}

.error {
  color: #d32f2f;
}

.dashboard-container {
  margin-top: 20px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s ease;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.metric-label {
  font-size: 0.9rem;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.chart-section {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.chart-section h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.5rem;
  text-align: center;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h2 {
  margin-bottom: 0;
}

.info-button {
  background-color: #f0f0f0;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: help;
  transition: background-color 0.2s ease;
}

.info-button:hover {
  background-color: #e0e0e0;
}

.info-button span {
  font-size: 1.2rem;
  color: #555;
}

.chart-wrapper {
  position: relative;
  height: 400px;
  width: 100%;
}

/* Responsive design */
@media (max-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .overview-cards {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .chart-wrapper {
    height: 300px;
  }
  
  .page-title {
    font-size: 2rem;
  }
  
  .metric-value {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .overview-cards {
    grid-template-columns: 1fr;
  }
}
</style>