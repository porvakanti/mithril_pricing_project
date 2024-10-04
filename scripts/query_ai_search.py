
from scripts.query_simulation import simulate_user_query

def request_user_query(openai_client, search_client, embedding_model):
    query = input("Enter your query: ")
    results = simulate_user_query(query, search_client, openai_client, embedding_model)
    print(f"Search Results: {results}")
