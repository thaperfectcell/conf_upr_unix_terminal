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
    """
    Реализация команды cd - смена директории
    """
    if not args:
        # cd без аргументов - переход в домашнюю директорию
        return vfs.change_directory("/home")
    
    path = args[0]
    
    if path == "..":
        return vfs.change_directory("..")
    
    if path == "~":
        return vfs.change_directory("/home")
    
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