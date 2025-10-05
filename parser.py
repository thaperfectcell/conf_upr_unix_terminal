import os

def expand_environment_variables(text):
    words = text.split()
    expanded_words = []
    
    for word in words:
        if word.startswith('$'):
            var_name = word[1:]
            var_value = os.getenv(var_name)
            if var_value:
                expanded_words.append(var_value)
            else:
                expanded_words.append(word)
        else:
            expanded_words.append(word)
    
    return ' '.join(expanded_words)

def parse_command(command_line):
    expanded_line = expand_environment_variables(command_line)
    parts = expanded_line.split()
    
    if not parts:
        return None, []
    
    command = parts[0]
    args = parts[1:]
    return command, args