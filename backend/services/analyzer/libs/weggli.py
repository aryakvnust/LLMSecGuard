import subprocess
import json
import re

PREFIX = r'^C:\\'

def run_weggli_analysis(file_path, language, weggli_rule):
    # Construct the weggli command
    command = ['weggli', '--cpp', '-n', '-A', '0', '-B', '0', weggli_rule, file_path]

    # Run the command and capture the output
    result = subprocess.run(command, stdout=subprocess.PIPE)

    # Parse the output from the command
    output = parse_weggli_output(result.stdout.decode())
    return output


def parse_weggli_output(output):
    # Split the output into lines
    lines = output.split('\n')

    # Initialize an empty list to store the parsed results
    parsed_results = []

    # Initialize an empty string to store the current file path
    current_file = ''
    skip = False

    # Iterate over each line in the output
    for line in lines:
        # If the line contains a file path, update the current file path
        if re.match(PREFIX, line):
            current_file = line.split(':')[1].strip()
            skip = True
            
        # If the line contains a code snippet, parse it and add it to the parsed results
        elif re.match(r'^\s*\d+:', line):
            
            if skip == True:
                skip = False
                continue
                
            line_number, code = line.split(':', 1)
            parsed_results.append({
                'file': current_file,
                'line': int(line_number.strip()),
                'code': code.strip()
            })
            
            skip = True

    # Return the parsed results
    return parsed_results
