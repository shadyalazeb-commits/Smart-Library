from db.database import Database

class LibraryLogic:
    def __init__(self):
        self.db = Database()

    # هل الكتاب متاح؟
    def is_book_available(self, book_id):
        query = """
        SELECT * FROM Loans
        WHERE BookID = %s AND ReturnDate IS NULL
        """
        result = self.db.fetch_one(query, (book_id,))
        return result is None

    # إعارة كتاب
    def borrow_book(self, member_id, book_id):
        if not self.is_book_available(book_id):
            return False, "❌ الكتاب متعار بالفعل"

        query = """
        INSERT INTO Loans (MemberID, BookID)
        VALUES (%s, %s)
        """
        self.db.execute(query, (member_id, book_id))
        return True, "✅ تم إعارة الكتاب بنجاح"
    
    # إرجاع كتاب
    def return_book(self, book_id):
        query = """
        UPDATE Loans
        SET ReturnDate = CURRENT_DATE
        WHERE BookID = %s AND ReturnDate IS NULL
        """
        self.db.execute(query, (book_id,))
        return "Book returned successfully"
    
# إحصائيات لوحة التحكم  

    def dashboard_stats(self):
        stats = {}

        stats["total_books"] = self.db.fetch_one(
            "SELECT COUNT(*) AS total FROM Books"
        )["total"]

        stats["total_members"] = self.db.fetch_one(
            "SELECT COUNT(*) AS total FROM Members"
        )["total"]

        stats["borrowed_books"] = self.db.fetch_one(
            "SELECT COUNT(*) AS total FROM Loans WHERE ReturnDate IS NULL"
        )["total"]

        return stats
# 📊 تقرير أكثر الكتب استعارة
    def most_borrowed_books(self, limit=5):
        query = """
        SELECT B.Title, COUNT(L.LoanID) AS borrow_count
        FROM Loans L
        JOIN Books B ON L.BookID = B.BookID
        GROUP BY B.Title
        ORDER BY borrow_count DESC
        LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

    # 👤 أكثر الأعضاء نشاطًا
    def most_active_members(self, limit=5):
        query = """
        SELECT M.Name, COUNT(L.LoanID) AS loans_count
        FROM Loans L
        JOIN Members M ON L.MemberID = M.MemberID
        GROUP BY M.Name
        ORDER BY loans_count DESC
        LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))

    # 📚 حالة الكتب
    def books_status(self):
        query = """
        SELECT 
            SUM(CASE WHEN L.ReturnDate IS NULL THEN 1 ELSE 0 END) AS borrowed,
            COUNT(B.BookID) - SUM(CASE WHEN L.ReturnDate IS NULL THEN 1 ELSE 0 END) AS available
        FROM Books B
        LEFT JOIN Loans L ON B.BookID = L.BookID
        """

        result = self.db.fetch_one(query)

        return {
            "borrowed": int(result["borrowed"]),
            "available": int(result["available"])
        }
    
    # اكثر الكتب تقييماً
    def top_rated_books(self, limit=5):
        query = """
        SELECT 
        B.Title,
        ROUND(AVG(R.Rating), 2) AS avg_rating,
        COUNT(R.ReviewID) AS reviews_count
        FROM Reviews R
        JOIN Books B ON R.BookID = B.BookID
        GROUP BY B.BookID, B.Title
        ORDER BY avg_rating DESC
        LIMIT %s
        """
        return self.db.fetch_all(query, (limit,))
    
    # بحث ذكي عن الكتب
    def smart_search(self, keyword):
        query = """
        SELECT Title, Author, Genre
        FROM Books
        WHERE Title LIKE %s OR Author LIKE %s OR Genre LIKE %s
        """
        like = f"%{keyword}%"
        return self.db.fetch_all(query, (like, like, like))