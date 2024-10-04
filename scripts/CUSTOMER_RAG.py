import json
import time
import openai
from azure.search.documents import SearchClient
from scripts.embeddings import get_embeddings_vector
from scripts.env_setup import setup_clients
from scripts.vector_search import perform_vector_search
from azure.search.documents.models import VectorizedQuery


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
    """Removes internal doc references like [doc1], [doc2], etc., from the output."""
    # This function will replace all instances of [docX] with an empty string
    import re
    cleaned_content = re.sub(r"\[doc\d+\]", "", message_content)
    return cleaned_content


def format_output(response):
    """Formats the response into a more readable structure."""
    # Parse response as JSON
    response_dict = json.loads(response)

    # Extracting the relevant parts from the response
    message_content = response_dict["choices"][0]["message"]["content"]
    model = response_dict["model"]
    usage = response_dict["usage"]

    # Remove the document references like [doc1], [doc2], etc.
    message_content = remove_doc_references(message_content)  # Remove [docX] references

    # Print the formatted output
    print("Response:")
    print(message_content)


    '''
    citations = response_dict["choices"][0]["message"].get("context", {}).get("citations", [])
    formatted_citations = "\n".join([f"- {citation['content']}" for citation in citations])
    
    print("\nCitations:")
    print(formatted_citations if formatted_citations else "No citations available.")
    '''

    print("\nModel:", model)
    print("\nUsage:")
    print(f"- Completion Tokens: {usage['completion_tokens']}")
    print(f"- Prompt Tokens: {usage['prompt_tokens']}")
    print(f"- Total Tokens: {usage['total_tokens']}")

def gpt_interpret_query(openai_client, user_query):

    '''
    prompt = f"""
    You are an assistant working with a Mithril dataset. Interpret the following user query: "{user_query}".
    Identify the relevant fields (such as price, demand, customer, region, etc.) and specify the search index (CRM or Customer).
    """

    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=150
    )
    '''
    response = openai_client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "You are a helpful assistant for an AI learner."},
            {"role": "user", "content": user_query}
        ]
    )
    # Parse response as JSON
    response_dict = json.loads(response.json())

    # Extracting the relevant parts from the response
    message_content = response_dict["choices"][0]["message"]["content"]
    # model = response_dict["model"]
    # usage = response_dict["usage"]

    # Remove the document references like [doc1], [doc2], etc.
    # message_content = remove_doc_references(message_content)  # Remove [docX] references

    # Print the formatted output
    #print("Response:")
    #print(message_content)

    return message_content


def classify_query(interpretation, customer_index_name, crm_index_name):
    # Based on the interpreted query, classify it into one or more relevant indexes
    index_targets = []
    index_targets.append(customer_index_name)
    index_targets.append(crm_index_name)

    # Identify if it's related to Customer Index
    #if any(keyword in interpretation.lower() for keyword in ["customer", "region", "demand", "behavior"]):
    #    index_targets.append(customer_index_name)

    # Identify if it's related to CRM Index
    #if any(keyword in interpretation.lower() for keyword in
    #       ["price", "order", "trend", "amount", "quantity", "supply"]):
    #    index_targets.append(crm_index_name)

    return index_targets



def RAG_ai_search():
    user_query = input("Enter your query: ")

    # Setup clients (pull from env_setup.py to use environment variables instead of hardcoding)
    # openai_client, search_client, search_index_client, embedding_model, search_index_name = setup_clients()
    (openai_client, search_customer_client, search_crm_client, search_index_client,
     embedding_model, search_customer_index_name, search_crm_index_name, azure_search_service_admin_key) = setup_clients()

    # Step 1: Interpret the query using GPT-4
    # interpretation = gpt_interpret_query(openai_client, user_query)
    # print(f"Interpreted Query: {interpretation}")

    # Step 2: Classify the query into relevant index(es)
    index_targets = classify_query(user_query, search_customer_index_name, search_crm_index_name)

    # Step 3: Fetch context from all relevant indexes
    combined_context = []
    for index_name in index_targets:
        query_embedding = get_embeddings_vector(user_query, openai_client, embedding_model)
        vector_query = VectorizedQuery(vector=query_embedding, k_nearest_neighbors=50,
                                       fields="vector")
        if "customer" in index_name:
            try:
                # Use the embedding to search for relevant documents in Azure AI Search
                # relevant_docs = perform_vector_search(openai_client, search_customer_client, vector_query)
                relevant_docs = search_customer_client.search(
                    search_text=None,
                    vector_queries=[vector_query],
                    select=["CustomerID", "Name", "Region", "Realm", "Clan", "Contact",
                            "GeopoliticalIndex", "EconomicHealthIndex", "PreferredSeason",
                            "TransportationCostUSD", "description"],
                )
                if relevant_docs:
                    combined_context.extend(relevant_docs)
                if not relevant_docs:
                    print("No relevant documents found for the query.")
                    return
            except Exception as e:
                print(f"Error performing vector search: {e}")
                return

        elif "crm" in index_name:
            try:
                # Use the embedding to search for relevant documents in Azure AI Search
                # relevant_docs = perform_vector_search(openai_client, search_crm_client, vector_query)
                relevant_docs = search_crm_client.search(
                    search_text=None,
                    vector_queries=[vector_query],
                    select=["OrderID", "CustomerID", "OfferID", "OrderDate", "DeliveryDate", "DeliveryFrom", "DeliveryTo",
                            "Quantity", "PricePerUnitUSD", "TotalPriceUSD", "Mine", "MineLocation", "MineCapacity",
                            "DemandIndex", "SupplyIndex", "Season", "GeopoliticalIndex", "TransportationCostUSD",
                            "EconomicHealthIndex", "AdjustedPricePerUnitUSD", "description"],
                )
                if relevant_docs:
                    combined_context.extend(relevant_docs)
                if not relevant_docs:
                    print("No relevant documents found for the query.")
                    return
            except Exception as e:
                print(f"Error performing vector search: {e}")
                return

        '''
        if "customer" in index_name:
            try:
                search_context = search_customer_client.search(
                    search_text="",
                    vector={"value": query_embedding, "fields": "vector"}
                )

                if search_context:
                    combined_context.extend(search_context)

            except Exception as e:
                print(f"Error performing vector search: {e}")
                return

        elif "crm" in index_name:
            try:
                search_context = search_crm_client.search(
                    search_text="",
                    vector={"value": query_embedding, "fields": "vector"}
                )

                if search_context:
                    combined_context.extend(search_context)

            except Exception as e:
                print(f"Error performing vector search: {e}")
                return

        if not combined_context:
            return "No relevant data found in any search index for your query."

        '''
    '''    
    # Step 1: Convert the query into embeddings using your custom function
    print("Step 1: Convert the query into embeddings")
    query_embedding = get_embeddings_vector(user_query, openai_client, embedding_model)

    # Step 2: Perform vector search using the generated embedding
    print("Step 2: Perform vector search using the generated embedding")

    try:
        search_results = search_client.search(
            search_text="",  # No traditional text search
            vector={"value": query_embedding, "fields": "vector_field", "k": 5}
            # Assuming 'vector_field' is your field name
        )

        relevant_docs = [doc for doc in search_results]

        if not relevant_docs:
            print("No relevant documents found for the query.")
            return
    except Exception as e:
        print(f"Error performing vector search: {e}")
        return

    # Filter the retrieved documents for relevant and non-redundant content
    context = filter_context(relevant_docs)

    if not context:
        print("No useful context found in the retrieved documents.")
        return
    '''
    # Retry logic for calling OpenAI with the retrieved documents
    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        try:
            # Step 3: Pass the context and query to OpenAI for final answer generation
            print("Step 3: Pass the context and query to OpenAI for final answer generation")
            #print("Context: ", combined_context)
            response = openai_client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for users, "
                                                  "who want to understand the information related to the commodity "
                                                  "called mithril, regarding its pricing, orders, offeres, customers, "
                                                  "regions etc. use the indexes and context given to you to "
                                                  "answer the questions. You are an expert at data analysis"},
                    {"role": "user", "content": user_query},
                    {"role": "system",
                     "content": f"Here is some relevant information to help answer the query: {combined_context}"}
                ],
                extra_body={  # This ensures the extra body for Azure Search is included
                    "data_sources": [
                        {
                            "type": "azure_search",
                            "parameters": {
                                "endpoint": search_customer_client._endpoint,
                                # This pulls from the SearchClient using env vars
                                "index_name": search_customer_index_name,
                                # Use the index from the environment variables
                                "authentication": {
                                    "type": "api_key",
                                    "key": azure_search_service_admin_key
                                }
                            }
                        }
                    ]
                }
            )

            # Format and display the output
            format_output(response.json())  # Parsing response as JSON

            # Return or print the response
            return

        except openai.OpenAIError as e:
            retry_count += 1
            print(f"OpenAI error occurred: {e}. Retrying in 10 seconds... ({retry_count}/{max_retries})")
            time.sleep(10)  # Wait for 10 seconds before retrying

            if retry_count >= max_retries:
                print("Max retries exceeded. Exiting...")
                break


if __name__ == '__main__':
    RAG_ai_search()
