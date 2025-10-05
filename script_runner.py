def execute_script_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        commands = []
        for line in lines:
            # Убираем пробелы в начале и конце строки
            clean_line = line.strip()
            
            # Пропускаем пустые строки и комментарии
            if not clean_line or clean_line.startswith('#'):
                continue
                
            commands.append(clean_line)
        
        return commands
        
    except FileNotFoundError:
        print(f"Error: Script file '{file_path}' not found")
        return []
    except Exception as e:
        print(f"Error reading script: {e}")
        return []