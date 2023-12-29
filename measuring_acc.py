import os
import re
import torch
import random
from argument import args
from hungarian_match import hungarian_evaluate, confusion_matrix

def extract_class(file_name):
    """ Extracts class from the file name. """
    match = re.search(r'(\d+)_(.+)\.(jpg|png)', file_name)
    return match.group(2) if match else None

def load_final_answers(classification_path, clustering_path, final_classes):
    """ Loads final answers and classes from files. """
    final_answers = []
    with open(classification_path, 'r') as file:
        for line in file:
            try:
                final_answers.append(line.split(":")[1].strip().lower())
            except IndexError:
                final_answers.append(line)

    with open(clustering_path, 'r') as file:
        for line in file:
            if "Reason" not in line and line.strip() != "" and ":" in line:
                final_classes.append(line.split(":")[1].strip().lower())

    return final_answers

def correct_answers(final_answers, final_classes):
    """ Corrects the final answers based on the available classes. """
    corrected_answers, wrong_count = [], 0
    for answer in final_answers:
        if answer in final_classes:
            corrected_answers.append(answer)
        else:
            corrected_answers.append(random.choice(final_classes))
            wrong_count += 1
    return corrected_answers, wrong_count

def convert_to_numeric(classes):
    """ Converts class labels to numeric values. """
    unique_elements = list(set(classes))
    element_to_number = {element: i for i, element in enumerate(unique_elements)}
    return torch.tensor([element_to_number[element] for element in classes]), unique_elements

def save_stats(clustering_stats, stats_path):
    """ Saves clustering statistics to a file. """
    with open(stats_path, 'w') as file:
        file.write(str(clustering_stats))

def main():
    file_names = os.listdir(args.image_folder)
    true_classes = [extract_class(name) for name in file_names if extract_class(name) is not None]

    final_classes = []
    final_answers = load_final_answers(args.classification_result_path, args.clustering_result_path, final_classes)

    final_answers, wrong_count = correct_answers(final_answers, final_classes)
    print('Wrong Assigned:', wrong_count)

    final_answers_number, _ = convert_to_numeric(final_answers)
    true_classes_number, true_class_names = convert_to_numeric(true_classes)

    clustering_stats = hungarian_evaluate(targets=true_classes_number, predictions=final_answers_number,
                                          class_names=true_class_names, compute_confusion_matrix=True, 
                                          confusion_matrix_file=f"{args.exp_path}/confusion_matrix.pdf")
    print(clustering_stats)

    save_stats(clustering_stats, args.exp_path + "/accuracy.txt")

if __name__ == "__main__":
    main()
