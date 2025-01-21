import os
import time
import math
import traceback

def human_readable_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

class DirectorySizeCalculator:
    def __init__(self):
        self.directory_sizes = {}
        self.errors = []

    def scandir(self, directory):
        try:
            return os.scandir(directory)
        except Exception as error:
            self.errors.append(traceback.format_exc())  
            with open("exceptions.log", "w") as logfile:
                traceback.print_exc(file=logfile)
            return []

    def size_files_in_directory(self, directory, max_depth = 10, current_depth = 0):
        dir_size = 0
        self.directory_sizes[directory] = 0
        try:
            os.access(directory, os.R_OK)
        except Exception as error:
            self.errors.append(traceback.format_exc())
        for entry in self.scandir(directory):
                if entry.is_file():
                    dir_size += os.path.getsize(entry)
                elif entry.is_dir() and current_depth < max_depth:
                    subdir_size = self.size_files_in_directory(entry.path, max_depth, current_depth + 1)
                    self.directory_sizes[entry.path] = subdir_size
                    dir_size += subdir_size
                elif entry.is_dir() and current_depth >= max_depth:
                    dir_size += self._size_files_in_directory(entry)   
        self.directory_sizes[directory] = dir_size
        return dir_size
    
    def _size_files_in_directory(self, directory):
        dir_size = 0
        for entry in self.scandir(directory):
            if entry.is_file():
                dir_size += os.path.getsize(entry)
            elif entry.is_dir():
                dir_size += self._size_files_in_directory(entry.path)
        return dir_size
    
    def get_errors(self):
        return self.errors
    
    def print_errors(self):
        for error in self.errors:
            print(error)

# Использование класса
if __name__ == "__main__":
    size_canculator = DirectorySizeCalculator()
    directory_path = input('Путь к каталогу: ').strip()  # Укажите путь к вашему каталогу
    max_depth = input('Максимальная вложенность: ')
    size_canculator.size_files_in_directory(directory_path, int(max_depth))
    
    for dir_path, dir_size in size_canculator.directory_sizes.items():
        dir_size = human_readable_size(dir_size)
        print(f"{dir_path} {dir_size}") 
    if len(size_canculator.get_errors()) > 0:
        print('Обнаружены ошибки, посмотрите файл exceptions.log')
    #size_canculator.print_errors()
