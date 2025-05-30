import os
import shutil
import threading
from tkinter import BOTH, Tk, Button, Label, filedialog, StringVar, ttk, Checkbutton, IntVar, Frame, messagebox, Listbox, Scrollbar, Toplevel, END

FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv', '.odt'],
    'Videos': ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv'],
    'Audio': ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.java', '.json', '.xml', '.php', '.sh'],
}

# this part organizes them into their different spacess like what u see belwo
def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return 'Others'

# orgAnizes it 
def organize_files(folder_path, progress_label):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        total_files = len(files)
        count = 0
        progress_label.set(f"Found {total_files} files to organize.")

        for file in files:
            ext = os.path.splitext(file)[1].lower()
            category = get_category(ext)
            category_path = os.path.join(folder_path, category)

            if not os.path.exists(category_path):
                os.makedirs(category_path)

            src = os.path.join(folder_path, file)
            dst = os.path.join(category_path, file)

            # this part handles the name conflicts for files and shi
            if os.path.exists(dst):
                base, ext = os.path.splitext(file)
                i = 1
                while os.path.exists(os.path.join(category_path, f"{base}_{i}{ext}")):
                    i += 1
                dst = os.path.join(category_path, f"{base}_{i}{ext}")

            shutil.move(src, dst)
            count += 1
            progress_label.set(f"Organizing... ({count}/{total_files})")

        progress_label.set("Organization complete!")

    except Exception as e:
        progress_label.set(f"Error: {str(e)}")


def start_organizing(progress_label):
    folder_path = filedialog.askdirectory()
    if folder_path:
        progress_label.set("Starting organization...")
        threading.Thread(target=organize_files, args=(folder_path, progress_label), daemon=True).start()

def log_error(message):
    print(f"[Error] {message}") 

#gui
def create_gui():
    root = Tk("THE File Organizer")
    root.geometry("400x300")
    root.title("File Organizer")
    root.resizable(False, False)
    root.configure(bg="#424040")

    progress_label = StringVar()
    progress_label.set("Select a folder to organize.")

    Label(root, text="File Organizer", font=("Helvetica", 16)).pack(pady=10)
    Button(root, text="Choose Folder and Organize", command=lambda: start_organizing(progress_label), width=30).pack(pady=10)
    Label(root, textvariable=progress_label, wraplength=380, justify="center").pack(pady=20)
    Button( root, text="Exit", command=root.destroy,bg="#b30000", fg="white", width=10).pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
