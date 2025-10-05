import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Emulator CLI')
    
    # Добавляем аргументы
    parser.add_argument('--vfs-path', 
                       help='Path to VFS CSV file')
    parser.add_argument('--start-script',
                       help='Path to startup script file')
    
    # Парсим аргументы
    args = parser.parse_args()
    
    return args