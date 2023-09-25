import tensorflow as tf
import tensorflow_hub as hub

# Load the Universal Sentence Encoder model
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def calculate_similarity(sentence1, sentence2):
    # Encode the sentences
    embeddings = embed([sentence1, sentence2])

    # Calculate the cosine similarity
    similarity = tf.keras.losses.cosine_similarity(embeddings[0], embeddings[1]).numpy()[0]

    return similarity

if __name__ == "__main__":
    sentence1 = input("Enter the first sentence: ")
    sentence2 = input("Enter the second sentence: ")

    similarity_score = calculate_similarity(sentence1, sentence2)
    print(f"Similarity between the two sentences: {similarity_score}")
