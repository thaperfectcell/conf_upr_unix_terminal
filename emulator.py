from parser import parse_command
from config import parse_arguments
from script_runner import execute_script_file
from vfs import VirtualFileSystem
from commands import execute_ls, execute_cd, execute_pwd, execute_whoami, execute_uptime, execute_du, execute_echo, execute_chmod, execute_cp, execute_vfs_load
import time

class EmulatorState:
    """
    Класс для хранения состояния эмулятора
    """
    def __init__(self):
        self.start_time = time.time()
    
    def get_uptime(self):
        """
        Возвращает время работы эмулятора в читаемом формате
        """
        uptime_seconds = int(time.time() - self.start_time)
        
        hours = uptime_seconds // 3600
        minutes = (uptime_seconds % 3600) // 60
        seconds = uptime_seconds % 60
        
        return f"{hours} hours, {minutes} minutes, {seconds} seconds"

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

def execute_command(command, args, vfs, emulator_state): 
    if command == "exit":
        return "exit", None
    elif command == "ls":
        result = execute_ls(args, vfs)
        return "continue", result
    elif command == "cd":
        result = execute_cd(args, vfs)
        return "continue", result
    elif command == "pwd":
        result = execute_pwd(args, vfs)
        return "continue", result
    elif command == "whoami":
        result = execute_whoami(args, vfs)
        return "continue", result
    elif command == "uptime":
        result = execute_uptime(args, vfs, emulator_state)  
        return "continue", result
    elif command == "du":
        result = execute_du(args, vfs)
        return "continue", result
    elif command == "echo":
        result = execute_echo(args, vfs)
        return "continue", result
    elif command == "chmod":
        result = execute_chmod(args, vfs)
        return "continue", result
    elif command == "cp":
        result = execute_cp(args, vfs)
        return "continue", result
    elif command == "vfs-load":
        result = execute_vfs_load(args, vfs)
        return "continue", result
    else:
        return "continue", f"Error: command '{command}' not found"
def main():
    args = parse_arguments()
    
    vfs = VirtualFileSystem()
    emulator_state = EmulatorState() 
    
    display_startup_info(args.vfs_path, args.start_script)
    
    # Если указан VFS путь - загружаем VFS
    if args.vfs_path:
        vfs.load_from_csv(args.vfs_path)
    
    # Если указан стартовый скрипт - выполняем его
    if args.start_script:
        print(f"\nExecuting startup script: {args.start_script}")
        script_commands = execute_script_file(args.start_script)
        
        for command_line in script_commands:
            print(f"[vfs] $ {command_line}")
            
            command, args_list = parse_command(command_line)
            if command is None:
                continue
                
            result_type, output = execute_command(command, args_list, vfs, emulator_state)  # НОВОЕ - передаем состояние
            
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
        
        result_type, output = execute_command(command, args_list, vfs, emulator_state)  # НОВОЕ - передаем состояние
        
        if output:
            print(output)
            
        if result_type == "exit":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()