class VFSNode:
    def __init__(self, node_type, path, name, content, encoding, permissions):
        self.type = node_type      # 'file' или 'directory'
        self.path = path          # полный путь: '/home/user'
        self.name = name          # имя: 'user'
        self.content = content    # содержимое файла (уже декодированное)
        self.encoding = encoding  # 'text' или 'base64' (НОВОЕ!)
        self.permissions = permissions  # 'rwxr-xr-x'
        self.children = []        # список дочерних узлов (для папок)
        self.parent = None        # ссылка на родительский узел
    
    def __str__(self):
        if self.type == 'directory':
            return f"{self.name}/"
        else:
            encoding_info = f" [{self.encoding}]" if self.encoding != 'text' else ""
            return f"{self.name}{encoding_info}"

class VirtualFileSystem:
    def __init__(self):
        self.root = None          # корневая папка
        self.current_path = "/"   # текущий путь
        self.current_directory = None
        self.nodes = {}           # словарь {путь: узел}
        self.current_user = "virtual_user"

    def load_from_csv(self, csv_path):
        try:
            import csv
            import base64  
            
            print(f"Loading VFS from: {csv_path}")
            self.nodes = {}
            
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Сначала создаем все узлы
                for row in reader:
                    # Обрабатываем кодировку
                    content = row['content']
                    encoding = row.get('encoding', 'text')  # по умолчанию 'text'
                    
                    if encoding == 'base64' and content:
                        try:
                            # Декодируем из Base64 в байты, затем в строку
                            decoded_bytes = base64.b64decode(content)
                            content = decoded_bytes.decode('utf-8')
                        except Exception as e:
                            print(f"Warning: Failed to decode Base64 for {row['path']}: {e}")
                            content = "[Base64 decoding error]"
                    
                    node = VFSNode(
                        node_type=row['type'],
                        path=row['path'],
                        name=row['name'],
                        content=content,
                        encoding=encoding,
                        permissions=row['permissions']
                    )
                    self.nodes[node.path] = node
                
                self._build_tree()
                
                # Устанавливаем корень и текущую директорию
                self.root = self.nodes.get('/')
                if self.root:
                    self.current_directory = self.root
                    print("VFS loaded successfully!")
                else:
                    print("Error: Root directory not found in CSV")
                    
        except FileNotFoundError:
            print(f"Error: VFS file '{csv_path}' not found")
        except Exception as e:
            print(f"Error loading VFS: {e}")
    
    def _build_tree(self):
        """
        Строит древовидную структуру из узлов
        """
        for path, node in self.nodes.items():
            if path == '/':  # корневой узел не имеет родителя
                continue
            
            # Находим родительскую директорию
            parent_path = '/'.join(path.split('/')[:-1]) or '/'
            parent_node = self.nodes.get(parent_path)
            
            if parent_node and parent_node.type == 'directory':
                parent_node.children.append(node)
                node.parent = parent_node
    
    def get_node(self, path):
        # Если путь относительный - делаем абсолютным
        if not path.startswith('/'):
            path = self.current_path + '/' + path if self.current_path != '/' else '/' + path
            path = path.replace('//', '/')
        
        return self.nodes.get(path)
    
    def is_directory(self, path):
        node = self.get_node(path)
        return node and node.type == 'directory'
    
    def list_directory(self, path=None):
        if path is None:
            path = self.current_path
        
        node = self.get_node(path)
        if not node:
            return f"Error: Directory '{path}' not found"
        if node.type != 'directory':
            return f"Error: '{path}' is not a directory"
        
        return [child.name for child in node.children]
    
    def change_directory(self, path):
        # Обработка cd ..
        if path == "..":
            if self.current_path == "/":
                return "Error: Already at root directory"
            
            parent_path = '/'.join(self.current_path.split('/')[:-1]) or '/'
            node = self.get_node(parent_path)
            
            if node and node.type == 'directory':
                self.current_path = parent_path
                self.current_directory = node
                return f"Changed directory to {self.current_path}"
            else:
                return "Error: Parent directory not found"
        
        if path.startswith('/'):
            target_path = path
        else:
            if self.current_path == '/':
                target_path = '/' + path
            else:
                target_path = self.current_path + '/' + path
        
        # Нормализуем путь (убираем двойные слеши)
        target_path = target_path.replace('//', '/')
        
        node = self.get_node(target_path)
        
        if not node:
            return f"Error: Directory '{path}' not found"
        
        if node.type != 'directory':
            return f"Error: '{path}' is not a directory"
        
        # Меняем текущую директорию
        self.current_path = target_path
        self.current_directory = node
        return f"Changed directory to {self.current_path}"

    def list_directory(self, path=None):
        if path is None:
            path = self.current_path
        
        node = self.get_node(path)
        if not node:
            return f"Error: Directory '{path}' not found"
        
        if node.type != 'directory':
            return f"Error: '{path}' is not a directory"
        
        # Возвращаем только имена дочерних элементов
        return [child.name for child in node.children]
    
    def calculate_directory_size(self, path=None):
        if path is None:
            path = self.current_path
        
        node = self.get_node(path)
        if not node:
            return 0
        
        total_size = 0
        
        if node.type == 'file':
            # Для файла считаем длину содержимого + служебная информация
            content_size = len(node.content) if node.content else 0
            return content_size + 100  # +100 байт на метаданные
        
        elif node.type == 'directory':
            # Для директории рекурсивно считаем размер всех детей
            for child in node.children:
                total_size += self.calculate_directory_size(child.path)
            return total_size + 50  # +50 байт на метаданные директории

    def format_size(self, size_bytes):
        """
        Форматирует размер в читаемом виде
        """
        if size_bytes >= 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        elif size_bytes >= 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes} bytes"