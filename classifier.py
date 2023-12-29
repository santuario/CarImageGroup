import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
from utils.llm_utils import get_gpt_response, get_llama_response
from utils.argument import args 

def load_environment_variables():
    """ Load the appropriate environment variables based on the model type. """
    api_key, user, model = (os.getenv(key) for key in ["API_KEY", "USER", "MODEL"]) if args.use_gpt4 else (os.getenv(key) for key in ["API_KEY_3.5", "USER_3.5", "MODEL_3.5"])
    llama_url = os.getenv(f"LLAMA_{args.llama_ver.upper()}_URL") if args.llama_ver else ""
    return api_key, user, model, llama_url

def read_file(file_path):
    """ Reads content from a file. """
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except IOError:
        print(f"Error reading file: {file_path}")
        return []

def extract_classes_from_labels(file_lines):
    """ Extracts classes from given lines of a file. """
    return [line.split(":")[1].strip().lower() for line in file_lines if "Reason" not in line and line.strip() != "" and ":" in line]

def get_model_responses(system_prompt, answers, api_key, user, model, url):
    """ Gets responses from the model for each answer. """
    results = []
    for answer in tqdm(answers):
        answer_data = json.loads(answer)
        user_prompt = answer_data["text"] + "\nTo which class from the list does this image belong to, based on the description provided? Answer in the following format: \"Answer: {class}\""
        response = get_llama_response(system_prompt, user_prompt, url) if args.llama else get_gpt_response(system_prompt, user_prompt, api_key, user, model)
        image_text = f"Image file-{answer_data['image_file']} " if "image_file" in answer_data else ""
        results.append(image_text + response)
    return results

def save_results(results, result_path):
    """ Saves results to a file. """
    try:
        with open(result_path, 'w') as file:
            file.write("\n".join(results))
    except IOError:
        print(f"Error writing to file: {result_path}")

def main():
    load_dotenv()
    api_key, user, model, url = load_environment_variables()
    
    # Process step2b results
    step2b_results = read_file(args.step2b_result_path)
    class_list = extract_classes_from_labels(step2b_results)

    # Read and process system prompt
    system_prompt_lines = read_file(args.step3_prompt_path)
    system_prompt = ''.join(system_prompt_lines).replace("[__CLASSES__]", str(class_list))

    # Process initial answers
    answers = read_file(args.step1_result_path)
    responses = get_model_responses(system_prompt, answers, api_key, user, model, url)
    save_results(responses, args.step3_result_path)

if __name__ == "__main__":
    main()
