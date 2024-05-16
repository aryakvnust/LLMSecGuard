# Analyzer Service

This directory is used to host a sample analyzer service that is used to analyze the code. `analyzer` service could be ran via the UI by navigating to `/security-agent/analyzer/start_built_in/`.

A Custom engine could also be used as long as it follows the supported interface. 

## API Interface

Analyzers host an HTTP server that is used to communicate with the tool. The out-of-the-box analyzer is built around Regex and [Weggli](https://github.com/weggli-rs/weggli) rules. 

To write a custom analyzer follow these interfaces for the input and the output: 

**INPUT**:
```json
{
    "lang": "STRING - ENUM",
    "code": "STRING - SOURCE CODE",
    "rules": [{ 
        "id": "UNIQUE ID",
        "rule": "STRING - RULE"
    }]
}
```

**OUTPUT**:
```json
{
    "status": "success || error" , 
    "uuid": "BATCH ID",
    "results": [{
        "file": "FILE NAME",
        "line": 0,
        "code": "CONCERING CODE"
    }]
}
```