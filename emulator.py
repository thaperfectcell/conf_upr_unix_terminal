# Импортируем наш парсер из отдельного файла
from parser import parse_command

def main():
    print("=== Emulator Started ===")
    
    while True:
        command_line = input("[vfs] $ ")
        
        command, args = parse_command(command_line)
        
        # Пустая команда - пропускаем
        if command is None:
            continue
        
        if command == "exit":
            print("Goodbye!")
            break
        elif command == "ls":
            print(f"Command: ls, args: {args}")
        elif command == "cd":
            print(f"Command: cd, args: {args}")
        else:
            # Красиво выводим команду и аргументы
            if args:
                print(f"Command: {command}, args: {', '.join(args)}")
            else:
                print(f"Command: {command}, args: []")

if __name__ == "__main__":
    main()