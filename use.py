import tensorflow as tf

# Define the path to the extracted Universal Sentence Encoder model directory
model_dir = "USE"

# Load the USE model
use_model = tf.saved_model.load(model_dir)

sentence = "The quick brown fox jumps over the lazy dog."

# Encode the sentence using the loaded model
embeddings = use_model([sentence])
print(embeddings)

sentence2 = "The quick brown fox jumps over the lazy dog."
sentence3 = "A speedy brown fox leaps over the sleepy dog."


embeddings = use_model([sentence2, sentence3])

similarity_score = tf.keras.losses.cosine_similarity(embeddings[0], embeddings[1]).numpy()

print(f"Similarity between the two sentences: {similarity_score}")

#download USE wala folder readme file madhun 
