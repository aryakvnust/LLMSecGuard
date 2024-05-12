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
]
    