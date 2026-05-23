# 📚 Smart Library System

A desktop application for managing a smart library system built with Python, CustomTkinter, and MySQL.

## ✨ Features

- 📊 **Dashboard** — View total books, members, and borrowed books
- 📕 **Borrow System** — Borrow books by member ID and book ID
- ⭐ **Reviews** — Add reviews and view top rated books
- 🔍 **Smart Search** — Search books by title, author, or genre

## 🛠️ Tech Stack

- Python 3
- CustomTkinter (Modern GUI)
- MySQL (Database)
- mysql-connector-python
- python-dotenv

## ⚙️ How to Run

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Create a `.env` file:
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=smartlibraryDB
4. Import the database:
   Run `sql/smartlibraryDB.sql` in MySQL Workbench
5. Run the app:
   python main.py

## 📁 Project Structure

smart_library/
├── main.py
├── ui/
│   └── app.py
├── logic/
│   └── library_logic.py
├── db/
│   └── database.py
└── sql/
    └── smartlibraryDB.sql
