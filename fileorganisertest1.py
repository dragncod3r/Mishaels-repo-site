import os
import shutil
import threading
from tkinter import BOTH, Tk, Button, Label, filedialog, StringVar, ttk, Checkbutton, IntVar, Frame, messagebox, Listbox, Scrollbar, Toplevel, END
import datetime

FILE_CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.tiff', '.webp'],
    'Documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.csv', '.odt'],
    'Videos': ['.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv'],
    'Audio': ['.mp3', '.wav', '.aac', '.ogg', '.flac', '.m4a'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Code': ['.py', '.js', '.html', '.css', '.cpp', '.c', '.java', '.json', '.xml', '.php', '.sh'],
}

# this part organizes them into their different spaces like what u see below
def get_category(extension):
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return 'Others'

# this part shows the preview of the files before organizing them what they are and where they will go 
def organize_files(folder_path, progress_label, sort_by_date_var):
    try:
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        total_files = len(files)
        count = 0
        progress_label.set(f"Found {total_files} files to organize.")
        
        sort_by_date = sort_by_date_var.get() == 1 # Check if the checkbox is ticked

        #looking for all the files in the folder and then organizing them
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            category = get_category(ext)
            
            # Determine the base path for the file (Category or Category/Year/Month)
            current_category_path = os.path.join(folder_path, category)
            
            if sort_by_date:
                try:
                    # Get the creation date of the file
                    file_path = os.path.join(folder_path, file)
                    creation_timestamp = os.path.getctime(file_path)
                    creation_date = datetime.datetime.fromtimestamp(creation_timestamp)
                    year_folder = str(creation_date.year)
                    month_folder = creation_date.strftime("%B") # Full month name
                    
                    category_path = os.path.join(current_category_path, year_folder, month_folder)
                except Exception as date_e:
                    log_error(f"Could not get creation date for {file}: {date_e}. Placing in category folder.")
                    category_path = current_category_path
            else:
                category_path = current_category_path
            
            # create the category/year/month folder if it doesn't exist
            if not os.path.exists(category_path):
                os.makedirs(category_path)
            
            # move the file to the appropriate category folder
            src = os.path.join(folder_path, file)
            dst = os.path.join(category_path, file)

            # this part handles the name conflicts for files and ensures unique names
            if os.path.exists(dst):
                base, ext = os.path.splitext(file)
                i = 1
                while os.path.exists(os.path.join(category_path, f"{base}_{i}{ext}")):
                    i += 1
                dst = os.path.join(category_path, f"{base}_{i}{ext}")
            
            # move the file
            shutil.move(src, dst)
            count += 1
            progress_label.set(f"Organizing... ({count}/{total_files})")
        
        # just a little message to show that the organization is complete nothing special
        progress_label.set("Organization complete!")

    except Exception as e:
        progress_label.set(f"Error: {str(e)}")
        log_error(f"Organization error: {e}")

# this part starts the organizing process and handles the folder selection
def start_organizing_thread(progress_label, sort_by_date_var):
    folder_path = filedialog.askdirectory()
    if folder_path:
        progress_label.set("Starting organization...")
        threading.Thread(target=organize_files, args=(folder_path, progress_label, sort_by_date_var), daemon=True).start()

def log_error(message):
    print(f"[Error] {message}") 

#gui
def create_gui():
    root = Tk()
    root.geometry("400x350") 
    root.title("File Organizer")
    root.resizable(False, False)
    root.configure(bg="#711883")

    progress_label = StringVar()
    progress_label.set("Select a folder to organize.")

    sort_by_date_var = IntVar() 

    Label(root, text="File Organizer", font=("Helvetica", 16)).pack(pady=10)
    
    # Checkbutton for sorting by date
    Checkbutton(root, text="Sort by Date (Year/Month subfolders)", variable=sort_by_date_var, bg="#FFFFFF").pack(pady=5)
    
    Button(root, text="Choose Folder and Organize", command=lambda: start_organizing_thread(progress_label, sort_by_date_var), width=30).pack(pady=10)
    Label(root, textvariable=progress_label, wraplength=380, justify="center").pack(pady=20)
    Button(root, text="Exit", command=root.destroy, bg="#b30000", fg="white", width=10).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
