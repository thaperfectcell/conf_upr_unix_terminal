from parser import parse_command
from config import parse_arguments
from script_runner import execute_script_file

def format_command_output(command, args):
    if args:
        args_str = ', '.join(f"'{arg}'" for arg in args)
        return f"Command: {command}, args: [{args_str}]"
    else:
        return f"Command: {command}, args: []"

def display_startup_info(vfs_path, start_script):
    print("=== DEBUG: Startup Parameters ===")
    print(f"VFS path: {vfs_path if vfs_path else '(not specified)'}")
    print(f"Start script: {start_script if start_script else '(not specified)'}")
    print("=== Starting emulator ===")

def execute_command(command, args):
    if command == "exit":
        return "exit", None
    elif command == "ls":
        return "continue", format_command_output("ls", args)
    elif command == "cd":
        return "continue", format_command_output("cd", args)
    else:
        return "continue", format_command_output(command, args)

def main():
    # Получаем аргументы командной строки
    args = parse_arguments()
    
    # Показываем отладочную информацию
    display_startup_info(args.vfs_path, args.start_script)
    
    # Если указан стартовый скрипт - выполняем его
    if args.start_script:
        print(f"\nExecuting startup script: {args.start_script}")
        script_commands = execute_script_file(args.start_script)
        
        for command_line in script_commands:
            # Показываем команду
            print(f"[vfs] $ {command_line}")
            
            # Выполняем команду
            command, args_list = parse_command(command_line)
            if command is None:
                continue
                
            result_type, output = execute_command(command, args_list)
            
            # Показываем результат
            if output:
                print(output)
            
            if result_type == "exit":
                print("Goodbye!")
                return
    
    print("\nEntering interactive mode...")
    while True:
        command_line = input("[vfs] $ ")
        command, args_list = parse_command(command_line)
        
        if command is None:
            continue
        
        result_type, output = execute_command(command, args_list)
        
        if output:
            print(output)
            
        if result_type == "exit":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()