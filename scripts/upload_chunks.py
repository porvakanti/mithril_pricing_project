import os
import json


def upload_chunks_to_search(search_client, chunk_directory):
    print("Uploading to AI Search")
    print("**********************")

    # Resolve the absolute path to the chunk directory
    script_directory = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_directory, '..'))
    chunk_directory = os.path.join(project_root, chunk_directory)

    # Check if chunk directory exists
    if not os.path.exists(chunk_directory):
        print(f"Chunk directory does not exist: {chunk_directory}")
        return

    # Loop through all the chunk files in the directory
    for filename in os.listdir(chunk_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(chunk_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as chunk_file:
                chunk_data = json.load(chunk_file)

                # Unpack the fields and vector for individual upload
                document = chunk_data['fields']  # Unpack all key-value pairs from the 'fields'
                document['vector'] = chunk_data['vector']  # Add the vector to the document
                document['id'] = chunk_data['id']
                document['description'] = chunk_data['description']

                # Upload each document (normal upload)
                try:
                    result = search_client.upload_documents(documents=[document])
                    print(f"Upload of {filename} succeeded: {result[0].succeeded}")
                except Exception as e:
                    print(f"Failed to upload chunk {filename}: {e}")

    # Uncomment below for batch upload
    """
    # Batch upload logic
    documents = []
    for filename in os.listdir(chunk_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(chunk_directory, filename)
            with open(file_path, 'r', encoding='utf-8') as chunk_file:
                chunk_data = json.load(chunk_file)
                document = chunk_data['fields']
                document['vector'] = chunk_data['vector']
                document['id'] = chunk_data['id']
                documents.append(document)

    # Perform batch upload
    if documents:
        try:
            upload_result = search_client.upload_documents(documents=documents)
            for result in upload_result:
                print(f"Upload of document succeeded: {result.succeeded}")
        except Exception as e:
            print(f"Failed to upload documents in batch: {e}")
    else:
        print("No chunks found to upload in batch.")
    """
    print("**********************")

# Example usage:
# upload_chunks_to_search(search_customer_client, 'data/chunks/customer_chunks')
# upload_chunks_to_search(search_crm_client, 'data/chunks/crm_chunks')
