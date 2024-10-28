import pandas as pd
import random

# Generate a fake CRM dataset with additional 'CSU' column
def generate_crm_data(num_rows=3400):
    customer_names = [
        'Frodo Baggins', 'Samwise Gamgee', 'Aragorn', 'Legolas', 'Gimli', 'Gandalf', 'Boromir', 'Merry Brandybuck',
        'Pippin Took', 'Elrond', 'Galadriel', 'Arwen', 'Eowyn', 'Faramir', 'Bilbo Baggins', 'Saruman', 'Sauron',
        'Thorin Oakenshield', 'Bard the Bowman', 'Thranduil', 'Balin', 'Dwalin', 'Kili', 'Fili', 'Glorfindel',
        'Radagast', 'Treebeard', 'Isildur', 'Anarion', 'Celebrimbor', 'Gil-galad', 'Cirdan', 'Earendil', 'Eomer',
        'Theoden', 'Denethor', 'Gollum', 'Shelob', 'Elendil', 'Tar-Miriel', 'Pharazon', 'Halbrand', 'Adar',
        'Elros', 'Luthien', 'Beren', 'Hurin', 'Turin', 'Thingol', 'Melian', 'Maeglin', 'Turgon', 'Finrod',
        'Fingolfin', 'Finarfin', 'Feanor', 'Maedhros', 'Maglor', 'Celegorm', 'Caranthir', 'Curufin',
        'Aule', 'Yavanna', 'Manwe', 'Varda', 'Ulmo', 'Mandos', 'Melkor', 'Ungoliant', 'Silmariën', 'Tar-Ancalimon',
        'Tar-Minastir', 'Ar-Pharazon', 'Earendil', 'Idril', 'Tuor', 'Voronwe', 'Ecthelion', 'Glorfindel', 'Ancalagon',
        'Glaurung', 'Ungoliant', 'Shelob', 'Grima Wormtongue', 'Gorlim', 'Beleg', 'Mablung', 'Huan', 'Tolkien',
        'Morwen',
        'Finduilas', 'Nienor', 'Nerdanel', 'Elwing', 'Indis', 'Aredhel', 'Oropher', 'Thranduil', 'Tinfang Warble'
    ]
    regions = ['Mordor', 'Gondor', 'Rohan', 'Shire', 'Lothlórien', 'Rivendell']
    mines = ['Khazad-dûm Mine 1', 'Khazad-dûm Mine 2', 'Iron Hills Mine']
    seasons = ['Winter', 'Spring', 'Summer', 'Autumn']
    csu_options = ['North', 'South', 'East', 'West']

    data = {
        'OrderID': [f'ORD{i:03d}' for i in range(1, num_rows + 1)],
        'CustomerID': [f'CUST{random.randint(1, 100):03d}' for _ in range(num_rows)],
        'OfferID': [f'OFF{random.randint(1, 100):03d}' for _ in range(num_rows)],
        'OrderDate': pd.date_range(start='2024-01-01', periods=num_rows, freq='D').strftime('%Y-%m-%d').tolist(),
        'DeliveryDate': pd.date_range(start='2024-02-01', periods=num_rows, freq='D').strftime('%Y-%m-%d').tolist(),
        'DeliveryFrom': [random.choice(regions) for _ in range(num_rows)],
        'DeliveryTo': [random.choice(regions) for _ in range(num_rows)],
        'Quantity': [random.randint(1, 10) for _ in range(num_rows)],
        'PricePerUnitUSD': [random.uniform(45000, 60000) for _ in range(num_rows)],
        'TotalPriceUSD': [random.uniform(100000, 500000) for _ in range(num_rows)],
        'Mine': [random.choice(mines) for _ in range(num_rows)],
        'MineLocation': [random.choice(regions) for _ in range(num_rows)],
        'MineCapacity': [random.uniform(5000, 10000) for _ in range(num_rows)],
        'DemandIndex': [random.uniform(0.5, 1.5) for _ in range(num_rows)],
        'SupplyIndex': [random.uniform(0.5, 1.5) for _ in range(num_rows)],
        'Season': [random.choice(seasons) for _ in range(num_rows)],
        'GeopoliticalIndex': [random.uniform(0.5, 1.5) for _ in range(num_rows)],
        'TransportationCostUSD': [random.uniform(1000, 5000) for _ in range(num_rows)],
        'EconomicHealthIndex': [random.uniform(0.5, 1.5) for _ in range(num_rows)],
        'AdjustedPricePerUnitUSD': [random.uniform(45000, 60000) for _ in range(num_rows)],
        'CSU': [random.choice(csu_options) for _ in range(num_rows)]  # New CSU column
    }

    crm_df = pd.DataFrame(data)
    return crm_df

# Generate a fake Customers dataset with additional 'CSU' column
def generate_customers_data(num_rows=100):
    customer_names = [
        'Frodo Baggins', 'Samwise Gamgee', 'Aragorn', 'Legolas', 'Gimli', 'Gandalf', 'Boromir', 'Merry Brandybuck',
        'Pippin Took', 'Elrond', 'Galadriel', 'Arwen', 'Eowyn', 'Faramir', 'Bilbo Baggins', 'Saruman', 'Sauron',
        'Thorin Oakenshield', 'Bard the Bowman', 'Thranduil', 'Balin', 'Dwalin', 'Kili', 'Fili', 'Glorfindel',
        'Radagast', 'Treebeard', 'Isildur', 'Anarion', 'Celebrimbor', 'Gil-galad', 'Cirdan', 'Earendil', 'Eomer',
        'Theoden', 'Denethor', 'Gollum', 'Shelob', 'Elendil', 'Tar-Miriel', 'Pharazon', 'Halbrand', 'Adar',
        'Elros', 'Luthien', 'Beren', 'Hurin', 'Turin', 'Thingol', 'Melian', 'Maeglin', 'Turgon', 'Finrod',
        'Fingolfin', 'Finarfin', 'Feanor', 'Maedhros', 'Maglor', 'Celegorm', 'Caranthir', 'Curufin',
        'Aule', 'Yavanna', 'Manwe', 'Varda', 'Ulmo', 'Mandos', 'Melkor', 'Ungoliant', 'Silmariën', 'Tar-Ancalimon',
        'Tar-Minastir', 'Ar-Pharazon', 'Earendil', 'Idril', 'Tuor', 'Voronwe', 'Ecthelion', 'Glorfindel', 'Ancalagon',
        'Glaurung', 'Ungoliant', 'Shelob', 'Grima Wormtongue', 'Gorlim', 'Beleg', 'Mablung', 'Huan', 'Tolkien', 'Morwen',
        'Finduilas', 'Nienor', 'Nerdanel', 'Elwing', 'Indis', 'Aredhel', 'Oropher', 'Thranduil', 'Tinfang Warble'
    ]

    regions = ['Mordor', 'Gondor', 'Rohan', 'Shire', 'Lothlórien', 'Rivendell']
    realms = ['Elf', 'Dwarf', 'Human', 'Orc', 'Maiar', 'Hobbit']
    csu_options = ['North', 'South', 'East', 'West']

    data = {
        'CustomerID': [f'CUST{random.randint(1, 100):03d}' for _ in range(num_rows)],
        'Name': [random.choice(customer_names) for _ in range(num_rows)],
        'Region': [random.choice(regions) for _ in range(num_rows)],
        'Realm': [random.choice(realms) for _ in range(num_rows)],
        'Clan': [random.choice(realms) for _ in range(num_rows)],
        'Contact': [f'contact{random.randint(1, 100)}@mithril.com' for _ in range(num_rows)],
        'GeopoliticalIndex': [random.uniform(0.5, 1.5) for _ in range(num_rows)],
        'EconomicHealthIndex': [random.uniform(0.5, 1.5) for _ in range(num_rows)],
        'PreferredSeason': [random.choice(['Winter', 'Spring', 'Summer', 'Autumn']) for _ in range(num_rows)],
        'TransportationCostUSD': [random.uniform(1000, 5000) for _ in range(num_rows)],
        'CSU': [random.choice(csu_options) for _ in range(num_rows)]  # New CSU column
    }

    customers_df = pd.DataFrame(data)
    return customers_df

# Generate the datasets
crm_data = generate_crm_data()
customers_data = generate_customers_data()

# Save as .md files
crm_data.to_csv('fully_enriched_crm_data.md', sep='|', index=False)
customers_data.to_csv('enriched_customers_data.md', sep='|', index=False)
