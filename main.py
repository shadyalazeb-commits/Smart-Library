print("✅ main.py started")
from ui.app import SmartLibraryApp
if __name__ == "__main__":
    print("✅ creating app")
    app = SmartLibraryApp()
    print("✅ entering mainloop")
    app.mainloop()