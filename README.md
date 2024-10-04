# Mithril Pricing Intelligence Platform (RAG-Based PoC)

## Overview

This project demonstrates the implementation of a Pricing Intelligence Platform using Azure OpenAI and Azure AI Search in a **Retrieval-Augmented Generation (RAG)** framework. The goal is to enable business stakeholders to access real-time pricing insights independently, leveraging embedded and vectorized data to reduce reliance on technical teams and accelerate decision-making.

## Project Structure

mithril_pricing_project/

│

├── scripts/

│ ├── CRM_RAG.py # Main RAG script for interacting with the pricing intelligence platform

│ ├── file_chunking_dynamic.py # Script for chunking CRM and customer data

│ ├── indexing.py # Azure AI Search index creation script

│ ├── upload_chunks.py # Uploads the chunked data to Azure AI Search

│ └── env_setup.py # Sets up the Azure and OpenAI environment configurations

│

├── data/

│ ├── enriched_customers_data.md # Customer data in markdown format

│ ├── fully_enriched_crm_data.md # CRM data in markdown format

│ ├── chunks/ # Directory where chunked data is stored

│ │ ├── customer_chunks/ # Chunked customer data
   
│ │ └── crm_chunks/ # Chunked CRM data

│

├── README.md # Documentation file

├── requirements.txt # Python packages required

├── config/

│ └── .env # Environment variables file (see below)

## Prerequisites

1. **Python 3.7+**
2. **Azure OpenAI Service** with deployment of GPT-4 and an embedding model.
3. **Azure AI Search** with two indexes: one for customer data and one for CRM data.

## Installation

1. Clone the repository:
<div style="background-color:#545352; padding: 10px; border-radius: 5px;">

git clone <https://github.com/your_username/mithril_pricing_project.git>

cd mithril_pricing_project

</div>
2. Install the required Python libraries:
<div style="background-color:#545352; padding: 10px; border-radius: 5px;">

pip install -r requirements.txt
</div>


## Environment Variables

The .env file must include the following configuration:

<div style="background-color:#545352; padding: 10px; border-radius: 5px;">

#### # Azure and OpenAI Configurations
AZURE_SEARCH_SERVICE_ENDPOINT=&lt;your-search-service-endpoint&gt;
AZURE_SEARCH_SERVICE_ADMIN_KEY=&lt;your-search-service-admin-key&gt;
SEARCH_CUSTOMER_INDEX_NAME=mithril-customer-index
SEARCH_CRM_INDEX_NAME=mithril-crm-index

AZURE_OPENAI_ENDPOINT=&lt;your-openai-endpoint&gt;
AZURE_OPENAI_API_KEY=&lt;your-openai-api-key&gt;

AZURE_OPENAI_CHAT_COMPLETIONS_DEPLOYMENT_NAME=gpt-4o
AZURE_OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

EMBEDDING_VECTOR_DIMENSIONS=1536

</div>


Ensure to replace &lt;your-search-service-endpoint&gt;, &lt;your-search-service-admin-key&gt;, &lt;your-openai-endpoint&gt;, and &lt;your-openai-api-key&gt; with the correct values.

## Running the Project 

1. **Create Azure AI Search Indexes**: Use the indexing.py script to create the required indexes (mithril-customer-index and mithril-crm-index):
<div style="background-color:#545352; padding: 10px; border-radius: 5px;">

python scripts/indexing.py
</div>

2. **Chunk the Data**: The file_chunking_dynamic.py script processes the markdown files into chunks for efficient retrieval by Azure AI Search:
<div style="background-color:#545352; padding: 10px; border-radius: 5px;">

python scripts/file_chunking_dynamic.py
</div>

3. **Upload the Chunked Data**: The upload_chunks.py uploads the chunked data into Azure AI Search:
<div style="background-color:#545352; padding: 10px; border-radius: 5px;">

python scripts/upload_chunks.py
</div>
4. **Run the RAG Pricing Intelligence Platform**: Execute the RAG.py script to initiate the Retrieval-Augmented Generation (RAG) process:
<div style="background-color:#545352; padding: 10px; border-radius: 5px;">

python scripts/RAG.py
</div>
This will prompt you to enter your query, which will be answered using the vectorized data stored in the Azure AI Search indexes.

**Example Queries**

1. **Price and Trend Queries**:
    - "What was the average price of Mithril over the last 6 months?"
    - "How has the price of Mithril fluctuated across different regions?"
2. **Demand and Supply Analysis**:
    - "Which regions have the highest demand for Mithril?"
    - "How does the supply from Khazad-dûm compare with the demand from Lothlórien?"
3. **Geopolitical and Economic Impact**:
    - "Explain how political instability in Mirkwood affected their ability to purchase Mithril."

**Sample Query and Output**

**Query: "What was the average price of Mithril over the last 6 months?"**

Response:

To calculate the average price of Mithril over the last 6 months, we need to consider the adjusted price per unit from the orders delivered within that timeframe. Here are the relevant orders and their adjusted prices:

1. \*\*Order ORD026\*\*: Adjusted price per unit is 45000.0 USD, delivered on 2024-05-21 .

2. \*\*Order ORD027\*\*: Adjusted price per unit is 60000.0 USD, delivered on 2024-06-14 .

3. \*\*Order ORD029\*\*: Adjusted price per unit is 60000.0 USD, delivered on 2024-09-26 .

4. \*\*Order ORD033\*\*: Adjusted price per unit is 60000.0 USD, delivered on 2024-05-05 .

5. \*\*Order ORD035\*\*: Adjusted price per unit is 60000.0 USD, delivered on 2024-05-21 .

Therefore, the average price of Mithril over the last 6 months is \*\*57000.0 USD\*\*.

**Project Highlights**

1. **RAG Framework**: Implements the Retrieval-Augmented Generation (RAG) approach, utilizing GPT-4 for accurate, context-rich answers based on retrieved vectorized data from Azure AI Search.
2. **Scalable Design**: The platform is designed to scale, providing real-time, self-service insights to business stakeholders without requiring constant technical support.
3. **Azure Integration**: Leverages both **Azure OpenAI** for natural language understanding and **Azure AI Search** for efficient, accurate retrieval of data.

**Next Steps**

This project can be expanded by:

1. **Optimizing Search Results**: Fine-tuning the embeddings and vector retrieval to improve the precision of results.
2. **Integrating BI Dashboards**: Visualizing the outputs and insights for a more interactive business-facing experience.
3. **Adding More Datasets**: Incorporating additional datasets such as transportation costs, supply chain data, or geopolitical risks to further enrich the insights.

This README file gives a comprehensive overview of the project from setup to execution, detailing all the key steps and information necessary to get the RAG-based Pricing Intelligence platform running.