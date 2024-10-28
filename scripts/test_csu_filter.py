import openai
from scripts.env_setup import setup_clients
def test_csu_filter():
    (openai_client, search_customer_client, search_crm_client, search_index_client,
     embedding_model, search_customer_index_name, search_crm_index_name, azure_search_service_admin_key) = setup_clients()

    query = "mithril"
    try:
        relevant_docs = search_crm_client.search(
            search_text=query,
            filter="CSU eq 'Adoni'",
            select=["CSU", "description"]
        )

        for doc in relevant_docs:
            print(f"CSU: {doc['CSU']}, Description: {doc['description']}")

    except Exception as e:
        print(f"Error performing search with CSU filter: {e}")

if __name__ == '__main__':
    test_csu_filter()
