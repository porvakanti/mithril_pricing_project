from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    VectorSearchProfile,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticSearch,
    SemanticField
)
import os
from dotenv import load_dotenv

def create_mithril_index(type):

    # Load environment variables from .env
    load_dotenv()

    # Set up the Azure Search service endpoint and key
    endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
    api_key = os.getenv("AZURE_SEARCH_SERVICE_ADMIN_KEY")
    customer_index_name = os.getenv("SEARCH_CUSTOMER_INDEX_NAME")
    crm_index_name = os.getenv("SEARCH_CRM_INDEX_NAME")

    credential = AzureKeyCredential(api_key)
    search_index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

    if type=='customer':
        print("CREATING CUSTOMER INDEX")
        print("***********************")
        result = create_customer_index(customer_index_name, search_index_client)
        return result
    else:
        print("CREATING CRM INDEX")
        print("***********************")
        result = create_crm_index(crm_index_name, search_index_client)
        return result


def create_customer_index(customer_index_name, search_index_client):
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            sortable=True,
            filterable=True,
            facetable=True,
        ),
        SearchField(name="CustomerID", type=SearchFieldDataType.String, sortable=True, filterable=True,
                    facetable=True),
        SearchField(name="Name", type=SearchFieldDataType.String),
        SearchField(name="Region", type=SearchFieldDataType.String, sortable=True, filterable=True,
                    facetable=True),
        SearchField(name="Realm", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="Clan", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="Contact", type=SearchFieldDataType.String),
        SearchField(name="GeopoliticalIndex", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="EconomicHealthIndex", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="PreferredSeason", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="TransportationCostUSD", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="description", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), searchable=True,
                    vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile"),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnsw")],
        profiles=[VectorSearchProfile(name="myHnswProfile", algorithm_configuration_name="myHnsw")]
    )

    semantic_config = SemanticConfiguration(
        name="customer-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(title_field=SemanticField(field_name="Name"),
                                                     content_fields=[SemanticField(field_name="Region"),
                                                                     SemanticField(field_name="Realm")])
    )

    semantic_search = SemanticSearch(configurations=[semantic_config])

    customer_index = SearchIndex(name=customer_index_name, fields=fields, vector_search=vector_search,
                                 semantic_search=semantic_search)

    result = search_index_client.create_or_update_index(customer_index)
    print(f'Customer Index {result.name} created')
    return result


def create_crm_index(crm_index_name, search_index_client):
    fields = [
        SimpleField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            sortable=True,
            filterable=True,
            facetable=True,
        ),
        SearchField(name="OrderID", type=SearchFieldDataType.String, sortable=True, filterable=True,
                    facetable=True),
        SearchField(name="CustomerID", type=SearchFieldDataType.String, filterable=True,
                    facetable=True),
        SearchField(name="OfferID", type=SearchFieldDataType.String),
        SearchField(name="OrderDate", type=SearchFieldDataType.String),
        SearchField(name="DeliveryDate", type=SearchFieldDataType.String),
        SearchField(name="DeliveryFrom", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="DeliveryTo", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="Quantity", type=SearchFieldDataType.Int32, filterable=True),
        SearchField(name="PricePerUnitUSD", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="TotalPriceUSD", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="Mine", type=SearchFieldDataType.String, sortable=True, filterable=True,
                    facetable=True),
        SearchField(name="MineLocation", type=SearchFieldDataType.String, sortable=True, filterable=True,
                    facetable=True),
        SearchField(name="MineCapacity", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="DemandIndex", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="SupplyIndex", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="Season", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="GeopoliticalIndex", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="TransportationCostUSD", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="EconomicHealthIndex", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="AdjustedPricePerUnitUSD", type=SearchFieldDataType.Double, filterable=True),
        SearchField(name="description", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single), searchable=True,
                    vector_search_dimensions=1536, vector_search_profile_name="myHnswProfileCRM"),
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnswCRM")],
        profiles=[VectorSearchProfile(name="myHnswProfileCRM", algorithm_configuration_name="myHnswCRM")]
    )

    # String fields only
    semantic_config = SemanticConfiguration(
        name="crm-semantic-config",
        prioritized_fields=SemanticPrioritizedFields(
            title_field=SemanticField(field_name="OrderID"),
            content_fields=[
                SemanticField(field_name="CustomerID"),
                SemanticField(field_name="Mine"),
                SemanticField(field_name="MineLocation"),
                SemanticField(field_name="Season")
            ]
        )
    )

    semantic_search = SemanticSearch(configurations=[semantic_config])

    crm_index = SearchIndex(name=crm_index_name, fields=fields, vector_search=vector_search,
                            semantic_search=semantic_search)

    result = search_index_client.create_or_update_index(crm_index)
    print(f'CRM Index {result.name} created')
    return result


if __name__ == '__main__':
    create_customer_index()
    create_crm_index()
