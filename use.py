import tensorflow as tf

saved_dir = 'USE'
use_model = tf.saved_model.load(saved_dir)

paragraph2 = ["The exploration of the universe has been a source of fascination for humans throughout history. Scientists and astronomers are committed to delving into the secrets of the cosmos, striving to decipher the enigmatic nature of the stars that adorn our night sky. Technological progress, coupled with the development of sophisticated telescopes and space exploration tools, has propelled our comprehension of far-off galaxies and planetary systems. The quest for understanding the cosmos serves not only as a catalyst for scientific breakthroughs but also as a conduit for marvel and appreciation, fostering a profound connection to the magnificence of the universe."]
paragraph1 = ["Exploring the vast expanse of the universe is an endeavor that has captivated human curiosity for centuries. Scientists and astronomers dedicate their careers to unraveling the mysteries of the cosmos, seeking to comprehend the celestial bodies that dot the night sky. With advancements in technology, telescopes, and space probes, our understanding of distant galaxies and star systems continues to expand. The pursuit of knowledge about the cosmos not only fuels scientific discovery but also instills a sense of wonder and awe, connecting us to the grandeur of the universe."]  # Replace with actual sentences

# Combine all sentences into a single list
all_sentences = paragraph1 + paragraph2

# Get embeddings for all sentences
embeddings = use_model(all_sentences)

# Separate embeddings for each paragraph
embeddings_paragraph1 = embeddings[:len(paragraph1)]
embeddings_paragraph2 = embeddings[len(paragraph1):]

# Calculate cosine similarity between each sentence in paragraph1 and every sentence in paragraph2
similarity_matrix = tf.linalg.matmul(
    tf.math.l2_normalize(embeddings_paragraph1, axis=1),
    tf.math.l2_normalize(embeddings_paragraph2, axis=1),
    transpose_b=True
)

# Display the similarity matrix
print("Similarity Matrix:")
print(similarity_matrix.numpy())

max_similarity_scores = tf.reduce_max(similarity_matrix, axis=1).numpy()
print("Maximum Similarity Scores for Each Sentence in Paragraph1:")
print(max_similarity_scores)

