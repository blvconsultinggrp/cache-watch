import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import stat

class FolderSizeHandler(FileSystemEventHandler):
    def __init__(self, folder_path, exempt_filename, max_size):
        self.folder_path = folder_path
        self.exempt_filename = exempt_filename
        self.max_size = max_size
        self.lock = threading.Lock()
        self.check_folder_size()

    def on_any_event(self, event):
        self.check_folder_size()

    def get_folder_size(self):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(self.folder_path):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except FileNotFoundError:
                    print(f"File not found: {filepath}")
                except Exception as e:
                    print(f"Error getting size for file '{filepath}': {e}")
        return total_size

    def delete_folder(self, folder_path):
        try:
            # Change permissions to ensure the folder can be deleted
            for root, dirs, files in os.walk(folder_path):
                for dir in dirs:
                    os.chmod(os.path.join(root, dir), stat.S_IRWXU)
                for file in files:
                    os.chmod(os.path.join(root, file), stat.S_IRWXU)
            shutil.rmtree(folder_path)
            print(f"Folder '{folder_path}' has been deleted.")
        except PermissionError:
            print(f"Permission denied when deleting folder '{folder_path}'. Skipping...")
        except Exception as e:
            print(f"Error deleting folder '{folder_path}': {e}. Skipping...")

    def clear_folders_in_directory(self):
        try:
            folders_to_delete = []
            for item in os.listdir(self.folder_path):
                item_path = os.path.join(self.folder_path, item)
                if os.path.isdir(item_path):
                    folders_to_delete.append(item_path)
                elif os.path.isfile(item_path) and item != self.exempt_filename:
                    print(f"File '{item_path}' is exempt and has not been deleted.")

            with ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(self.delete_folder, folder) for folder in folders_to_delete]
                for future in as_completed(futures):
                    try:
                        future.result()  # Raise exception if occurred
                    except Exception as e:
                        print(f"Error occurred during deletion: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def check_folder_size(self):
        with self.lock:
            folder_size = self.get_folder_size()
            print(f"Current folder size: {folder_size} bytes")
            if folder_size > self.max_size:
                print("Folder size exceeded limit. Clearing folders...")
                self.clear_folders_in_directory()

def monitor_folder(folder_path, exempt_filename, max_size, check_interval=60):
    event_handler = FolderSizeHandler(folder_path, exempt_filename, max_size)
    observer = Observer()
    observer.schedule(event_handler, folder_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(check_interval)
            event_handler.check_folder_size()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Example usage
folder_path = r'C:\.ADSPOWER_GLOBAL\cache'  # Replace with your folder path
exempt_filename = 'cache_time'  # File that should not be deleted
max_size = 200 * 1024 * 1024 * 1024  # 1 MB in bytes
check_interval = 60  # Interval to check folder size in seconds

monitor_folder(folder_path, exempt_filename, max_size, check_interval)
