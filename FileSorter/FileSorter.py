import string
import os
import shutil


class FileSorter:
    def __init__(self):
        self.extensions = {
            # Audio
            ".mp3": "audio",
            ".wav": "audio",
            ".flac": "audio",
            ".aac": "audio",
            ".ogg": "audio",
            ".m4a": "audio",
            ".wma": "audio",
            # Video
            ".mp4": "video",
            ".mkv": "video",
            ".avi": "video",
            ".mov": "video",
            ".wmv": "video",
            ".flv": "video",
            ".webm": "video",
            # Images
            ".png": "image",
            ".jpg": "image",
            ".jpeg": "image",
            ".gif": "image",
            ".bmp": "image",
            ".tiff": "image",
            ".svg": "image",
            ".webp": "image",
            ".ico": "image",
            # Documents
            ".pdf": "document",
            ".doc": "document",
            ".docx": "document",
            ".xls": "document",
            ".xlsx": "document",
            ".ppt": "document",
            ".pptx": "document",
            ".txt": "document",
            ".rtf": "document",
            ".odt": "document",
            ".md": "document",
            # Code / Scripts
            ".py": "python",
            ".pyc": "python",
            ".ipynb": "python",
            ".cpp": "c++",
            ".cxx": "c++",
            ".c": "c",
            ".h": "c-header",
            ".hpp": "c++-header",
            ".java": "java",
            ".class": "java",
            ".js": "javascript",
            ".ts": "typescript",
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".php": "php",
            ".rb": "ruby",
            ".go": "go",
            ".sh": "shell",
            ".bat": "batch",
            ".pl": "perl",
            ".rs": "rust",
            # Executables
            ".exe": "executable",
            ".msi": "executable",
            ".apk": "executable",
            ".app": "executable",
            ".bin": "executable",
            ".deb": "executable",
            ".rpm": "executable",
            ".run": "executable",
            # Archives / Compressed
            ".zip": "archive",
            ".rar": "archive",
            ".7z": "archive",
            ".tar": "archive",
            ".gz": "archive",
            ".bz2": "archive",
            ".xz": "archive",
            ".iso": "archive",
            # Fonts
            ".ttf": "font",
            ".otf": "font",
            ".woff": "font",
            ".woff2": "font",
            # Data / Config
            ".json": "data",
            ".xml": "data",
            ".csv": "data",
            ".tsv": "data",
            ".yaml": "data",
            ".yml": "data",
            ".ini": "data",
            ".env": "data",
            ".log": "data",
            # Databases
            ".db": "database",
            ".sqlite": "database",
            ".sqlite3": "database",
            ".mdb": "database",
            ".accdb": "database",
            # Misc
            ".bak": "backup",
            ".tmp": "temporary",
            ".swp": "temporary",
        }

    def get_files(self):
        files = os.listdir()

        if files:
            for file in files:
                if file == os.path.basename(__file__):
                    continue
                if os.path.isfile(file):
                    _, ext = os.path.splitext(file)
                    catagory = self.extensions.get(ext.lower(), None)
                    if catagory:
                        if not (os.path.isdir(catagory)):
                            os.mkdir(catagory)
                        shutil.move(file, catagory)
                    else:
                        print(f"Skipped: {file} (unknown extension: '{ext}')")
        else:
            print("No files to be sorted.")


def main():
    sorter = FileSorter()
    sorter.get_files()


if __name__ == "__main__":
    main()
