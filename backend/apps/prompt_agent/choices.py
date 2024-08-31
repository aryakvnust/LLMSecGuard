from django.db.models import TextChoices

class StatusChoices(TextChoices):
    PENDING = 'PENDING', 'Pending'
    DISPATCHED = 'DISPATCHED', 'Dispatched'
    DELIVERED = 'DELIVERED', 'Delivered'
    CANCELLED = 'CANCELLED', 'Cancelled'
    
LlmTypes = [
    "ANYSCALE::meta-llama/Llama-2-7b-chat-hf",
    "ANYSCALE::meta-llama/Llama-2-13b-chat-hf",
    "ANYSCALE::meta-llama/Llama-2-70b-chat-hf",
    "ANYSCALE::codellama/CodeLlama-34b-Instruct-hf",
    "ANYSCALE::mistralai/Mistral-7B-Instruct-v0.1",
    "ANYSCALE::HuggingFaceH4/zephyr-7b-beta",
    
    "OPENAI::gpt-3.5-turbo",
    "OPENAI::gpt-4",
    
    "TOGETHER::mistralai/Mistral-7B-v0.1",
    "TOGETHER::lmsys/vicuna-7b-v1.5",
    "TOGETHER::togethercomputer/CodeLlama-7b",
    "TOGETHER::togethercomputer/CodeLlama-7b-Python",
    "TOGETHER::togethercomputer/CodeLlama-7b-Instruct",
    "TOGETHER::togethercomputer/CodeLlama-13b",
    "TOGETHER::togethercomputer/CodeLlama-13b-Python",
    "TOGETHER::togethercomputer/CodeLlama-13b-Instruct",
    "TOGETHER::togethercomputer/falcon-40b",
    "TOGETHER::togethercomputer/llama-2-7b",
    "TOGETHER::togethercomputer/llama-2-7b-chat",
    "TOGETHER::togethercomputer/llama-2-13b",
    "TOGETHER::togethercomputer/llama-2-13b-chat",
    "TOGETHER::togethercomputer/llama-2-70b",
    "TOGETHER::togethercomputer/llama-2-70b-chat",

    "OPENROUTER::nousresearch/hermes-3-llama-3.1-405b",
    "OPENROUTER::nousresearch/hermes-3-llama-3.1-405b:extended",
    "OPENROUTER::meta-llama/llama-3.1-8b-instruct:free",
    "OPENROUTER::qwen/qwen-2-7b-instruct:free",
    "OPENROUTER::google/gemma-2-9b-it:free",
    "OPENROUTER::mistralai/mistral-7b-instruct:free",
    "OPENROUTER::microsoft/phi-3-mini-128k-instruct:free",
    "OPENROUTER::microsoft/phi-3-medium-128k-instruct:free",
    "OPENROUTER::meta-llama/llama-3-8b-instruct:free",
    "OPENROUTER::google/gemma-7b-it:free",
    "OPENROUTER::recursal/eagle-7b",
    "OPENROUTER::recursal/rwkv-5-3b-ai-town",
    "OPENROUTER::rwkv/rwkv-5-world-3b",
    "OPENROUTER::gryphe/mythomist-7b:free",
    "OPENROUTER::nousresearch/nous-capybara-7b:free",
    "OPENROUTER::openchat/openchat-7b:free",
    "OPENROUTER::undi95/toppy-m-7b:free",
    "OPENROUTER::huggingfaceh4/zephyr-7b-beta:free"
]
    