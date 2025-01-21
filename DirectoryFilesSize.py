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
            if len(self.errors) == 0:
                file_mode = 'w'
            else:
                file_mode = 'a'
            self.errors.append(traceback.format_exc())  
            with open("exceptions.log", file_mode) as logfile:
                traceback.print_exc(file=logfile)
            return []

    def size_files_in_directory(self, directory, max_depth = 10, current_depth = 0):
        dir_size = 0
        self.directory_sizes[directory] = (0, current_depth)
        for entry in self.scandir(directory):
                if entry.is_file():
                    dir_size += os.path.getsize(entry)
                elif entry.is_dir() and current_depth < max_depth:
                    subdir_size = self.size_files_in_directory(entry.path, max_depth, current_depth + 1)
                    self.directory_sizes[entry.path] = subdir_size
                    dir_size += subdir_size[0]
                elif entry.is_dir() and current_depth >= max_depth:
                    dir_size += self._size_files_in_directory(entry) 
        self.directory_sizes[directory] = (dir_size, current_depth)
        return (dir_size, current_depth)
    
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
    i = 0
    for dir_info in size_canculator.directory_sizes.items():
        dir_path = os.path.basename(dir_info[0])
        dir_size = human_readable_size(dir_info[1][0])
        if i == 0:
            print('')
        if dir_info[1][1] == 1 and i != 0:
            print('')
        prefix = '-' * dir_info[1][1]
        if prefix != '':
            prefix += ' '
        print(f"{prefix}{dir_path} {dir_size}") 
        i += 1
    if len(size_canculator.get_errors()) > 0:
        print('\nОбнаружены ошибки, посмотрите файл exceptions.log')
    #size_canculator.print_errors()
