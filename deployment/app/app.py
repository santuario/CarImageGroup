from flask import Flask, render_template, request, jsonify
from image_model_evaluator import evaluate_images
from model_responses import classify_images
import base64
import os

app = Flask(__name__)

step1_result_path = os.getenv("STEP1_PATH")
exp_path = os.getenv("HOME_PATH")
step2b_result_path = os.getenv("STEP2B_PATH")
step3_prompt_path = os.getenv("STEP3_PROMT_PATH")
step3_result_path = os.getenv("STEP3_RESULT_PATH")

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify(error='No image part'), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')

    
    responses = classify_images(evaluate_images(image_base64, step1_result_path, exp_path), step1_result_path, step2b_result_path, step3_prompt_path, step3_result_path)

    vision_response = responses.json()
    content = vision_response.get('choices', [{}])[0].get('message', {}).get('content', '')
    return jsonify(description=content), 200





@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

