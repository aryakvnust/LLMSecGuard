from flask import Flask, request, jsonify
from CybersecurityBenchmarks.insecure_code_detector import insecure_code_detector as icd
from CybersecurityBenchmarks.insecure_code_detector.insecure_patterns import InsecurePattern

import json

app = Flask(__name__)

debug = True

@app.route('/analyze_code', methods=['GET'])
async def analyze_code_get():
    result = []
    # find vulnerable code for debugging
    instructs = json.load(open("CybersecurityBenchmarks/datasets/instruct/instruct.json", "r", encoding="utf-8"))
    # for i, c in enumerate(code):
    #     r = await icd.analyze("cpp", c['origin_code'])
    #     print(i, r)
    #     result.append(r)
        
    code = instructs[4]['origin_code']
    result = await icd.analyze("cpp", code)
    print(code)
    return jsonify({
        'code': code, 
        'results': result
    })


@app.route('/analyze_code', methods=['POST'])
async def analyze_code():
    code = request.json['code']
    language = request.json['language']
    patterns = request.json.get('patterns')
    
    if patterns is None:
        patterns = []
    
    if language is None:
        language = "cpp"
        
    result = await icd.analyze(language, code, custom_patterns=patterns)
    
    return jsonify(result)

app.run(debug=debug)