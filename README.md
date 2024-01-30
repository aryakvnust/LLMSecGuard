## LLMGuard
LLMGuard is tool for creating secure code with already-existing LLMs. 

## Components
- LLMGuard: Python + DJango
- Analyzer: Python + Flask
  - Weggli: Rust (Binary)
  - Semgrep: Executable
  - Regex: Built-in
 
## Environment

**Running LLMGuard**

1. Activate Python Env:
  - Windows: ``.\venv\Script\activate``
  - *nix:    ``source ./venv/bin/activate``

2. Install Dependecies:
   ``pip install -r requirements.txt``
   
4. Run Development Server:
  ``python manage.py runserver 0.0.0.0:8000``

**Running Standalone Analyzer Engine**

1. Activate Python Env:
  - Windows: ``.\venv\Script\activate``
  - *nix:    ``source ./venv/bin/activate``

2. Install Dependecies:
   ``pip install -r requirements.txt``

3. Install ``weggli``
   - Download compatible weggli executable from https://github.com/weggli-rs/weggli
   - Add executable path to PATH environmental variable.
   
5. Run Stand-alone Analyzer Engine: 
   ``python sub_servers.py``

## Usage
1. Create a superuser by running ``python manage.py createsuperuser``
2. Add API key of a supported LLM in ``/admin/`` under **Prompt Dispatcher > LLMs**
3. Navigate to main page of the tool (``http://localhost:8000``)
4. Type a prompt and wait for the response 
