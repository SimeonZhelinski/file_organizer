import shutil
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

file_type_folders = {
    "-=Images Folder=-": ["jpg", "jpeg", "png", "gif", "bmp", "tif", "jxr"],
    "-=Text Documents Folder=-": ["txt", "doc", "docx", "odt", "rtf"],
    "-=Presentations Folder": [".ppt", ".pptx", ".odp", ".pps", ".ppsx", ".pot", ".potx"],
    "-=Cad_Plot Folder=-": ["plt", "dwg", "dxf"],
    "-=PDFs Folder=-": ["pdf"],
    "-=Ebooks Folder=-": ["epub", "mobi", "azw", "azw3", "ibooks", "fb2", "lit"],
    "-=Audio=-": ["mp3", "wav", "aac", "flac", "ogg", "wma", "alac", "aiff", "m4a", "opus"],
    "-=Video=-": ["mp4", "avi", "mov", "mkv", "flv", "wmv", "webm", "mpeg", "mpg", "m4v", "3gp", "asf"],
    "-=Archives=-": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso", "cab", "tar.gz", "tar.bz2", "tar.xz", "z"],
}

processed_files = []


def organize_files(directory_path):
    path = Path(directory_path)
    processed_files.clear()
    text_box.delete("1.0", tk.END)
    files_count = 0

    for file in path.iterdir():
        if file.is_file():
            if file.suffix.lower() == '.lnk':
                continue

            file_name = file.name
            extension = file_name.split(".")[-1].lower()

            folder_name = None
            for folder, extensions in file_type_folders.items():
                if extension in extensions:
                    folder_name = folder
                    break

            if not folder_name:
                folder_name = f"-={extension}=- folder"

            file_time_last_mod = datetime.fromtimestamp(file.stat().st_mtime)
            year_month_folder = f"{file_time_last_mod.year}-{file_time_last_mod.month:02d}"
            target_folder = path / folder_name / year_month_folder

            if not target_folder.exists():
                target_folder.mkdir(parents=True, exist_ok=True)

            shutil.move(str(file), str(target_folder / file_name))
            processed_files.append(file_name)
            text_box.config(state=tk.NORMAL)
            text_box.insert(tk.END, f"Processed: {file_name}\n")
            text_box.see(tk.END)
            text_box.config(state=tk.DISABLED)
            files_count = len(processed_files)

    messagebox.showinfo("Success", f"{files_count} files organized successfully!")


def save_processed_files():
    if not processed_files:
        messagebox.showwarning("Warning", "No files processed yet!")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if save_path:
        with open(save_path, "w") as f:
            f.write(f"Processed Files List:\n")
            f.write("\n".join(processed_files))
        messagebox.showinfo("Saved", f"Processed files saved to {save_path}")


def browse_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, directory_path)


def start_organization():
    directory_path = path_entry.get()
    if directory_path:
        organize_files(directory_path)
    else:
        messagebox.showwarning("Warning", "Please select a directory first!")


def exit_program():
    app.quit()


app = tk.Tk()
app.title("File Organizer")
app.geometry("320x350")

label = tk.Label(app, text="Select a folder to organize:", font=("Arial", 12))
label.grid(row=0, column=0, padx=10, pady=10)
frame = tk.Frame(app)
frame.grid(row=1, column=0, padx=10, pady=5)
path_entry = tk.Entry(frame, width=30, font=("Arial", 10))
path_entry.pack(side=tk.LEFT, padx=5)
button_browse = tk.Button(frame, text="Browse", command=browse_directory, font=("Arial", 10), bg="lightblue")
button_browse.pack(side=tk.LEFT)
button_exit = tk.Button(app, text="Exit", command=exit_program, font=("Arial", 12), bg="lightcoral", width=10)
button_exit.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
button_start = tk.Button(app, text="Start", command=start_organization, font=("Arial", 12), bg="lightgreen", width=10)
button_start.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
text_box = scrolledtext.ScrolledText(app, width=40, height=10, font=("Arial", 10))
text_box.grid(row=3, column=0, padx=10, pady=10)
button_save = tk.Button(app, text="Save Processed Files List", command=save_processed_files, font=("Arial", 10),
                        bg="lightblue")
button_save.grid(row=4, column=0, pady=5)

app.mainloop()
