import api from '@/api';

export const fetchCatalogData = async () => {
    try {
        // Fetch subjects and quizzes in parallel
        const [subjectsResponse, quizzesResponse] = await Promise.all([
            api.get('/admin/api/subjects'),
            api.get('/admin/api/quizzes')
        ]);

        // First, organize quizzes by chapter_id
        const quizzesByChapter = quizzesResponse.data.reduce((acc, quiz) => {
            if (!acc[quiz.chapter_id]) {
                acc[quiz.chapter_id] = [];
            }
            acc[quiz.chapter_id].push(quiz);
            return acc;
        }, {});

        // Then, structure the complete data with subjects, chapters, and their quizzes
        const organizedData = {
            subjects: subjectsResponse.data.subjects.map(subject => ({
                id: subject.id,
                name: subject.name,
                description: subject.description,
                chapters: subject.chapters.map(chapter => ({
                    id: chapter.id,
                    name: chapter.name,
                    description: chapter.description,
                    quizzes: quizzesByChapter[chapter.id] || [] // Add quizzes to each chapter
                }))
            }))
        };

        return { data: organizedData, error: null };
    } catch (error) {
        console.error('Error fetching catalog data:', error);
        return { data: null, error: error.message || 'Failed to fetch data' };
    }
}; 