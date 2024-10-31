import shutil
from datetime import datetime
from pathlib import Path

path = Path(r"")

file_type_folders = {
    "-=Images Folder=-": ["jpg", "jpeg", "png", "gif", "bmp", "tif", "jxr"],
    "-=Text Documents Folder=-": ["txt", "doc", "docx", "odt", "rtf"],
    "-=Cad_Plot Folder=-": ["plt", "dwg", "dxf"],
    "-=PDFs Folder=-": ["pdf"],
    "-=Ebooks Folder=-": ["epub", "mobi", "azw", "azw3", "ibooks", "fb2", "lit"],
    "-=Audio=-": ["mp3", "wav", "aac", "flac", "ogg", "wma", "alac", "aiff", "m4a", "opus"],
    "-=Video=-": ["mp4", "avi", "mov", "mkv", "flv", "wmv", "webm", "mpeg", "mpg", "m4v", "3gp", "asf"],
    "-=Archives=-": ["zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso", "cab", "tar.gz", "tar.bz2", "tar.xz", "z"],
}

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
