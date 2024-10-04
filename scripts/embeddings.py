
def get_embeddings_vector(text, openai_client, embedding_model):
    response = openai_client.embeddings.create(
        input=text,
        model=embedding_model,
    )
    embedding = response.data[0].embedding
    return embedding

# Example usage:
# vector = get_embeddings_vector("Sample text", openai_client, azure_openai_embedding_model)
