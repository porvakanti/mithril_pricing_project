import json
import time
import openai
from azure.search.documents import SearchClient
from scripts.embeddings import get_embeddings_vector
from scripts.env_setup import setup_clients
from scripts.vector_search import perform_vector_search
from azure.search.documents.models import VectorizedQuery

query_history = []

def filter_context(relevant_docs):
    """Filters redundant or non-informative sections from relevant documents."""
    context = []
    for doc in relevant_docs:
        content = doc.get('chunk_content', '')
        if "Next steps" in content or len(content) < 50:  # Skip common headers/footers or very short content
            continue
        context.append(content)
    return "\n".join(context) if context else None

def remove_doc_references(message_content):
    """Remove internal doc references like [doc1], [doc2], etc., from the output."""
    import re
    cleaned_content = re.sub(r"\[doc\d+\]", "", message_content)
    return cleaned_content

def format_output(response, query):
    """Format the response into a more readable structure."""
    response_dict = json.loads(response)
    message_content = response_dict["choices"][0]["message"]["content"]
    model = response_dict["model"]
    usage = response_dict["usage"]

    message_content = remove_doc_references(message_content)
    query_history.append({"query": query, "response": message_content})

    return message_content, model, usage

def RAG_ai_search(csu_name='East'):

    # This loop continues until the user explicitly types "exit"
    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ").strip()

        if user_query.lower() == 'exit':
            print("Exiting session. Goodbye!")
            break

        # Check if the user input is empty and wait for a valid query.
        if not user_query:
            print("No query provided. Please enter a query.")
            continue  # Skip GPT and go back to input loop until valid input

        # Setup clients
        (openai_client, search_customer_client, search_crm_client, search_index_client,
         embedding_model, search_customer_index_name, search_crm_index_name, azure_search_service_admin_key) = setup_clients()

        # Step 1: Interpret the query using GPT-4 (if needed, not mandatory here)

        # Step 2: Fetch documents based on the query
        combined_context = []
        for index_name in [search_customer_index_name, search_crm_index_name]:
            query_embedding = get_embeddings_vector(user_query, openai_client, embedding_model)
            vector_query = VectorizedQuery(vector=query_embedding, k_nearest_neighbors=100, fields="vector")

            try:
                if "customer" in index_name:
                    relevant_docs = search_customer_client.search(
                        search_text=None,
                        vector_queries=[vector_query],
                        filter=f"CSU eq '{csu_name}'",
                        select=["CustomerID", "Name", "Region", "Realm", "Clan", "Contact",
                                "GeopoliticalIndex", "EconomicHealthIndex", "PreferredSeason",
                                "TransportationCostUSD", "description", "CSU"]
                    )
                else:
                    relevant_docs = search_crm_client.search(
                        search_text=None,
                        vector_queries=[vector_query],
                        filter=f"CSU eq '{csu_name}'",
                        select=["OrderID", "CustomerID", "OfferID", "OrderDate", "DeliveryDate", "DeliveryFrom",
                                "DeliveryTo",
                                "Quantity", "PricePerUnitUSD", "TotalPriceUSD", "Mine", "MineLocation", "MineCapacity",
                                "DemandIndex", "SupplyIndex", "Season", "GeopoliticalIndex", "TransportationCostUSD",
                                "EconomicHealthIndex", "AdjustedPricePerUnitUSD", "description", "CSU"]
                    )

                if relevant_docs:
                    combined_context.extend(relevant_docs)
            except Exception as e:
                print(f"Error performing vector search: {e}")
                return

        # Step 3: If no documents found, inform user and skip GPT
        if not combined_context:
            print("No relevant documents found for the given query. Please try again.")
            continue  # Go back to user input prompt

        #print(f"Retrieved {len(combined_context)} documents")

        # Step 4: Prepare context for GPT-4
        combined_context_text = "\n".join([doc["description"] for doc in combined_context])
        history_text = "\n".join([f"Q: {pair['query']} R: {pair['response']}" for pair in query_history])
        #print("\nCombined context:", combined_context_text)
        #print("\nQuery History:", history_text)

        # Retry logic for calling GPT with documents
        for attempt in range(3):
            try:
                response = openai_client.chat.completions.create(
                    model='gpt-4o',
                    messages=[
                        {"role": "system", "content": "You are an AI assistant. The user has provided an input."
                                                      "Identify whether is a question or an appreciation of something else"
                                                      "and respond appropriately. Please leverage the context provided to you"
                                                      "to answer the user's questions"},
                        {"role": "user", "content": user_query},
                        {"role": "system", "content": f" Use the context provided to you. "
                                                      f"Here is the context: "
                                                      f"{combined_context_text}\nQuery History: {history_text}"}
                    ]
                )

                message_content, model, usage = format_output(response.json(), user_query)

                # Print final response
                print("\nResponse:")
                print(message_content)

                # Show model usage details
                #print("\nModel:", model)
                #print(f"Total tokens: {usage['total_tokens']}")

                break  # Exit retry loop on success
            except openai.OpenAIError as e:
                print(f"OpenAI error occurred: {e}. Retrying in 10 seconds...")
                time.sleep(10)  # Wait before retrying

        # After response, reset user query and wait for another one
        user_query = ''  # Ensure it's cleared before next loop

if __name__ == '__main__':
    RAG_ai_search()
