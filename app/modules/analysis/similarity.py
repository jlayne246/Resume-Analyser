from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
def compute_similarity(text1: str, text2: str) -> float:
    """Compute the cosine similarity between two texts using sentence embeddings.

    Args:
        text1 (str): The first text.
        text2 (str): The second text.

    Returns:
        float: Cosine similarity score between 0 and 1.
    """
    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)
    
    similarity_score = util.pytorch_cos_sim(embedding1, embedding2).item()
    return similarity_score