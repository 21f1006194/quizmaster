<template>
  <div class="user-summary">
    <h1 class="page-title">User Summary</h1>
    
    <div v-if="loading" class="loading">
      <p>Loading quiz history...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>{{ error }}</p>
    </div>
    
    <div v-else-if="quizHistory.length === 0" class="no-data">
      <p>No quiz history available.</p>
    </div>
    
    <div v-else class="dashboard-container">
      <!-- Performance Overview Cards -->
      <div class="overview-cards">
        <div class="metric-card">
          <div class="metric-value">{{ totalTimeSpent.toFixed(1) }}</div>
          <div class="metric-label">Total Time Spent (min)</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ averageScore.toFixed(1) }}%</div>
          <div class="metric-label">Average Score</div>
        </div>
        <div class="metric-card">
          <div class="metric-value">{{ totalQuizAttempts }}</div>
          <div class="metric-label">Total Quiz Attempts</div>
        </div>
      </div>

      <!-- Charts Grid -->
      <div class="charts-container">
        <!-- Performance Trend Over Time -->
        <div class="chart-section">
          <h2>Performance Trend Over Time</h2>
          <div class="chart-wrapper">
            <Line 
              :data="performanceTrendData" 
              :options="performanceTrendOptions"
              class="chart"
            />
          </div>
        </div>
        
        <!-- Score Breakdown -->
        <div class="chart-section">
          <h2>Answers Distribution</h2>
          <div class="chart-wrapper">
            <Doughnut 
              :data="scoreBreakdownData" 
              :options="scoreBreakdownOptions"
              class="chart"
            />
          </div>
        </div>
        
        <!-- Accuracy Across Quizzes -->
        <div class="chart-section">
          <h2>Accuracy Across Quizzes</h2>
          <div class="chart-wrapper">
            <Bar 
              :data="accuracyData" 
              :options="accuracyOptions"
              class="chart"
            />
          </div>
        </div>
        
        <!-- Time Spent per Quiz -->
        <div class="chart-section">
          <h2>Time Utilization per Quiz</h2>
          <div class="chart-wrapper">
            <Bar 
              :data="timeSpentData" 
              :options="timeSpentOptions"
              class="chart"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { Line, Bar, Doughnut } from 'vue-chartjs';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import api from '@/api';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const loading = ref(false);
const error = ref(null);
const quizHistory = ref([]);

const loadQuizHistory = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const response = await api.get('/user/api/quiz/history');
    quizHistory.value = response.data;
  } catch (err) {
    console.error('Error loading quiz history:', err);
    error.value = err.response?.data?.message || 'Failed to load quiz history';
  } finally {
    loading.value = false;
  }
};

// Helper function to calculate time difference in minutes
const calculateTimeSpent = (startTime, endTime) => {
  if (!startTime || !endTime) return 0;
  const start = new Date(startTime);
  const end = new Date(endTime);
  return Math.round((end - start) / (1000 * 60)); // Convert to minutes
};

// Helper function to calculate time utilization percentage
const calculateTimeUtilization = (startTime, endTime, timeDuration) => {
  if (!startTime || !endTime || !timeDuration) return 0;
  const actualTime = calculateTimeSpent(startTime, endTime);
  const utilization = (actualTime / timeDuration) * 100;
  return Math.min(utilization, 100); // Cap at 100%
};

// Helper function to calculate accuracy percentage
const calculateAccuracy = (correctCount, attemptedCount) => {
  if (attemptedCount === 0) return 0;
  return Math.round((correctCount / attemptedCount) * 100);
};

// Helper function to calculate performance percentage
const calculatePerformancePercentage = (score, maxMarks) => {
  if (maxMarks === 0) return 0;
  return Math.round((score / maxMarks) * 100);
};

// Computed properties for chart data
const performanceTrendData = computed(() => {
  const sortedHistory = [...quizHistory.value].sort((a, b) => {
    const dateA = a.quiz_date || a.start_time;
    const dateB = b.quiz_date || b.start_time;
    return new Date(dateA) - new Date(dateB);
  });

  return {
    labels: sortedHistory.map(item => {
      const date = item.quiz_date || item.start_time;
      return new Date(date).toLocaleDateString();
    }),
    datasets: [
      {
        label: 'Performance (%)',
        data: sortedHistory.map(item => 
          calculatePerformancePercentage(item.score, item.max_marks)
        ),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1,
      }
    ]
  };
});

const scoreBreakdownData = computed(() => {
  const totalCorrect = quizHistory.value.reduce((sum, item) => sum + item.correct_count, 0);
  const totalWrong = quizHistory.value.reduce((sum, item) => sum + item.wrong_count, 0);
  const totalUnattempted = quizHistory.value.reduce((sum, item) => sum + item.unattempted_count, 0);

  return {
    labels: ['Correct', 'Wrong', 'Unattempted'],
    datasets: [
      {
        data: [totalCorrect, totalWrong, totalUnattempted],
        backgroundColor: [
          'rgba(75, 192, 192, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(255, 205, 86, 0.8)'
        ],
        borderColor: [
          'rgb(75, 192, 192)',
          'rgb(255, 99, 132)',
          'rgb(255, 205, 86)'
        ],
        borderWidth: 2
      }
    ]
  };
});

const accuracyData = computed(() => {
  const sortedHistory = [...quizHistory.value].sort((a, b) => {
    const dateA = a.quiz_date || a.start_time;
    const dateB = b.quiz_date || b.start_time;
    return new Date(dateA) - new Date(dateB);
  });

  return {
    labels: sortedHistory.map(item => item.quiz_title || 'Quiz'),
    datasets: [
      {
        label: 'Accuracy (%)',
        data: sortedHistory.map(item => 
          calculateAccuracy(item.correct_count, item.attempted_count)
        ),
        backgroundColor: 'rgba(54, 162, 235, 0.8)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth: 1
      }
    ]
  };
});

const timeSpentData = computed(() => {
  const sortedHistory = [...quizHistory.value].sort((a, b) => {
    const dateA = a.quiz_date || a.start_time;
    const dateB = b.quiz_date || b.start_time;
    return new Date(dateA) - new Date(dateB);
  });

  return {
    labels: sortedHistory.map(item => item.quiz_title || 'Quiz'),
    datasets: [
      {
        label: 'Time Utilization (%)',
        data: sortedHistory.map(item => 
          calculateTimeUtilization(item.start_time, item.end_time, item.time_duration)
        ),
        backgroundColor: 'rgba(255, 159, 64, 0.8)',
        borderColor: 'rgb(255, 159, 64)',
        borderWidth: 1
      }
    ]
  };
});

// Computed properties for overview cards
const totalTimeSpent = computed(() => {
  return quizHistory.value.reduce((sum, item) => sum + calculateTimeSpent(item.start_time, item.end_time), 0);
});

const averageScore = computed(() => {
  if (quizHistory.value.length === 0) return 0;
  const totalScore = quizHistory.value.reduce((sum, item) => sum + item.score, 0);
  const totalMaxMarks = quizHistory.value.reduce((sum, item) => sum + item.max_marks, 0);
  if (totalMaxMarks === 0) return 0;
  return Math.round((totalScore / totalMaxMarks) * 100);
});

const totalQuizAttempts = computed(() => {
  return quizHistory.value.length;
});

// Chart options
const performanceTrendOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Performance Trend Over Time'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: 'Performance (%)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Quiz Date'
      }
    }
  }
};

const scoreBreakdownOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Overall Score Breakdown'
    }
  }
};

const accuracyOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Accuracy Across Quizzes'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: 'Accuracy (%)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Quiz'
      }
    }
  }
};

const timeSpentOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'top',
    },
    title: {
      display: true,
      text: 'Time Utilization per Quiz'
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      title: {
        display: true,
        text: 'Time Utilization (%)'
      }
    },
    x: {
      title: {
        display: true,
        text: 'Quiz'
      }
    }
  }
};

onMounted(() => {
  loadQuizHistory();
});
</script>

<style scoped>
.user-summary {
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
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-top: 20px;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.metric-card {
  text-align: center;
  padding: 15px;
  border-radius: 6px;
  background-color: #f8f9fa;
  border: 1px solid #e9ecef;
}

.metric-value {
  font-size: 2rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.metric-label {
  font-size: 0.9rem;
  color: #666;
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-top: 20px;
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

.chart-wrapper {
  position: relative;
  height: 400px;
  width: 100%;
}

.chart {
  width: 100% !important;
  height: 100% !important;
}

/* Responsive design */
@media (max-width: 768px) {
  .dashboard-container {
    flex-direction: column;
    gap: 20px;
  }

  .overview-cards {
    grid-template-columns: 1fr;
  }

  .charts-container {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .chart-wrapper {
    height: 300px;
  }
  
  .page-title {
    font-size: 2rem;
  }
}
</style>