"""
Model inference logic using the 'KingNish/Reasoning-0.5b' model.

- Loads the model and tokenizer once at startup for reuse.
- Handles reasoning generation and final answer prediction.
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Constants for reasoning and response token limits
MAX_REASONING_TOKENS = 1024
MAX_RESPONSE_TOKENS = 512

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Loading model to: {DEVICE}")
MODEL_NAME = "KingNish/Reasoning-0.5b"
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype="auto").to(DEVICE)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def generate_reasoning_and_answer(prompt: str) -> str:
    """
    Generate reasoning and an answer based on the provided prompt using the 
    "KingNish/Reasoning-0.5b" model.

    Args:
        prompt (str): The input prompt/question from the user.

    Returns:
        str: The generated answer from the model.
    """
    # Step 1: Prepare the prompt and reasoning template
    messages = [
        {"role": "user", "content": prompt}
    ]

    reasoning_template = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_reasoning_prompt=True
    )
    reasoning_inputs = tokenizer(reasoning_template, return_tensors="pt").to(model.device)

    # Step 2: Generate reasoning
    reasoning_ids = model.generate(
        **reasoning_inputs,
        max_new_tokens=MAX_REASONING_TOKENS
    )
    reasoning_output = tokenizer.decode(
        reasoning_ids[0, reasoning_inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )

    # Step 3: Generate the final answer based on the reasoning
    messages.append(
        {"role": "reasoning", "content": reasoning_output}
    )
    response_template = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    response_inputs = tokenizer(
        response_template,
        return_tensors="pt"
    ).to(model.device)
    response_ids = model.generate(
        **response_inputs,
        max_new_tokens=MAX_RESPONSE_TOKENS
    )
    response_output = tokenizer.decode(
        response_ids[0, response_inputs.input_ids.shape[1]:],
        skip_special_tokens=True
    )
    return response_output
