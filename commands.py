from vfs import VirtualFileSystem

def execute_ls(args, vfs):
    """
    Реализация команды ls - список файлов и папок
    """
    if not args:
        # ls без аргументов - показываем текущую директорию
        path = vfs.current_path
    else:
        # ls с путем - показываем указанную директорию
        path = args[0]
    
    # Получаем содержимое директории
    result = vfs.list_directory(path)
    
    if isinstance(result, str) and result.startswith("Error:"):
        return result  # Возвращаем ошибку
    
    # Форматируем вывод
    if not result:
        return "Directory is empty"
    
    return "  ".join(result)

def execute_cd(args, vfs):
    if not args:
        # cd без аргументов - переход в домашнюю директорию пользователя
        # Если домашней директории нет - остаемся в текущей
        home_dir = f"/home/{vfs.current_user}"
        home_node = vfs.get_node(home_dir)
        
        if home_node and home_node.type == 'directory':
            return vfs.change_directory(home_dir)
        else:
            # Если домашней директории нет, пробуем /home
            home_root = vfs.get_node("/home")
            if home_root and home_root.type == 'directory':
                return vfs.change_directory("/home")
            else:
                # Если /home тоже нет - остаемся где есть
                return f"Already in {vfs.current_path}"
    
    path = args[0]
    
    # Обработка cd ..
    if path == "..":
        return vfs.change_directory("..")
    
    # Обработка cd ~ (домашняя директория)
    if path == "~":
        home_dir = f"/home/{vfs.current_user}"
        home_node = vfs.get_node(home_dir)
        if home_node and home_node.type == 'directory':
            return vfs.change_directory(home_dir)
        else:
            return vfs.change_directory("/home")
    
    # Обработка cd - (предыдущая директория) - можно добавить позже
    if path == "-":
        return "Error: Previous directory tracking not implemented"
    
    # Обычный переход
    return vfs.change_directory(path)

def execute_pwd(args, vfs):
    return vfs.current_path

def execute_whoami(args, vfs):
    return vfs.current_user

def execute_uptime(args, vfs, emulator_state):
    uptime = emulator_state.get_uptime()
    return f"Emulator uptime: {uptime}"

def execute_du(args, vfs):
    if not args:
        path = vfs.current_path
    else:
        path = args[0]
    
    # Проверяем существование пути
    node = vfs.get_node(path)
    if not node:
        return f"Error: Path '{path}' not found"
    
    # Вычисляем размер
    size_bytes = vfs.calculate_directory_size(path)
    formatted_size = vfs.format_size(size_bytes)
    
    if node.type == 'file':
        return f"{formatted_size}\t{path}"
    else:
        return f"{formatted_size}\t{path}"
    
def execute_echo(args, vfs):

    if not args:
        return "" 
    
    # Объединяем все аргументы в одну строку
    output = ' '.join(args)

    return output

def execute_chmod(args, vfs):
    """
    Реализация команды chmod - изменение прав доступа
    """
    if len(args) < 2:
        return "Error: chmod requires permissions and path arguments\nUsage: chmod permissions path"
    
    permissions = args[0]
    path = args[1]
    
    # Валидация формата прав (упрощенная)
    if not is_valid_permissions(permissions):
        return f"Error: Invalid permissions format '{permissions}'. Use format like '755' or 'rwxr-xr-x'"
    
    # Находим узел
    node = vfs.get_node(path)
    if not node:
        return f"Error: Path '{path}' not found"
    
    # Меняем права
    result = vfs.change_permissions(path, permissions)
    if result.startswith("Error:"):
        return result
    
    return f"Permissions changed to {permissions} for {path}"

def is_valid_permissions(permissions):
    """
    Проверяет корректность формата прав доступа
    """
    # Проверяем числовой формат (755)
    if permissions.isdigit() and len(permissions) == 3:
        return all(0 <= int(digit) <= 7 for digit in permissions)
    
    # Проверяем символьный формат (rwxr-xr-x)
    if len(permissions) == 9 and all(c in 'rwx-' for c in permissions):
        return True
    
    return False

def execute_cp(args, vfs):
    """
    Реализация команды cp - копирование файлов/папок
    """
    if len(args) < 2:
        return "Error: cp requires source and destination arguments\nUsage: cp source destination"
    
    source_path = args[0]
    dest_path = args[1]
    
    # Проверяем существование источника
    source_node = vfs.get_node(source_path)
    if not source_node:
        return f"Error: Source path '{source_path}' not found"
    
    # Копируем
    result = vfs.copy_node(source_path, dest_path)
    if result.startswith("Error:"):
        return result
    
    return f"Copied '{source_path}' to '{dest_path}'"

def execute_vfs_load(args, vfs):
    """
    Реализация команды vfs-load - загрузка новой VFS
    """
    if len(args) < 1:
        return "Error: vfs-load requires a path argument\nUsage: vfs-load path/to/vfs.csv"
    
    csv_path = args[0]
    
    # Загружаем новую VFS
    try:
        vfs.load_from_csv(csv_path)
        return f"VFS loaded successfully from {csv_path}"
    except Exception as e:
        return f"Error loading VFS: {e}"