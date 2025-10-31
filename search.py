from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import whoosh
import os


# Schema: company_name (text), index (id)
schema = Schema(company_name=TEXT(stored=True), index=ID(stored=True, unique=True))

#  insert panda frame into whoosh index
# data is at 'BTS 2025 Company Names.xlsx'
import pandas as pd
df = pd.read_excel('BTS 2025 Company Names.xlsx')
# remove duplicates based on 'Company Name' column
df = df.drop_duplicates(subset=['Company Name'])
index_dir = 'whoosh_index'
if not os.path.exists(index_dir):
    os.mkdir(index_dir)
ix = create_in(index_dir, schema)
writer = ix.writer()
for i, row in df.iterrows():
    writer.add_document(company_name=row['Company Name'], index=str(i))
writer.commit()

# load company location json from location_output.txt
import json
locations = {}
# json load file
with open('locations_output.txt', 'r') as f:
    locations = json.load(f)
print(f"Loaded locations for {len(locations)} companies.")
# query with company_name from locations_output.txt and get index from whoosh index
ix = whoosh.index.open_dir(index_dir)
with ix.searcher() as searcher:
    parser = QueryParser("company_name", ix.schema)
    for company in locations.keys():
        query = parser.parse(company)
        results = searcher.search(query)
        if results:
            print(f"Company: {company}, Index: {results[0]['index']}, Locations: {locations[company]}")
        else:
            print(f"Company: {company} not found in index.")
        # append the location data to the row in BTW dataframe (eg. company_name, location1, location2, location3...)
        if results:
            idx = int(results[0]['index'])
            locs = locations[company]
            for j, loc in enumerate(locs):
                df.at[idx, f'location{j+1}'] = loc
# save dataframe to new excel file
df.to_excel('BTS 2025 Company Names with Locations.xlsx', index=False)