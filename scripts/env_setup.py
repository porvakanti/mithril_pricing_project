
import os
from openai import AzureOpenAI
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv, dotenv_values
from azure.core.credentials import AzureKeyCredential

def setup_clients():
    if os.path.exists('.env'):
        load_dotenv(override=True)
        config = dotenv_values('.env')
    
    azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
    azure_openai_api_key = os.getenv('AZURE_OPENAI_API_KEY')
    azure_openai_chat_completions_deployment_name = os.getenv('AZURE_OPENAI_CHAT_COMPLETIONS_DEPLOYMENT_NAME')
    azure_openai_embedding_model = os.getenv('AZURE_OPENAI_EMBEDDING_MODEL')
    
    azure_search_service_endpoint = os.getenv('AZURE_SEARCH_SERVICE_ENDPOINT')
    azure_search_service_admin_key = os.getenv('AZURE_SEARCH_SERVICE_ADMIN_KEY')
    search_customer_index_name = os.getenv('SEARCH_CUSTOMER_INDEX_NAME')
    search_crm_index_name = os.getenv('SEARCH_CRM_INDEX_NAME')

    openai_client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_api_key,
        api_version="2024-06-01"
    )

    #credential = DefaultAzureCredential()
    credential = AzureKeyCredential(azure_search_service_admin_key)
    search_customer_client = SearchClient(endpoint=azure_search_service_endpoint,
                                 credential=credential, index_name=search_customer_index_name)
    search_crm_client = SearchClient(endpoint=azure_search_service_endpoint,
                                          credential=credential, index_name=search_crm_index_name)
    search_index_client = SearchIndexClient(endpoint=azure_search_service_endpoint,
                                            credential=credential)

    return (openai_client, search_customer_client, search_crm_client,
            search_index_client, azure_openai_embedding_model, search_customer_index_name,
            search_crm_index_name, azure_search_service_admin_key)
