import re
import pandas as pd
from google import genai
filename = 'BTS 2025 Company Names.xlsx'
df = pd.read_excel(filename)
company_names = df['Company Name'].tolist()
unique_company_names = sorted(list(set(company_names)))
# for each company name, call gemini api to get locations
client = genai.Client()
locations = {}
batch_size = 20
for i in range(0, len(unique_company_names), batch_size):
    batch = unique_company_names[i:i+batch_size]
    prompt = "List all locations for each of the following companies in JSON format:\n"
    for company in batch:
        prompt += f"{company}:[LOCATION1, LOCATION2, LOCATION3, ...]\n"
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )
    if not response or not response.text:
        raise ValueError("No response from the model")
    response_text = response.text.strip()
    # write response to file
    with open('locations_output.txt', 'a') as f:
        f.write(response_text + '\n')