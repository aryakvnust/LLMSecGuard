# Apps.Dispatcher

## Use Case

The `apps.dispatcher` module is responsible for handling the dispatching of prompts in the LLMSecGuard backend system. It provides functionality to manage and track the progress of tasks as they are assigned to different workers.

## Models

The dispatcher app consists of the following models: 

1. `LlmModel`: Contains name, type and API key alongside basic information about the model. 
2. `LlmResponse`: Contains of an LlmModel and a response. The purpose of this module is to record all prompts and responsed for dataset gathering.


## Usage

To use the `apps.dispatcher` module, you can import the necessary classes and functions into your code. For example:
