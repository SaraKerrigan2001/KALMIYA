class MovieRecommender:
    def __init__(self):
        self.watched_movies = []
        self.watchlist = []

    def add_to_watchlist(self, movie_title, genre, year=None):
        """Add a movie to the watchlist."""
        self.watchlist.append({
            'title': movie_title,
            'genre': genre,
            'year': year,
            'status': 'unwatched'
        })

    def mark_watched(self, movie_index, rating=None):
        """Mark a movie as watched."""
        if movie_index < len(self.watchlist):
            movie = self.watchlist.pop(movie_index)
            movie['rating'] = rating
            self.watched_movies.append(movie)

    def get_recommendations(self, genre=None, mood=None):
        """Get movie recommendations."""
        return {
            'recommendations': [],
            'genre': genre,
            'mood': mood
        }

    def get_stats(self):
        """Get watching statistics."""
        return {'watched': len(self.watched_movies), 'watchlist': len(self.watchlist)}
