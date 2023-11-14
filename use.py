import tensorflow as tf


saved_dir = 'USE'

use_model = tf.saved_model.load(saved_dir)

sentences = [
    "My name is suyash.",
    "That boy's name is suyash.",
    "He studies in APSIT."
]

embeddings = use_model(sentences)



for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        similarity_score = tf.tensordot(embeddings[i], embeddings[j], axes=1).numpy()
        print(f"Similarity between '{sentences[i]}' and '{sentences[j]}': {similarity_score:.4f}")
        