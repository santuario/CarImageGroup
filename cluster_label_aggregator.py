import os
from dotenv import load_dotenv
from utils.argument import args 
from utils.llm_utils import get_gpt_response, get_llama_response

def load_env_variables():
    """ Loads environment variables based on the model type. """
    suffix = "" if args.use_gpt4 else "_3.5"
    api_key = os.getenv(f"API_KEY{suffix}")
    user = os.getenv(f"USER{suffix}")
    model = os.getenv(f"MODEL{suffix}")
    llama_ver = args.llama_ver.upper().replace("LLAMA_", "")
    url = os.getenv(f"LLAMA_{llama_ver}_URL") if args.llama else ""
    return api_key, user, model, url

def read_file(file_path):
    """ Reads a file and returns its content. """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def post_process(answer_path):
    """ Post-processes the answer file and aggregates labels. """
    try:
        with open(answer_path, 'r') as file:
            answers = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {answer_path}")
        return {}

    answer_list = {}
    for answer in answers:
        answer = answer.split(";")[1] if "Image file-" in answer else answer
        label = " ".join(answer.split(" ")[1:]).lower().strip().strip(".")
        label = f'answer: {label}' if 'answer: ' not in label else label
        answer_list[label] = answer_list.get(label, 0) + 1
    return answer_list

def get_model_response(system_prompt, user_prompt, api_key, user, model, url):
    """ Gets the model response based on the provided prompts. """
    if args.llama:
        return get_llama_response(system_prompt, user_prompt, url)
    else:
        return get_gpt_response(system_prompt, user_prompt, api_key, user, model)

def save_response(response, result_path):
    """ Saves the response to a file. """
    try:
        with open(result_path, 'w') as file:
            file.write(response)
    except IOError:
        print(f"Could not write to file: {result_path}")

def main():
    load_dotenv()
    api_key, user, model, url = load_env_variables()
    answer_list = post_process(args.step2a_result_path)

    # Filter answers based on a threshold
    filtered_answers = {k: v for k, v in answer_list.items() if v > 5}

    system_prompt = read_file(args.step2b_prompt_path)
    if system_prompt is None:
        return

    system_prompt = system_prompt.replace("[__NUM_CLASSES_CLUSTER__]", str(args.num_classes))
    system_prompt = system_prompt.replace("[__LEN__]", str(len(filtered_answers)))

    user_prompt = f"list of labels: {filtered_answers}\nnum_classes: {args.num_classes}"
    response = get_model_response(system_prompt, user_prompt, api_key, user, model, url)

    if response == "ERROR_CONTEXT_LENGTH":
        # Fallback to gpt-4-32k
        api_key, user, model = os.getenv("API_KEY_32K"), os.getenv("USER_32K"), os.getenv("MODEL_32K")
        response = get_gpt_response(system_prompt, user_prompt, api_key, user, model)

    save_response(response, args.step2b_result_path)

if __name__ == "__main__":
    main()
