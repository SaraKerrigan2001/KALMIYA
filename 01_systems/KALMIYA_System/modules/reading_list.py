class ReadingListManager:
    def __init__(self):
        self.books = []
        self.reading_history = []

    def add_book(self, title, author, genre, status='to_read'):
        """Add a book to the reading list."""
        self.books.append({
            'title': title,
            'author': author,
            'genre': genre,
            'status': status,
            'rating': None
        })

    def mark_reading(self, book_index):
        """Mark a book as currently reading."""
        if book_index < len(self.books):
            self.books[book_index]['status'] = 'reading'

    def complete_book(self, book_index, rating=None):
        """Mark a book as completed."""
        if book_index < len(self.books):
            self.books[book_index]['status'] = 'completed'
            self.books[book_index]['rating'] = rating

    def get_recommendations(self, genre=None):
        """Get book recommendations."""
        return {'recommendations': [], 'genre': genre}
