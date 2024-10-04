
def perform_vector_search(openai_client, search_client, vector_query):
    #results = search_client.search(search_text="", vector=vector_query, top=5)
    #return [result['chunk_content'] for result in results]

    #print(vector_query)
    results = search_client.search(
        search_text=None,
        vector_queries=[vector_query],
        select=["page_title", "page_date", "chunk_title", "chunk_content"],
    )

    # Print the total count
    #print(f"Total count: {results.get_count()}")

    #for result in results:
    #    print(f"Page Date: {result['page_date']}")
    #    print(f"Page Title: {result['page_title']}")
    #    print(f"Chunk Title: {result['chunk_title']}")
    #    print(f"Chunk Content: {result['chunk_content']}")
    #    print(f"Score: {result['@search.score']}")

    return results

# Example usage:
# vector_query = get_embeddings_vector("Sample query text")
# results = perform_vector_search(search_client, vector_query)
