import uuid
import json
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from scripts.tokenizer import num_tokens_from_string
from scripts.embeddings import get_embeddings_vector
from scripts.file_processing import clean_markdown_content
from datetime import datetime

# Function to check if a string is a valid date (format: YYYY-MM-DD)
def is_date(string):
    try:
        datetime.strptime(string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Function to check if a string is a valid time (format: HH:MM:SS or similar)
def is_time(string):
    try:
        datetime.strptime(string, "%H:%M:%S.%f")  # Time format with microseconds
        return True
    except ValueError:
        try:
            datetime.strptime(string, "%H:%M:%S")  # Time format without microseconds
            return True
        except ValueError:
            return False


def get_index_schema(search_client, index_name):
    """
    Retrieves the schema of the specified Azure Search index and returns a dictionary
    mapping field names to their data types (e.g., Edm.String, Edm.Double).
    """
    schema = search_client.get_index(index_name)
    field_types = {}

    for field in schema.fields:
        field_types[field.name] = field.type

    return field_types


def cast_value_to_type(value, field_type):
    """
    Casts the given value to the type specified by the field_type.
    For example, if the field_type is Edm.Double, cast the value to float.
    """
    if value is None or value == '':
        return None  # Handle missing or empty values
    try:
        if field_type == "Edm.Int32":
            return int(value)
        elif field_type == "Edm.Double":
            # Ensure the value is a valid float before casting
            return float(value) if is_float(value) else value
        elif field_type == 'Edm.Boolean':
            return value.lower() in ('true', '1')
        elif field_type == "Edm.String":
            return str(value)
        else:
            # Default to string for unsupported types
            return str(value)
    except ValueError as e:
        print(f"Warning: Could not convert {value} to {field_type} due to {e}. Treating as string.")
        return str(value)

def is_float(value):
    """
    Helper function to check if a value can be converted to a float.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

def generate_customer_description(customer_data):
    """Generate a text description for a customer record."""
    return (
        f"Customer {customer_data.get('Name', 'Unknown')} with ID of {customer_data.get('CustomerID', 'Unknown-')}, "
        f" belonging to CSU {customer_data.get('CSU', 'Unknown')}, "
        f"from the {customer_data.get('Clan', 'Unknown')} clan "
        f"in the {customer_data.get('Realm', 'Unknown')} realm, resides in the {customer_data.get('Region', 'Unknown')} "
        f"region. They have a geopolitical index of {customer_data.get('GeopoliticalIndex', 'N/A')} and an economic "
        f"health index of {customer_data.get('EconomicHealthIndex', 'N/A')}. Their preferred season is {customer_data.get('PreferredSeason', 'Unknown')}, and "
        f"the transportation cost associated with deliveries is {customer_data.get('TransportationCostUSD', 'Unknown')} USD."
    )


def generate_crm_description(crm_data):
    """Generate a text description for a CRM record."""
    return (
        f"Order {crm_data.get('OrderID', 'Unknown')} placed by customer {crm_data.get('CustomerID', 'Unknown')}, "
        f" belonging to CSU {crm_data.get('CSU', 'Unknown')}, "
        f"was delivered from {crm_data.get('DeliveryFrom', 'Unknown')} to {crm_data.get('DeliveryTo', 'Unknown')} on "
        f"{crm_data.get('DeliveryDate', 'Unknown')}. The order consists of {crm_data.get('Quantity', 'Unknown')} units of Mithril "
        f"priced at {crm_data.get('PricePerUnitUSD', 'Unknown')} USD per unit, totaling {crm_data.get('TotalPriceUSD', 'Unknown')} USD. "
        f"The order was sourced from {crm_data.get('Mine', 'Unknown')} mine, located at {crm_data.get('MineLocation', 'Unknown')}, "
        f"which has a capacity of {crm_data.get('MineCapacity', 'Unknown')}. The demand index is {crm_data.get('DemandIndex', 'N/A')}, "
        f"supply index is {crm_data.get('SupplyIndex', 'N/A')}, and geopolitical index is {crm_data.get('GeopoliticalIndex', 'N/A')}. "
        f"The adjusted price per unit is {crm_data.get('AdjustedPricePerUnitUSD', 'Unknown')} USD."
    )


def chunk_file(input_directory, output_directory, openai_client, embedding_model, search_client, index_name, max_tokens=8191):
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

    # Fetch the index schema from Azure Search
    field_types = get_index_schema(search_client, index_name)
    print(f"Field types: {field_types}")

    # Create separate directories for Customer and CRM chunks if applicable
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

                    # Split content into rows
                    rows = content.split('\n')

                    # Parse the header, ensuring each column is treated as a single entity between pipes
                    header = [h.strip() for h in rows[0].split('|') if h.strip()]  # Handle empty columns safely

                    # Skip the second row (table separator) and process the data rows
                    for row in rows[2:]:
                        if not row.strip():  # Skip empty rows
                            continue

                        chunk_index += 1

                        # Use the pipes to split row values correctly, handling multiword values.
                        row_data = [r.strip() for r in row.split('|') if r.strip()]

                        if len(row_data) != len(header):
                            print(f"Skipping malformed row: {row}")
                            continue

                        # Initialize fields dictionary for this row
                        fields = {}

                        # Map header to row_data while maintaining the correct column-value mapping
                        for i, column_name in enumerate(header):
                            value = row_data[i] if i < len(row_data) else None  # Handle missing values
                            fields[column_name] = cast_value_to_type(value, field_types.get(column_name, "Edm.String"))

                        # Get the embedding vector for the chunk
                        vector = get_embeddings_vector(json.dumps(fields), openai_client, embedding_model)

                        # create the description for the chunk/row
                        description = ""
                        if 'customer' in filename.lower():
                            description = generate_customer_description(fields)
                        else:
                            description = generate_crm_description(fields)

                        # Create the chunk data
                        chunk_data = {
                            "id": str(uuid.uuid4()),
                            'fields': fields,
                            'description': description,
                            'vector': vector
                        }

                        # Clean and format the chunk file name
                        chunk_file_name = f'chunk_{chunk_index}_{filename.replace(".md", "")}.json'.replace('?', '').replace(':', '').replace("'", '').replace('|', '').replace('/', '').replace('\\', '')

                        # Write chunk into JSON file in the appropriate directory (Customer or CRM based on file type)
                        if 'customer' in filename.lower():
                            output_dir = customer_output_dir
                        else:
                            output_dir = crm_output_dir

                        with open(os.path.join(output_dir, chunk_file_name), 'w') as f:
                            json.dump(chunk_data, f)

    print("***************")


# Example usage:
# chunk_file('data', 'data/chunks', openai_client, embedding_model, search_client, 'crm-index')
