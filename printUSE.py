# import tensorflow as tf
import numpy as np
import pandas as pd

# saved_dir = "USE"
#
# use_model = tf.saved_model.load(saved_dir)
#
# sentences = [
#     "I feel great",
#     "I am feeling awesome",
#     "This is a cat",
#     "Dogs are friendly animals"
# ]
#
# # Generate embeddings for sentences
# embeddings = use_model(sentences)
#
# # Calculate the scores by summing the embeddings
# scores = [np.sum(embedding) for embedding in embeddings]
#
# # Print the sentences along with their scores
# for sentence, score in zip(sentences, scores):
#     print(f"Sentence: {sentence}")
#     print(f"Score: {score}")
#     print()

df = pd.read_csv("C:/Users/hp/Downloads/Feem/data.csv")
print(df)