import sys
import os
import shutil
import argparse
import json
from tqdm import tqdm
from PIL import Image
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
from dotenv import load_dotenv, find_dotenv
from utils.argument import get_args

# Load environment variables
env_path = find_dotenv()
load_dotenv(env_path)
home_path = os.getenv("HOME_PATH")
sys.path.append(home_path + "/KLUSTER")

class ImageModelEvaluator:
    """
    A class to handle the evaluation of a descriptions generated on a set of images.
    """

    def __init__(self, args):
        self.args = args
        self.model, self.processor = self.load_model()

    def load_model(self):
        """
        Loads the machine learning model and processor.
        """
        processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xxl")
        model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xxl", device_map="auto", offload_folder="offload", offload_state_dict=True, torch_dtype=torch.float32)
        return model, processor

    @staticmethod
    def read_file_to_string(filename):
        """
        Reads a file and returns its content as a string.
        """
        with open(filename, 'r') as file:
            content = file.read()
        return content

    @staticmethod
    def load_image_paths_from_folder(folder_path):
        """
        Loads all image file paths from a specified folder.
        """
        image_paths = []
        for filename in os.listdir(folder_path):
            if filename.lower().endswith((".jpg", ".png", ".jpeg")):  # Simplified condition
                image_paths.append(os.path.join(folder_path, filename))
        return image_paths

    def evaluate(self):
        """
        Evaluates the model on the specified set of images.
        """
        image_files = self.load_image_paths_from_folder(self.args.image_folder)
        answers_file = os.path.expanduser(self.args.step1_result_path)
        os.makedirs(os.path.dirname(answers_file), exist_ok=True)

        with open(answers_file, "w") as ans_file:
            questions = self.read_file_to_string(f"{self.args.exp_path}/step1_prompt.txt")

            for image_file in tqdm(image_files):
                image_path = os.path.join(self.args.image_folder, image_file)
                try:
                    image = Image.open(image_path)
                    inputs = self.processor(image, questions, return_tensors="pt").to(device="cpu", dtype=torch.float32)
                    out = self.model.generate(**inputs, max_new_tokens=50)
                    outputs = self.processor.decode(out[0], skip_special_tokens=True)

                    ans_file.write(json.dumps({"text": outputs, "image_file": image_file, "metadata": {}}) + "\n")
                except Exception as e:
                    print(f"Error processing file {image_file}: {e}")

            if not os.path.exists(f"{self.args.exp_path}/step1_result.jsonl"):
                shutil.copy(self.args.step1_result_path, f"{self.args.exp_path}/step1_result.jsonl")

if __name__ == "__main__":
    args = get_args()  # Assuming get_args() is a function that parses command line arguments
    evaluator = ImageModelEvaluator(args)
    evaluator.evaluate()
