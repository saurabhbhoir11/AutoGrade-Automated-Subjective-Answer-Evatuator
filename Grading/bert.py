from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Define the student's answer and model answer
student_answer = "The quick brown fox jumps over the lazy dog."
model_answer = "A fast brown fox leaps over a lazy canine."

# Tokenize and encode the answers
student_tokens = tokenizer(student_answer, return_tensors="pt")
model_tokens = tokenizer(model_answer, return_tensors="pt")

# Get BERT embeddings
student_outputs = model(**student_tokens)
model_outputs = model(**model_tokens)

# Extract the embeddings for the [CLS] token, which typically represents the entire sequence
student_embedding = student_outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
model_embedding = model_outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()

# Calculate cosine similarity
similarity = 1 - cosine(student_embedding, model_embedding)

print(f"Similarity between student and model answer: {similarity}")
