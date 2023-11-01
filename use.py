import tensorflow as tf
import os

# Specify the directory path where the USE model is saved
saved_dir = 'USE'

# Load the USE model
use_model = tf.saved_model.load(saved_dir)

# Define sentences to be evaluated
sentences = [
    "My name is suyash.",
    "That boy's name is suyash.",
    "He studies in APSIT."
]

# Encode the sentences
embeddings = use_model(sentences)

# Calculate the cosine similarity between sentences

for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        similarity_score = tf.tensordot(embeddings[i], embeddings[j], axes=1).numpy()
        print(f"Similarity between '{sentences[i]}' and '{sentences[j]}': {similarity_score:.4f}")
        