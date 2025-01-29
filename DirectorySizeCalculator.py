import os
import time
import math
import traceback
import pathlib
import argparse
import sys
import pprint
import textwrap
import mimetypes

def human_readable_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

source_code_extensions = [
    # Python
    ".py", ".pyi",
    
    # JavaScript/TypeScript
    ".js", ".mjs", ".cjs", ".ts", ".tsx",
    
    # Java
    ".java",
    
    # C/C++
    ".c", ".cpp", ".cxx", ".cc", ".h", ".hpp", ".hxx",
    
    # C#
    ".cs",
    
    # Ruby
    ".rb", ".erb",
    
    # PHP
    ".php", ".phtml",
    
    # Go
    ".go",
    
    # Rust
    ".rs",
    
    # Swift
    ".swift",
    
    # Kotlin
    ".kt", ".kts",
    
    # Dart
    ".dart",

    # Shell Scripting
    ".sh", ".bash", ".zsh",
    
    # Perl
    ".pl", ".pm",
    
    # R
    ".R", ".Rmd",
    
    # MATLAB
    ".m",

    # Assembly
    ".asm", ".s",
    
    # Haskell
    ".hs",
    
    # Scala
    ".scala",
    
    # Elixir
    ".ex", ".exs",
    
    # Erlang
    ".erl", ".hrl",
    
    # Lua
    ".lua",
    
    # D
    ".d",
    
    # F#
    ".fs", ".fsx",
    
    # Objective-C
    ".m", ".mm",
    
    # Groovy
    ".groovy",
    
    # VBA/VB.NET
    ".bas", ".vb",
    
    # PowerShell
    ".ps1",
]

excecutable_extensions = [
    ".exe", ".dll", ".so", ".bin", ".app", ".dmg", ".elf", ".o", ".obj", ".class", ".jar", ".pyc", ".pyd", ".wasm"
]
class DirectorySizeCalculator:
    def __init__(self):
        self.directory_sizes = {}
        self.directory_sizes_detail = {} 
        self.errors = []
    
    # Метод для сканирования директории
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

    # Метод для добавления деталей о файле в словарь directory_sizes_detail
    def add_detail(self, directory, filepath, filesize = False):
        if filesize == False:
            filesize = os.path.getsize(filepath) 
        file_suffix = pathlib.Path(filepath).suffix.lower()
         # Инициализация структуры данных для директории, если её ещё нет
        if directory not in self.directory_sizes_detail:
            self.directory_sizes_detail[directory] = {}
        # Инициализация секции 'type', если её ещё нет
        if 'type' not in self.directory_sizes_detail[directory]:
            self.directory_sizes_detail[directory]['type'] = {} 
        # Инициализация секции 'mimetype', если её ещё нет
        if 'mimetype' not in self.directory_sizes_detail[directory]:
            self.directory_sizes_detail[directory]['mimetype'] = {} 
        # Инициализация секции 'ext', если её ещё нет
        if 'ext' not in self.directory_sizes_detail[directory]:
            self.directory_sizes_detail[directory]['ext'] = {}
        # Классификация файлов по их расширениям
        if file_suffix not in self.directory_sizes_detail[directory]['ext']:
            self.directory_sizes_detail[directory]['ext'][file_suffix] = 0
        self.directory_sizes_detail[directory]['ext'][file_suffix] += filesize
        # Классификация файлов по типам (видео, изображения, документы и т.д.)
        if file_suffix in ['.mp4', '.webm', '.avi', '.mkv', '.mov', '.ogg', '.wmv']:
            if 'video' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['video'] = 0
            self.directory_sizes_detail[directory]['type']['video'] += filesize
        elif file_suffix in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp', '.tiff', '.tif']:
            if 'image' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['image'] = 0
            self.directory_sizes_detail[directory]['type']['image'] += filesize
        elif file_suffix in ['.txt', '.odt', '.ods', '.odp', '.html', 
                             '.css', '.pdf', '.mhtml', '.xml', '.json', '.docx', '.djvu', '.djv',
                             '.xls', '.xlsx', '.ppt', '.pptx', '.xml', '.md', '.markdown', '.yaml', '.yml']:
            if 'doc' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['doc'] = 0
            self.directory_sizes_detail[directory]['type']['doc'] += filesize
        elif file_suffix in source_code_extensions:
            if 'source code' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['source code'] = 0
            self.directory_sizes_detail[directory]['type']['source code'] += filesize
        elif file_suffix in excecutable_extensions:
            if 'executable' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['executable'] = 0
            self.directory_sizes_detail[directory]['type']['executable'] += filesize
        elif file_suffix in ['.iso', '.img']:
            if 'disk image' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['disk image'] = 0
            self.directory_sizes_detail[directory]['type']['disk image'] += filesize
        elif file_suffix in ['.vhd', '.vhdx', '.vmdk']:
            if 'virtual machine image' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['virtual machine image'] = 0
            self.directory_sizes_detail[directory]['type']['virtual machine image'] += filesize
        elif file_suffix in ['.db', '.mdb', '.sqlite', '.sql']:
            if 'database' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['database'] = 0
            self.directory_sizes_detail[directory]['type']['database'] += filesize
        elif file_suffix in ['.mp3', '.flac', '.m4a', '.wav', '.ogg']:
            if 'audio' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['audio'] = 0
            self.directory_sizes_detail[directory]['type']['audio'] += filesize
        elif file_suffix in ['.srt', '.ass', '.vtt']:
            if 'sub' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['sub'] = 0
            self.directory_sizes_detail[directory]['type']['sub'] += filesize
        elif file_suffix in ['.zip', '.rar', '.gzip', '.gz', '.tar', '.7z']:
            if 'archive' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['archive'] = 0
            self.directory_sizes_detail[directory]['type']['archive'] += filesize
        else:
            if 'undefined' not in self.directory_sizes_detail[directory]['type']:
                self.directory_sizes_detail[directory]['type']['undefined'] = 0
            self.directory_sizes_detail[directory]['type']['undefined'] += filesize
        # Классификация файлов по их MIME-типам
        file_mimetype = mimetypes.guess_type(filepath)[0]
        if file_mimetype == None:
            file_mimetype = 'undefined'
        if file_mimetype not in self.directory_sizes_detail[directory]['mimetype']:
            self.directory_sizes_detail[directory]['mimetype'][file_mimetype] = 0
        self.directory_sizes_detail[directory]['mimetype'][file_mimetype] += filesize

    # Рекурсивный метод для вычисления размера файлов в директории с учётом глубины
    def size_files_in_directory(self, directory, max_depth = 10, current_depth = 0):
        dir_size = 0
        if current_depth < max_depth:
            self.directory_sizes[directory] = (0, current_depth) # Инициализация записи для директории
        for entry in self.scandir(directory):
            if entry.is_file():
                filesize = os.path.getsize(entry)
                dir_size += filesize
                self.add_detail(directory, entry.path, filesize)
            elif entry.is_dir():
                subdir_size = self.size_files_in_directory(entry.path, max_depth, current_depth + 1)
                if current_depth < max_depth:
                    self.directory_sizes[entry.path] = subdir_size
                dir_size += subdir_size[0]
                if entry.path in self.directory_sizes_detail:
                    if directory not in self.directory_sizes_detail:
                        self.directory_sizes_detail[directory] = {}
                        self.directory_sizes_detail[directory]['type'] = {}
                        self.directory_sizes_detail[directory]['ext'] = {}
                        self.directory_sizes_detail[directory]['mimetype'] = {}
                    for entry_size_detail_type, entry_size_detail_value in self.directory_sizes_detail[entry.path]['type'].items():
                        if entry_size_detail_type not in self.directory_sizes_detail[directory]['type']:
                            self.directory_sizes_detail[directory]['type'][entry_size_detail_type] = 0
                        self.directory_sizes_detail[directory]['type'][entry_size_detail_type] += entry_size_detail_value
                    for entry_size_detail_ext, entry_size_detail_value in self.directory_sizes_detail[entry.path]['ext'].items():
                        if entry_size_detail_ext not in self.directory_sizes_detail[directory]['ext']:
                            self.directory_sizes_detail[directory]['ext'][entry_size_detail_ext] = 0
                        self.directory_sizes_detail[directory]['ext'][entry_size_detail_ext] += entry_size_detail_value
                    for entry_size_detail_mimetype, entry_size_detail_value in self.directory_sizes_detail[entry.path]['mimetype'].items():
                        if entry_size_detail_mimetype not in self.directory_sizes_detail[directory]['mimetype']:
                            self.directory_sizes_detail[directory]['mimetype'][entry_size_detail_mimetype] = 0
                        self.directory_sizes_detail[directory]['mimetype'][entry_size_detail_mimetype] += entry_size_detail_value
        if current_depth < max_depth:
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

    def find_root(self):
        root_path = max(self.directory_sizes.keys(), key=lambda x: self.directory_sizes[x][0])  # Находим путь с максимальным размером
        root_size, root_level = self.directory_sizes[root_path]
        return root_path

    # Функция для создания вложенной структуры
    def build_nested_structure(self):
        # Создаем корневой элемент
        root_path = self.find_root()
        self.root_path = root_path
        root_name_len = len(root_path)
        root = {"name": os.path.basename(root_path), "size": self.directory_sizes[root_path][0], "detail": self.directory_sizes_detail[root_path], "children": []}
        # Вспомогательная функция для добавления элементов в структуру
        def add_to_structure(parent, path_parts, size, level):
            if level >= len(path_parts):
                return
            current_name = path_parts[level]
            
            # Ищем, есть ли уже такой элемент в текущем уровне
            for child in parent["children"]:
                if child["name"] == current_name:
                    add_to_structure(child, path_parts, size, level + 1)
                    return
            
            # Если элемент не найден, создаем новый
            new_child = {"name": current_name, "size": size, "detail": self.get_directory_sizes_detail(self.root_path + '/' + '/'.join(path_parts)), "children": []}
            parent["children"].append(new_child)
            add_to_structure(new_child, path_parts, size, level + 1)
        
        # Обрабатываем каждый элемент в данных
        for path, (size, level) in self.directory_sizes.items():
            if level == 0:
                continue  # Корневой элемент уже создан
            path = path[root_name_len + 1:]
            path_parts = path.split('/')
            add_to_structure(root, path_parts, size, 0)
        
        self.directory_sizes = root

    def get_directory_sizes_detail(self, path):
        if path not in self.directory_sizes_detail:
            return {'type': {}, 'ext' : {}, 'mimetype': {}}
        return self.directory_sizes_detail[path]
            
    def sort_by_size(self, node, reverse=True):
        if isinstance(node, dict) and "children" in node:
            node["children"].sort(key=lambda x: x["size"], reverse=reverse)
            for child in node["children"]:
                self.sort_by_size(child, reverse=reverse)
        else:
            print("Ошибка: Некорректная структура данных!")

    def sort_by_name(self, node, reverse=False):
        if isinstance(node, dict) and "children" in node:
            node["children"].sort(key=lambda x: x["name"], reverse=reverse)
            for child in node["children"]:
                self.sort_by_name(child, reverse=reverse)
        else:
            print("Ошибка: Некорректная структура данных!")

def print_node(node, parent = '', level = 0, detail = False, detail_ext = False, detail_mimetype = False):
    size = human_readable_size(int(node['size']))
    interface_width = 100
    if level == 0:
        print('-' * (level * 3) + '-' * (100 - (level * 3)))
    #print(' ' * (level * 3) + '-' * (100 - (level * 3)))
    node_name = ' ' * (level * 3) + node['name']
    node_name = textwrap.fill(node_name, interface_width, replace_whitespace = False)
    node_name = node_name.split('\n')
    i = 0
    for node_name_part in node_name:
        if i != 0:
            print(' ' * (level * 3), end="")
        print(node_name_part, end="")
        print('')
        i += 1
    print(' ' * (level * 3), end="")
    print(size)
    if detail == True: 
        i_file_type_size = 0
        print_file_type_size = []
        node['detail']['type'] = dict(sorted(node['detail']['type'].items()))
        for file_type, file_type_size in node['detail']['type'].items():
            if file_type_size > 0:
                print_file_type_size.append(str(file_type) + ':' + str(human_readable_size(file_type_size)),)
            i_file_type_size += 1
        if i_file_type_size > 0:
            detail_output = ', '.join(print_file_type_size)
            detail_output = textwrap.fill(detail_output, interface_width - (level * 3), replace_whitespace = False)
            detail_output = detail_output.split('\n')
            i = 0
            for detail_output_part in detail_output:
                if i != 0:
                    print('', end="")
                print(' ' * (level * 3), end="")
                print(detail_output_part, end="")
                print('')
                i += 1
    if detail_ext == True: 
        i_file_ext_size = 0
        print_file_ext_size = []
        node['detail']['ext'] = dict(sorted(node['detail']['ext'].items()))
        for file_ext, file_ext_size in node['detail']['ext'].items():
            if file_ext_size > 0:
                print_file_ext_size.append(str(file_ext) + ':' + str(human_readable_size(file_ext_size)),)
            i_file_ext_size += 1
        if i_file_ext_size > 0:
            detail_ext_output = ', '.join(print_file_ext_size)
            detail_ext_output = textwrap.fill(detail_ext_output, interface_width - (level * 3), replace_whitespace = False)
            detail_ext_output = detail_ext_output.split('\n')
            i = 0
            for detail_ext_output_part in detail_ext_output:
                if i != 0:
                    print('', end="")
                print(' ' * (level * 3), end="")
                print(detail_ext_output_part, end="")
                print(' ' * (interface_width - len(detail_ext_output_part)), end="")
                print('')
                i += 1
    if detail_mimetype == True: 
        i_file_mimetype_size = 0
        print_file_mimetype_size = []
        node['detail']['mimetype'] = dict(sorted(node['detail']['mimetype'].items()))
        for file_mimetype, file_mimetype_size in node['detail']['mimetype'].items():
            if file_mimetype_size > 0:
                print_file_mimetype_size.append(str(file_mimetype) + ':' + str(human_readable_size(file_mimetype_size)),)
            i_file_mimetype_size += 1
        if i_file_mimetype_size > 0:
            detail_mimetype_output = ', '.join(print_file_mimetype_size)
            detail_mimetype_output = textwrap.fill(detail_mimetype_output, interface_width - (level * 3), replace_whitespace = False)
            detail_mimetype_output = detail_mimetype_output.split('\n')
            i = 0
            for detail_mimetype_output_part in detail_mimetype_output:
                if i != 0:
                    print('', end="")
                print(' ' * (level * 3), end="")
                print(detail_mimetype_output_part, end="")
                print(' ' * (interface_width - len(detail_mimetype_output_part)), end="")
                print('')
                i += 1    
    last_index = len(node['children']) - 1
    #if level == 0:
    print('-' * (level * 3) + '-' * (100 - (level * 3)))
    for i, children in enumerate(node['children']):
        #if i == last_index:
            #print(' ' * (level * 3) + '-' * (100 - (level * 3)))
        if level == 0:
            print_node(children, '', level + 1, detail, detail_ext, detail_mimetype)
        else:
            print_node(children, ' ' * (level * 3), level + 1, detail, detail_ext, detail_mimetype)
        #print(' ' * (level * 3) + '-' * (100 - (level * 3)))
    
# Использование класса
if __name__ == "__main__":
    parser = argparse.ArgumentParser("python " + sys.argv[0], formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-d", "--detail", help='Указывать размер файлов по типу', type=str, choices=["Y", "N"], default="N")  
    parser.add_argument("-de", "--detail-ext", help='Указывать размер файлов по расширению', type=str, choices=["Y", "N"], default="N")
    parser.add_argument("-dm", "--detail-mimetype", help='Указывать размер файлов по mimetype', type=str, choices=["Y", "N"], default="N")
    parser.add_argument("-s", "--sort", help='Сортировка', type=str, choices=["name", "size"], default="name")  
    args = parser.parse_args()
    size_canculator = DirectorySizeCalculator()
    input_directory_path = input('Путь к каталогу: ').strip()  # Укажите путь к вашему каталогу
    input_max_depth = input('Максимальная вложенность: ')
    if input_directory_path.endswith('/'):
        input_directory_path = input_directory_path[:-1]
    size_canculator.size_files_in_directory(input_directory_path, int(input_max_depth))
    size_canculator.build_nested_structure()
    if args.sort == 'size':
        size_canculator.sort_by_size(size_canculator.directory_sizes)
    else:
        size_canculator.sort_by_name(size_canculator.directory_sizes)
    if args.detail == 'Y':
        detail = True
    else:
        detail = False
    if args.detail_ext == 'Y':
        detail_ext = True
    else:
        detail_ext = False
    if args.detail_mimetype == 'Y':
        detail_mimetype = True
    else:
        detail_mimetype = False
    print_node(size_canculator.directory_sizes, '', 0, detail, detail_ext, detail_mimetype)
    if len(size_canculator.get_errors()) > 0:
        print('\nОбнаружены ошибки, посмотрите файл exceptions.log')
    #size_canculator.print_errors()
