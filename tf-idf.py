from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords_tfidf(text, num_keywords=5):
    # Create a TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer(max_features=num_keywords)

    # Fit and transform the text
    tfidf_matrix = tfidf_vectorizer.fit_transform([text])

    # Get feature names (words) and their TF-IDF scores
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.toarray()[0]

    # Create a dictionary of keywords and their TF-IDF scores
    keywords = {feature_names[i]: tfidf_scores[i] for i in range(len(feature_names))}

    # Sort keywords by TF-IDF score in descending order
    sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)

    # Get the top N keywords
    top_keywords = [keyword[0] for keyword in sorted_keywords[:num_keywords]]

    return top_keywords

if __name__ == "__main__":
    # Example text
    text = """
    Natural language processing (NLP) is a subfield of artificial intelligence that focuses on the interaction
    between computers and humans through natural language. NLP techniques can be used for various tasks 
    like text classification, sentiment analysis, and keyword extraction. Keyword extraction is crucial for 
    summarizing and understanding the main themes in a text.
    """

    # Extract the top 5 keywords based on TF-IDF
    keywords = extract_keywords_tfidf(text, num_keywords=5)

    # Print the extracted keywords
    print("Top 5 Keywords (TF-IDF):", keywords)
