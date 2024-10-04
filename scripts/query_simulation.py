from scripts.embeddings import get_embeddings_vector
from scripts.vector_search import perform_vector_search
from azure.search.documents.models import VectorizedQuery
def simulate_user_query(query, search_client, openai_client, embedding_model):
    embedding = get_embeddings_vector(query, openai_client, embedding_model)
    vector_query = VectorizedQuery(vector=embedding, k_nearest_neighbors=3, fields="vector")
    results = perform_vector_search(openai_client, search_client, vector_query)
    return results

# Example usage:
# results = simulate_user_query("What is Azure AI?", search_client, openai_client, azure_openai_embedding_model)
# print(results)
