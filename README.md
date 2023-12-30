# ALGOTIVE KlusterCar App 🚗: Sorting Vehicles Images with a Textual Twist

## 📣 Try

Experience the ease of clustering vehicle images with our intuitive drag-and-drop interface. Simply drag an image into the designated drop zone and let our AI-powered system analyze and sort the vehicle based on its visual and textual features, such as color, type, and orientation.

- Live App here: [ALGOTIVE KlusterCar App](https://algotive-kluster-cars-v1-5rxxsuinqa-zf.a.run.app/)

<div align="center">
  <img src="./figures/Video-Recording-2.gif" alt="Sample video of working App" width="980"/>
</div>

## 📕 Overview

This innovative clustering solution is designed for the automatic grouping of vehicle images obtained from surveillance camera footage. By employing the synergy of vision-language models (VLMs) and large language models (LLMs), we follow the IC|TC: Image Clustering Conditioned on Text Criteria that introduces a novel approach to image clustering [(arXiv link)](https://arxiv.org/abs/2310.18297). It not only prioritizes accuracy but also user-defined flexibility, allowing for the grouping of images based on a variety of text-based features such as color, orientation, and vehicle type. The system is capable of adapting to different features, showcasing a versatile application in the realm of automated surveillance and data organization.

Our approach showcases its capability in the sample image below, where various vehicle images are automatically classified into distinct categories. The system identifies and groups vehicles based on:

- **Vehicle Color**: Examples include white, silver, black, dark gray, blue, yellow, green, orange and red.
- **Vehicle Type**: Categorization into types such as bus, van, sedan, hatchback, pickup, truck, coupe and SUV.
- **View Angle**: Classifying the viewpoint of the vehicle image, such as front-view, rear-view, three-quarter rear-view, three-quarter front-view and side-view.
- **Roof Features**: Classifying the roof such as none, sunroof, roof rails, cargo or roof rack.

This visual summary underscores the app's proficiency in interpreting and sorting images based on the extracted features, demonstrating a high level of accuracy and detail in its classification process.

<div align="center">
  <img src="./figures/Label-Summary.png" alt="Summary of vehicle labels" width="980"/>
</div>

## 🔍 Problem Statement

In the bustling intersections of modern cities, surveillance cameras are the ever-watchful eyes, capturing every moment on the streets. Among the myriad of images collected, vehicles of all shapes and colors zip through the frame, each with a story to tell. The challenge we faced was not just to make sense of this vehicular mosaic but to bring order to the chaos. How do we group these mechanical marvels, not by the loudness of their horns or the brightness of their headlights, but by features that can be described in words? The ALGOTIVE KlusterCar App rises to the occasion, clustering with a clever textual twist, where traditional algorithms merely spin their wheels.

## 💬 Solution Approach

1️⃣ **Image Description Extraction**: We began by extracting comprehensive descriptions for each image using advanced VLMs. This process transformed visual data into descriptive text, laying the groundwork for further analysis.

2️⃣ **Label Derivation**: With the image descriptions in hand, we then utilized LLMs to intelligently generate labels. These labels distilled the essence of each image into textual features that could be used for clustering.

3️⃣ **Label Clustering**: The derived labels were grouped using LLMs, allowing us to organize the dataset into a predetermined number of clusters. This step involved fine-tuning the models to balance the granularity and coherence of the groupings.

4️⃣ **Image Classification**: Post-clustering, the images were categorized according to the groupings, ensuring that each cluster was homogenous in terms of the selected feature.

5️⃣ **Performance Evaluation**: To quantify the efficacy of our system, we employed the Hungarian Matching algorithm, which provided us with metrics such as Accuracy, Adjusted Rand Index (ARI), and Normalized Mutual Information (NMI).

## 💬🖍 Detailed Solution Approach

The methodology we employed to tackle the image clustering challenge is a testament to the versatility and power of combining different AI domains. Here's an in-depth look at our approach:

### 1. Image Description Extraction

The journey of our ALGOTIVE KlusterCar App begins with the insightful extraction of vehicle narratives from raw pixels. Our script, `visual_insight_generator.py`, harnesses the power of Salesforce's BLIP-2 (Bridging Language and Image Pre-training) model, a cutting-edge Vision-Language Model (VLM). The model is adept at generating rich textual descriptions that capture the nuanced features of each vehicle image in the dataset.

The script functions by iterating over images in a specified folder, each time invoking the BLIP-2 model to interpret the visual content and translate it into a descriptive text. The process is meticulous and handled with precision, thanks to the script's error management and progress tracking through tqdm. The generated descriptions are saved in a JSONL format, paving the way for the subsequent clustering and classification steps.

The use of environment variables and dynamic path management ensures that the script is adaptable and can be integrated seamlessly into different systems or workflows. Through this script, images are no longer just static data but stories waiting to be grouped into meaningful chapters.

_Script:_ `visual_insight_generator.py`

### 2. Label Derivation

With a trove of descriptive texts in hand from our first step, the `label_generator.py` script comes into play. This script is the bridge between raw descriptions and actionable data, translating verbose narratives into concise labels suitable for clustering. It employs two potent language models — GPT for general-purpose text generation and LLAMA for specialized prompts — to analyze and abstract the key features from the previously generated image descriptions.

The script's process is twofold: it reads the detailed descriptions and then, depending on whether we're using GPT or LLAMA, sends them to the respective language model. This dual-model strategy ensures that our labels are not just accurate but also relevant to the clustering criteria.

The output is a clean, organized set of labels that serve as the DNA for the forthcoming clustering phase. Each label is a condensed version of the image's story, ready to be categorized into a family of similar tales. The script's efficiency and precision are amplified by its use of environment variables and dynamic API management, allowing for seamless integration into our clustering workflow.

_Script:_ `label_generator.py`

### 3. Label Clustering

Once we have our raw labels ready, it's time for the `label_clustering.py` script to shine. This script performs the crucial task of organizing these labels into coherent groups, setting the stage for efficient image categorization.

The script begins by filtering the labels to ensure only the most relevant and frequently occurring ones are considered for clustering. It then employs either GPT or LLAMA models, depending on the setup, to analyze these labels and cluster them based on the specified number of classes. This process is not just about grouping similar labels; it's about understanding the context and nuances of each label and how they relate to each other in the grand scheme of our clustering criteria.

One of the key features of this script is its adaptability. It dynamically loads environment variables and adjusts its processing based on the model version used. In cases where the standard model encounters limitations, the script smartly falls back to a more capable model version, ensuring robustness and reliability in clustering.

The final output of this script is a set of clustered labels, each representing a distinct group of vehicle images based on the chosen feature. This output is a testament to the script's ability to transform a collection of individual labels into a meaningful and structured classification scheme.

_Script:_ `label_clustering.py`

### 4. Image Classification

Following the clustering of labels, the next pivotal step in our ALGOTIVE KlusterCar App is the `image_classifier.py` script. This script is tasked with the critical job of assigning each image to one of the previously determined clusters based on its descriptive features.

The script operates by first extracting the classes from the labels. It then reads through the initial answers - the detailed descriptions of each image - and prompts the language model (either GPT or LLAMA, based on the configuration) to classify these images. The model is asked to determine which cluster each image belongs to, based on its description.

What makes this script particularly efficient is its methodical approach to handling large volumes of data, courtesy of tqdm for progress tracking, and its dynamic environment variable loading for model configuration. The script ensures that each image is carefully analyzed and accurately placed into the most fitting category, considering all the nuanced details captured in the description.

The final outcome is a neatly organized set of images, each assigned to a cluster that best represents its key characteristics, as interpreted by the AI models. This step is crucial as it transforms our abstract labels into tangible groupings of similar images, ready for any practical application or further analysis.

_Script:_ `image_classifier.py`

### 5. Performance Evaluation

The final chapter in our ALGOTIVE KlusterCar App's journey is encapsulated by the `performance_evaluator.py` script. This script is designed to rigorously assess the accuracy and effectiveness of our clustering process.

It begins by loading the final answers (i.e., the classified images) and compares them with a set of pre-defined classes to ensure correctness. In cases where there's a mismatch, the script intelligently assigns a random but plausible class, maintaining the integrity of the dataset.

A key component of this evaluation is the application of the Hungarian Matching algorithm, which provides an accurate assessment of the clustering performance. The script calculates various statistics like silhouette score, Calinski-Harabasz index, and Davies-Bouldin index, offering a comprehensive view of the clustering quality.

Additionally, the script employs KMeans clustering to generate sample data and labels for further validation. This approach allows for a thorough comparison between the predicted and true labels, enabling us to measure the system's accuracy, precision, and overall efficiency.

The result is a detailed report, saved as `accuracy.txt`, which outlines the clustering's effectiveness in various statistical terms. This evaluation is crucial, as it not only validates our model's capability but also highlights areas for potential improvement in future iterations.

_Script:_ `performance_evaluator.py`

## 📗 Results

The system exhibited high accuracy and outperformed baseline methods in clustering images based on various text criteria. Detailed results and performance metrics for View Angle are provided, showcasing the system's effectiveness.

<div align="center">
  <img src="./figures/View-Angle-Clusters.png" alt="View Angle Metrics" width="980"/>
</div>

| Metric                  | Value | Interpretation                                                                                                                                                                    |
| ----------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Silhouette Score        | 0.627 | Indicates strong cohesion and separation; vehicle images are well-grouped by view angle.                                                                                          |
| Calinski-Harabasz Index | 55161 | Higher values mean clusters are dense and well separated, suggesting tight grouping within view angle clusters and clear distinction between them.                                |
| Davies-Bouldin Index    | 0.52  | Lower values indicate better clustering; implies that clusters are well separated from each other, and the algorithm has effectively distinguished between different view angles. |

Based on these metrics, we can conclude that the clustering algorithm performed well in segmenting the vehicle images by their view angles, with clear differentiation between the various views. This suggests that the approach used is effective for this particular application.

## 🛠 Deployment

The model is optimized for production deployment, focusing on improving latency and throughput. A Docker app, as demonstrated in the provided screenshot, is used for the production-like environment, taking advantage of its containerization features for easy scalability and replication.

<div align="center">
  <img src="./figures/App-1.png" alt="Sample image of working App" width="980"/>
</div>

The ALGOTIVE KlusterCar App is deployed with a robust backend service that includes an API endpoint for image analysis. Below is the documentation for using the API:

### API Endpoint: `/analyze-image`

This endpoint accepts `POST` requests containing an image file and returns a JSON response with the classified features of the vehicle in the image.

#### Request

- **Method**: `POST`
- **Endpoint**: `/analyze-image`
- **Content-Type**: `multipart/form-data`
- **Body**:
  - `image`: The image file to be analyzed.

#### Response

A successful request returns a `200 OK` status with a JSON payload containing the classified features of the vehicle. If the request does not contain an image or another error occurs, it will return a `400 Bad Request` status with an error message.

##### Example Response:

```json
{
  "vehicle_color": "yellow",
  "vehicle_type": "truck",
  "view_angle": "front-view",
  "roof_features": "none"
}
```

### API Endpoint Performance

During testing, our `/analyze-image` endpoint exhibited an response time of **3.91 seconds**. This metric reflects the latency from the instant a POST request with an image is sent to the server to the moment a response is received.

#### Latency:

- **Response Time**: The API endpoint has an average latency of 3.91 seconds. While this may be suitable for non-time-critical applications, efforts to optimize the server's response time are ongoing to enhance the user experience for more time-sensitive use cases.

Further optimization strategies are being considered to reduce this latency, including but not limited to:

- Refactoring the code to improve efficiency.
- Upgrading server hardware or increasing bandwidth.
- Implementing asynchronous processing to handle requests more quickly.

## 📃 Repository Structure

- `data/`: Contains the dataset of car images used for model training and evaluation.
- `deployment/`: Contains the necessary files and scripts for deploying the model, including Docker configuration files.
- `figures/`: Includes any figures, charts, and images generated during analysis or as part of the project's results.
- `src/`: Holds the source code for the project, with scripts for each step of the clustering and classification process.
- `utils/`: Provides utility scripts and functions that support the main processes, like argument parsing and LLM interaction utilities.
- `challenge_instructions.txt`: Instructions or notes regarding the image clustering challenge.
- `visual_insight_generator.py`: Generates descriptive insights from images (STEP 1).
- `predictive_label_analyzer.py`: Analyzes and predicts labels for the images (STEP 2).
- `cluster_label_aggregator.py`: Handles the aggregation of labels into clusters (STEP 3).
- `classifier.py`: The script responsible for the classification step in the clustering process (STEP 4).
- `measuring_acc.py`: Evaluates the clustering accuracy and other performance metrics (STEP 5).

## 🤓 Contributions

We followed best practices in coding and repository contributions, including descriptive commit messages and well-organized scripts.

## 🤯 Research and Creativity

This project stands out for its novel use of text criteria in image clustering and the creative application of language models to derive meaningful image groupings.

## 💚 Acknowledgements

This project, ALGOTIVE KlusterCar App, draws inspiration from the groundbreaking work detailed in "Image Clustering Conditioned on Text Criteria" by Sehyun Kwon, Jaeseung Park, Minkyu Kim, Jaewoong Cho, Ernest K. Ryu, and Kangwook Lee. The paper provides a solid foundation for our approach and has been instrumental in guiding our methodology.

For those interested in delving deeper into the research that underpins our work, we encourage you to read the full paper, available on [arXiv](https://arxiv.org/pdf/2310.18297.pdf).
