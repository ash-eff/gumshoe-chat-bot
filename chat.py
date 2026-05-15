import json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-sonnet-4-6"
system = (
    "You are a noir detective. "
    "You LOVE pizza. "
    "You will explain things simply. "
    ) 

def add_user_message(messages, text):
    user_message = {
        "role": "user", 
        "content": text
    }
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {
        "role": "assistant", 
        "content": text
    }
    messages.append(assistant_message)

def chat(messages, temperature=1.0, print_output=False):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    if system:
        params["system"] = system

    with client.messages.stream(**params) as stream:
        for text in stream.text_stream:
            if print_output:
                print(text, end="", flush=True)
        if print_output:
            print()

        usage_cost = stream.get_final_message().usage
        return stream.get_final_text(), usage_cost.input_tokens, usage_cost.output_tokens
    
def calculate_token_usage(in_tok, out_tok, total, show_usage = True):
    total += in_tok + out_tok
    if show_usage: 
        print("tokens: {} in, {} out | total session: {}".format(in_tok, out_tok, total))
    return total
    
def main():
    total_tokens = 0
    try:
        with open('message-history.json', 'r') as file:
            content = file.read().strip()
            messages = json.loads(content) if content else []
    except FileNotFoundError:
        print("No history Found")
        messages = []

    while True:
        user_input = input("> ")
        if user_input.lower() in ("quit", "exit", "q"):
            break

        add_user_message(messages, str(user_input))
        answer, in_tokens, out_tokens = chat(messages)
        total_tokens = calculate_token_usage(in_tokens, out_tokens, total_tokens)
        add_assistant_message(messages, answer)
    
    with open('message-history.json', 'w') as file:
        file.write(json.dumps(messages))

if __name__ == "__main__":
    main()