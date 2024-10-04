import uuid
import json
import os
from scripts.tokenizer import num_tokens_from_string
from scripts.embeddings import get_embeddings_vector
from scripts.file_processing import clean_markdown_content

def chunk_file(input_directory, output_directory, openai_client, embedding_model, max_tokens=8191):
    # Get the absolute path of the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Script is located in: {script_directory}")

    # Construct the full path to the data and output directories relative to the project root
    project_root = os.path.abspath(os.path.join(script_directory, '..'))  # Go one level up to the project root
    input_directory = os.path.join(project_root, input_directory)
    output_directory = os.path.join(project_root, output_directory)

    # Debugging: Print both input and output directory paths
    print(f"Input directory: {input_directory}")
    print(f"Output directory: {output_directory}")

    # Check if the input directory exists
    if not os.path.exists(input_directory):
        print(f"Input directory does not exist: {input_directory}")
        return

    # Create separate directories for Customer and CRM chunks
    customer_output_dir = os.path.join(output_directory, 'customer_chunks')
    crm_output_dir = os.path.join(output_directory, 'crm_chunks')

    # Create directories if they don't exist
    if not os.path.exists(customer_output_dir):
        os.makedirs(customer_output_dir)
    if not os.path.exists(crm_output_dir):
        os.makedirs(crm_output_dir)

    print(f"Chunking Files in: {input_directory}")
    print("***************")

    chunk_index = 0
    # List files in the directory and log them for debugging
    files_in_directory = os.listdir(input_directory)
    if not files_in_directory:
        print(f"No files found in directory: {input_directory}")
        return
    else:
        print(f"Files found: {files_in_directory}")

    for filename in files_in_directory:
        if filename.endswith('.md'):
            file_path = os.path.join(input_directory, filename)
            print(f"Processing file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

                # Split content by rows (lines separated by newlines)
                rows = content.split('\n')

                # Assuming the first row is the header, capture it
                header = rows[0].replace('|', '').strip()  # Clean the header by removing unwanted symbols

                # Process each row, combining it with the header
                for row in rows[1:]:
                    chunk_index += 1
                    row = row.replace('|', '').strip()  # Clean each row by removing unwanted symbols
                    chunk_content = f"{header}\n{row}"  # Combine header with the row

                    chunk_content = clean_markdown_content(chunk_content.strip())

                    if num_tokens_from_string(chunk_content) > max_tokens:
                        print(f'Chunk {chunk_index} in file {filename} has more than {max_tokens} tokens')
                        continue

                    # Determine if the chunk is for Customers or CRM based on the presence of unique fields
                    if 'Name' in chunk_content or 'Region' in chunk_content:  # Fields specific to Customer data
                        fields = extract_customer_fields(chunk_content)
                        chunk_output_dir = customer_output_dir
                    elif 'OrderID' in chunk_content or 'Mine' in chunk_content:  # Fields specific to CRM data
                        fields = extract_crm_fields(chunk_content)
                        chunk_output_dir = crm_output_dir
                    else:
                        print(f"Chunk {chunk_index} in file {filename} doesn't match Customer or CRM data")
                        continue

                    # Get the embedding vector for the chunk
                    vector = get_embeddings_vector(str(fields), openai_client, embedding_model)

                    # Create the chunk data
                    chunk_data = {
                        "id": str(uuid.uuid4()),
                        'fields': fields,  # Only fields
                        'vector': vector  # Embedding vector based on the fields
                    }

                    # Clean and format the chunk file name
                    chunk_file_name = f'chunk_{chunk_index}_{filename.replace(".md", "")}.json'.replace('?', '').replace(':', '').replace("'", '').replace('|', '').replace('/', '').replace('\\', '')

                    # Write chunk into JSON file in the appropriate directory
                    with open(os.path.join(chunk_output_dir, chunk_file_name), 'w') as f:
                        json.dump(chunk_data, f)

    print("***************")

def extract_customer_fields(content):
    # Example function to extract customer fields from the content
    customer_data = {}
    lines = content.split('\n')
    for line in lines:
        if 'CustomerID' in line:
            customer_data['CustomerID'] = line.split(':')[-1].strip()
        if 'Name' in line:
            customer_data['Name'] = line.split(':')[-1].strip()
        if 'Region' in line:
            customer_data['Region'] = line.split(':')[-1].strip()
        if 'Realm' in line:
            customer_data['Realm'] = line.split(':')[-1].strip()
        if 'Clan' in line:
            customer_data['Clan'] = line.split(':')[-1].strip()
        if 'Contact' in line:
            customer_data['Contact'] = line.split(':')[-1].strip()
        if 'GeopoliticalIndex' in line:
            customer_data['GeopoliticalIndex'] = line.split(':')[-1].strip()
        if 'EconomicHealthIndex' in line:
            customer_data['EconomicHealthIndex'] = line.split(':')[-1].strip()
        if 'PreferredSeason' in line:
            customer_data['PreferredSeason'] = line.split(':')[-1].strip()
        if 'TransportationCostUSD' in line:
            customer_data['TransportationCostUSD'] = line.split(':')[-1].strip()
    return customer_data


def extract_crm_fields(content):
    # Example function to extract CRM fields from the content
    crm_data = {}
    lines = content.split('\n')
    for line in lines:
        if 'OrderID' in line:
            crm_data['OrderID'] = line.split(':')[-1].strip()
        if 'CustomerID' in line:
            crm_data['CustomerID'] = line.split(':')[-1].strip()
        if 'OfferID' in line:
            crm_data['OfferID'] = line.split(':')[-1].strip()
        if 'OrderDate' in line:
            crm_data['OrderDate'] = line.split(':')[-1].strip()
        if 'DeliveryDate' in line:
            crm_data['DeliveryDate'] = line.split(':')[-1].strip()
        if 'DeliveryFrom' in line:
            crm_data['DeliveryFrom'] = line.split(':')[-1].strip()
        if 'DeliveryTo' in line:
            crm_data['DeliveryTo'] = line.split(':')[-1].strip()
        if 'Quantity' in line:
            crm_data['Quantity'] = line.split(':')[-1].strip()
        if 'PricePerUnitUSD' in line:
            crm_data['PricePerUnitUSD'] = line.split(':')[-1].strip()
        if 'TotalPriceUSD' in line:
            crm_data['TotalPriceUSD'] = line.split(':')[-1].strip()
        if 'Mine' in line:
            crm_data['Mine'] = line.split(':')[-1].strip()
        if 'MineLocation' in line:
            crm_data['MineLocation'] = line.split(':')[-1].strip()
        if 'MineCapacity' in line:
            crm_data['MineCapacity'] = line.split(':')[-1].strip()
        if 'DemandIndex' in line:
            crm_data['DemandIndex'] = line.split(':')[-1].strip()
        if 'SupplyIndex' in line:
            crm_data['SupplyIndex'] = line.split(':')[-1].strip()
        if 'Season' in line:
            crm_data['Season'] = line.split(':')[-1].strip()
        if 'GeopoliticalIndex' in line:
            crm_data['GeopoliticalIndex'] = line.split(':')[-1].strip()
        if 'TransportationCostUSD' in line:
            crm_data['TransportationCostUSD'] = line.split(':')[-1].strip()
        if 'EconomicHealthIndex' in line:
            crm_data['EconomicHealthIndex'] = line.split(':')[-1].strip()
        if 'AdjustedPricePerUnitUSD' in line:
            crm_data['AdjustedPricePerUnitUSD'] = line.split(':')[-1].strip()
    return crm_data


# Example usage:
# chunk_file('../data', '../data/chunks/', openai_client, embedding_model)
