# Analyzer App

The Analyzer app is a component of the LLMSecGuard backend system. It is responsible for analyzing data and generating insights for security monitoring and threat detection.

## Use Case

The Analyzer app provides the following use cases:

1. Data Analysis: The app processes incoming data from various sources, such as logs, network traffic, and system events. It applies algorithms and techniques to analyze the data and identify potential security threats.

2. Threat Detection: The app uses machine learning models and rule-based systems to detect and classify security threats. It can identify patterns, anomalies, and suspicious activities that may indicate a security breach or attack.

3. Insights Generation: The app generates actionable insights and reports based on the analyzed data. It provides visualizations, statistics, and recommendations to help security analysts and administrators make informed decisions and take appropriate actions.

## Models

The Analyzer app utilizes the following models:

1. `Analyzer`: Consists of name, description and basic usage information. This model could be private to a user. 
2. `Rule`: The main ruleset that is used for semantic analyzers. This model could be private to a user. 
3. `History`: This models keeps track of the input code and the matched rules. This data is used for creating new datasets.
4. `MonthlySumCache`: This model is a simple running sum of uses vs detected security concerns for each model per gregorian month.
5. `Benchmark`: This model is used to store imported benchmarks from [PurpleLlama](https://github.com/facebookresearch/PurpleLlama/).

## Analyzer Interface

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