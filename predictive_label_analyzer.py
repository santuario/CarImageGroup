import os
import json
from tqdm import tqdm
from dotenv import load_dotenv
from utils.argument import args 
from utils.llm_utils import get_gpt_response, get_llama_response

def load_api_settings(use_gpt4):
    """
    Load API settings based on the model version.
    """
    suffix = "" if use_gpt4 else "_3.5"
    api_key = os.getenv(f"API_KEY{suffix}")
    user = os.getenv(f"USER{suffix}")
    model = os.getenv(f"MODEL{suffix}")
    return api_key, user, model

def get_llama_url(version):
    """
    Get the appropriate URL for the LLAMA version.
    """
    return os.getenv(f"LLAMA_{version.upper()}_URL")

def process_responses(prompts_path, answers_path, use_llama, llama_url, api_key, user, model):
    """
    Process responses using the specified model.
    """
    results = []
    with open(prompts_path, "r") as label_file, open(answers_path, "r") as answer_file:
        system_prompt = label_file.read()
        answers = answer_file.readlines()

        for answer in tqdm(answers):
            answer_data = json.loads(answer)
            user_prompt = answer_data["text"]
            response = get_llama_response(system_prompt, user_prompt, llama_url) if use_llama else get_gpt_response(system_prompt, user_prompt, api_key, user, model)
            image_text = f"Image file-{answer_data['image_file']};" if "image_file" in answer_data else ""
            results.append(image_text + response)

    return "\n".join(results)

def save_results(results, result_path):
    """
    Save the processed results to a file.
    """
    with open(result_path, 'w') as file:
        file.write(results)

if __name__ == "__main__":
    load_dotenv()
    api_key, user, model = load_api_settings(args.use_gpt4)
    llama_url = get_llama_url(args.llama_ver) if args.llama else ""
    
    results = process_responses(args.step2a_prompt_path, args.step1_result_path, args.llama, llama_url, api_key, user, model)
    save_results(results, args.step2a_result_path)
