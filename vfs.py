class VFSNode:
    """
    Один узел в виртуальной файловой системе (файл или папка)
    """
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
        """
        Красивое строковое представление узла
        """
        if self.type == 'directory':
            return f"📁 {self.name}/"
        else:
            encoding_info = f" [{self.encoding}]" if self.encoding != 'text' else ""
            return f"📄 {self.name}{encoding_info}"

class VirtualFileSystem:
    def __init__(self):
        self.root = None          # корневая папка
        self.current_path = "/"   # текущий путь
        self.nodes = {}           # словарь {путь: узел}
    
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