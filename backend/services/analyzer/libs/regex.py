import re

def run_regex_analysis(code, regex):
    matches = []
    
    for line_number, line in enumerate(code.split('\n'), start=1):
        for match in re.finditer(regex, line):
            matches.append({
                'file': 'code',
                'line': line_number,
                'code': match.group()
            })
            
    return matches
