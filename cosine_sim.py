import nltk
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')  

def cosine_similarity_between_sentences(sentence1, sentence2):
    # Tokenize and vectorize the sentences
    vectorizer = CountVectorizer().fit_transform([sentence1, sentence2])
    vectors = vectorizer.toarray()

    # Calculate the cosine similarity between the vectors
    cosine_sim = cosine_similarity(vectors[0].reshape(1, -1), vectors[1].reshape(1, -1))[0][0]

    return cosine_sim


sentence1 = "The quick brown fox jumps over the lazy dog."
sentence2 = "A fast brown fox leaps over a sleepy dog."
similarity_score = cosine_similarity_between_sentences(sentence1, sentence2)
print("Cosine Similarity:", similarity_score)

