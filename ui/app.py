# نافذة رئيسية 

import keyword
import customtkinter as ctk
from tkinter import messagebox
from logic.library_logic import LibraryLogic

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SmartLibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.logic = LibraryLogic()

        self.title("📚 Smart Library System")
        self.geometry("1000x650")
        self.resizable(False, False)

        self.build_tabs()

    def build_tabs(self):
        self.tabs = ctk.CTkTabview(self, width=960, height=600)
        self.tabs.pack(padx=20, pady=20)

        self.dashboard_tab = self.tabs.add("📊 Dashboard")
        self.borrow_tab = self.tabs.add("📕 Borrow")
        self.review_tab = self.tabs.add("⭐ Reviews")
        self.search_tab = self.tabs.add("🔍 Smart Search")

        self.build_dashboard()
        self.build_borrow_tab()
        self.build_review_tab()
        self.build_search_tab()
# Dashboard ذكي 

    def build_dashboard(self):
        stats = self.logic.dashboard_stats()

        ctk.CTkLabel(self.dashboard_tab,text="📊 Library Overview",font=("Arial", 22, "bold")).pack(pady=20)

        for key, value in stats.items():
            ctk.CTkLabel(self.dashboard_tab,text=f"{key.replace('_',' ').title()}: {value}",font=("Arial", 18)).pack(pady=8)   

# نظام الإعارة الذكي 
 
    def build_borrow_tab(self):
        ctk.CTkLabel(
            self.borrow_tab,
            text="📕 Borrow Book",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        self.member_entry = ctk.CTkEntry(
            self.borrow_tab,
            placeholder_text="Member ID"
        )
        self.member_entry.pack(pady=10)

        self.book_entry = ctk.CTkEntry(
            self.borrow_tab,
            placeholder_text="Book ID"
        )
        self.book_entry.pack(pady=10)

        ctk.CTkButton(
            self.borrow_tab,
            text="Borrow Book",
            command=self.borrow_book
        ).pack(pady=20)

    def borrow_book(self):
        member_id = self.member_entry.get()
        book_id = self.book_entry.get()

        # ✅ Validation
        if not member_id or not book_id:
            messagebox.showerror("❌ Error", "All fields are required")
            return

        try:
            success, msg = self.logic.borrow_book(int(member_id), int(book_id))

            if success:
                messagebox.showinfo("✅ Success", msg)
            else:
                messagebox.showerror("❌ Failed", msg)

        except ValueError:
            messagebox.showerror("❌ Error", "Member ID and Book ID must be numbers")

        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
   
#  build_add_review_form 
 
    def build_add_review_form(self, parent_frame):
        ctk.CTkLabel(parent_frame,text="⭐ Add Review",font=("Arial", 22, "bold")).pack(pady=20)
        self.review_book = ctk.CTkEntry(parent_frame,placeholder_text="Book ID")
        self.review_book.pack(pady=8)

        self.review_member = ctk.CTkEntry(
            parent_frame,
            placeholder_text="Member ID"
        )
        self.review_member.pack(pady=8)

        self.review_rating = ctk.CTkEntry(
            parent_frame,
            placeholder_text="Rating (1-5)"
        )
        self.review_rating.pack(pady=8)

        self.review_comment = ctk.CTkEntry(
            parent_frame,
            placeholder_text="Comment"
        )
        self.review_comment.pack(pady=8)

        ctk.CTkButton(
            parent_frame,
            text="Submit Review",
            command=self.add_review
        ).pack(pady=20)

    def add_review(self):
        try:
            book_id = self.review_book.get()
            member_id = self.review_member.get()
            rating = self.review_rating.get()
            comment = self.review_comment.get()

            # ✅ Validation
            if not book_id or not member_id or not rating:
                messagebox.showerror("❌ Error", "All fields are required")
                return

            rating = int(rating)
            if rating < 1 or rating > 5:
                messagebox.showerror("❌ Error", "Rating must be between 1 and 5")
                return

            self.logic.add_review(
                int(book_id),
                int(member_id),
                rating,
                comment
            )

            messagebox.showinfo("⭐ Success", "Review added successfully")

            # ✅ Refresh table
            self.load_top_rated_books()

        except ValueError:
            messagebox.showerror("❌ Error", "IDs and Rating must be numbers")

        except Exception as e:
            messagebox.showerror("❌ Error", str(e))
# بحث ذكي عن الكتب  

    def build_search_tab(self):
        ctk.CTkLabel(
            self.search_tab,
            text="🔍 Smart Search",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        self.search_entry = ctk.CTkEntry(
            self.search_tab,
            placeholder_text="Search by book title"
        )
        self.search_entry.pack(pady=10)

        ctk.CTkButton(
            self.search_tab,
            text="Search",
            command=self.search_books
        ).pack(pady=10)

    def search_books(self):
        keyword = self.search_entry.get()

    # ✅ Validation
        if not keyword:
            messagebox.showwarning("⚠️ Warning", "Enter search keyword")
            return

        # ✅ مسح النتائج القديمة
        for widget in self.search_tab.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget != self.search_entry:
                widget.destroy()
                results = self.logic.smart_search(keyword)

            if not results:
                messagebox.showinfo("ℹ️ Info", "No results found")
                return

        for book in results:
            ctk.CTkLabel(
                self.search_tab,
                text=f"📘 {book['Title']} | {book['Author']} | {book['Genre']}",
                font=("Arial", 14)
            ).pack(pady=4)

# Review Tab Layout

    def build_review_tab(self):
        # Create 2 columns
        self.review_tab.grid_columnconfigure(0, weight=1)
        self.review_tab.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(self.review_tab, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        right_frame = ctk.CTkFrame(self.review_tab, fg_color="transparent")
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.build_add_review_form(left_frame)
        self.build_top_rated_section(right_frame)

    def build_top_rated_section(self, parent_frame):
        ctk.CTkLabel(
            parent_frame,
            text="⭐ Top Rated Books",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        columns_frame = ctk.CTkFrame(parent_frame)
        columns_frame.pack(pady=10)

        headers = ["Title", "Avg Rating", "Reviews"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                columns_frame,
                text=h,
                font=("Arial", 14, "bold"),
                width=200
            ).grid(row=0, column=i, padx=10)

        self.reviews_table = ctk.CTkFrame(parent_frame)
        self.reviews_table.pack()

        self.load_top_rated_books()   
    def load_top_rated_books(self):
        for widget in self.reviews_table.winfo_children():
            widget.destroy()

        books = self.logic.top_rated_books()

        for row, book in enumerate(books, start=1):
            ctk.CTkLabel(
                self.reviews_table,
                text=book["Title"],
                width=200
            ).grid(row=row, column=0, padx=10, pady=5)

            ctk.CTkLabel(
                self.reviews_table,
                text=book["avg_rating"],
                width=200
            ).grid(row=row, column=1, padx=10)

            ctk.CTkLabel(
                self.reviews_table,
                text=book["reviews_count"],
                width=200
            ).grid(row=row, column=2, padx=10)
