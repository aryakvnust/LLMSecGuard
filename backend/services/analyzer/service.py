from flask import Flask, request
from libs import weggli
import os
import shutil
import uuid
import json
import re
import concurrent.futures
    
app = Flask(__name__)

@app.route('/weggli', methods=['POST'])
def weggli_post():
    data = request.get_json()
    uuid_str = str(uuid.uuid4())

    dir_path = os.path.join('.', 'temp', uuid_str)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, 'CODE.' + data['lang'])
    with open(file_path, 'w') as f:
        f.write(data['code'])

    RULES = data['rules']

    results = []


    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for rule in RULES:
            future = executor.submit(weggli.run_weggli_analysis, file_path, data['lang'], rule['rule'])
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            for res in result:
                res['rule'] = rule['id']
                results.append(result)
                
        print(results)
        
    shutil.rmtree(dir_path)

    return {'status': 'success', 'uuid': uuid_str, 'results': flatten_extend(results)}, 200


@app.route('/regex', methods=['POST'])
def regex_post():
    data = request.get_json()
    regex = data['regex']
    code = data['code']

    matches = []
    for line_number, line in enumerate(code.split('\n'), start=1):
        for match in re.finditer(regex, line):
            matches.append({
                'file': 'code',
                'line': line_number,
                'code': match.group()
            })

    return {'status': 'success', 'matches': matches}, 200


def flatten_extend(matrix):
    flat_list = []
    for row in matrix:
        flat_list.extend(row)
    return flat_list


if __name__ == '__main__':
    app.run(debug=True)