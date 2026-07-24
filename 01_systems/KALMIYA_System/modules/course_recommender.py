class CourseRecommender:
    def __init__(self):
        self.courses = []
        self.interests = []

    def set_interests(self, *interests):
        """Set learning interests and preferences."""
        self.interests = list(interests)

    def get_recommendations(self):
        """Get course recommendations based on interests."""
        return {
            'interests': self.interests,
            'recommended_courses': [],
            'count': 0
        }

    def enroll_course(self, course_id, course_name):
        """Enroll in a course."""
        self.courses.append({
            'id': course_id,
            'name': course_name,
            'progress': 0,
            'enrolled_date': None
        })

    def get_progress(self, course_id):
        """Get progress in a specific course."""
        return next((c for c in self.courses if c['id'] == course_id), None)
