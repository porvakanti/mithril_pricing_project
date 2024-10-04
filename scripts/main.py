
from scripts.env_setup import setup_clients
from scripts.query_ai_search import request_user_query
from file_chunking_dynamic import chunk_file
from indexing import create_mithril_index
from upload_chunks import upload_chunks_to_search
from query_simulation import simulate_user_query

def check_openai_embedding(openai_client, embedding_model):
    test_text = "This is a test."
    try:
        response = openai_client.embeddings.create(
            input=test_text,
            model=embedding_model
        )
        print("Embedding generated successfully:", response)
    except Exception as e:
        print(f"Error in embedding generation: {e}")


def main():
    # Setup clients for querying
    # openai_client, search_client, _, embedding_model, _ = setup_clients()

    # Setup clients
    (openai_client, search_customer_client, search_crm_client, search_index_client,
     azure_openai_embedding_model, search_customer_index_name,
     search_crm_index_name, azure_search_service_admin_key) = setup_clients()

    # Call the test function with your client and model
    # check_openai_embedding(openai_client, embedding_model)

    # Step 1: Create search index
    # create_search_index(search_index_client, search_index_name)
    # create_customer_index()
    # create_crm_index()
    print("Step 1: Creating search index")
    create_mithril_index('customer')
    create_mithril_index('crm')

    # Step 2: Chunk files and upload them to Azure AI Search
    # chunk_file('data', 'data/chunks', openai_client, azure_openai_embedding_model)
    # Call chunking for Customer data
    print("Step 2: Chunking files")
    chunk_file('data/customers', 'data/chunks', openai_client, azure_openai_embedding_model,
               search_index_client, search_customer_index_name)

    # Call chunking for CRM data
    chunk_file('data/crm', 'data/chunks', openai_client, azure_openai_embedding_model,
               search_index_client, search_crm_index_name)

    print("Step 3: uploading chunks to Azure AI Search")
    upload_chunks_to_search(search_customer_client, 'data/chunks/customer_chunks')
    upload_chunks_to_search(search_crm_client, 'data/chunks/crm_chunks')

    # Step 3: Simulate a user query
    query = "Explain Azure AI"
    #results = simulate_user_query(query, search_client, openai_client, embedding_model)
    #print(f"Search Results: {results}")

    # Prompt user for query input and retrieve results
    #request_user_query(openai_client, search_client, embedding_model)

if __name__ == '__main__':
    main()
