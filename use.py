import tensorflow as tf
import os

# Specify the directory path where the USE model is saved
saved_dir = 'USE'

# Load the USE model
use_model = tf.saved_model.load(saved_dir)

# Define your sentences
sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A speedy brown fox leaps over the sleepy dog."

# Encode the sentences using the loaded model
embeddings = use_model([sentence1, sentence2])

# Compute the cosine similarity
similarity_score = tf.keras.losses.cosine_similarity(embeddings[0], embeddings[1]).numpy()

print(f"Similarity between the two sentences: {similarity_score}")
 