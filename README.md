# Company Location Fetcher

A Python project that uses Google's Gemini AI to automatically fetch and enrich company location data from an Excel spreadsheet.

## Overview

This project processes a list of company names from an Excel file, uses the Gemini API to fetch their locations, and creates an enriched dataset with location information. It also builds a searchable index using Whoosh for efficient company lookups.

## Features

- **AI-Powered Location Fetching**: Uses Google Gemini 2.5 Flash to automatically retrieve company locations
- **Batch Processing**: Processes companies in batches of 20 for efficient API usage
- **Full-Text Search**: Creates a Whoosh index for fast company name searches
- **Data Enrichment**: Merges location data back into the original Excel file
- **Deduplication**: Automatically removes duplicate company entries

## Project Structure

```
.
├── gemini_location_fetcher.py    # Fetches locations using Gemini API
├── search.py                     # Creates search index and merges data
├── BTS 2025 Company Names.xlsx   # Input data file
├── company_locations.csv         # CSV export of locations
├── locations_output.txt          # Raw API responses
├── whoosh_index/                 # Search index directory (ignored in git)
└── BTS 2025 Company Names with Locations.xlsx  # Output file
```

## Prerequisites

- Python 3.7+
- Google Gemini API access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd denna
```

2. Install required dependencies:
```bash
pip install pandas openpyxl google-generativeai whoosh
```

3. Set up your Gemini API credentials according to the [Google AI Python SDK documentation](https://github.com/google/generative-ai-python).

## Usage

### Step 1: Fetch Company Locations

Run the location fetcher to query Gemini API for company locations:

```bash
python gemini_location_fetcher.py
```

This script will:
- Read company names from `BTS 2025 Company Names.xlsx`
- Process unique company names in batches of 20
- Query Gemini API for each batch
- Save responses to `locations_output.txt`

### Step 2: Index and Merge Data

Process the fetched locations and merge them with the original data:

```bash
python search.py
```

This script will:
- Create a Whoosh search index from company names
- Load location data from `locations_output.txt`
- Match locations to companies using the search index
- Add location columns to the dataframe
- Export enriched data to `BTS 2025 Company Names with Locations.xlsx`

## Input Format

The input Excel file should have a column named `Company Name` containing the list of companies to process.

## Output Format

The output Excel file includes:
- All original columns from the input file
- Additional columns: `location1`, `location2`, `location3`, etc. (one column per location)

## Configuration

You can modify the following parameters in `gemini_location_fetcher.py`:

- `batch_size`: Number of companies to process per API call (default: 20)
- `model`: Gemini model to use (default: "models/gemini-2.5-flash")

## Notes

- The `whoosh_index/` directory is ignored in git as it can be regenerated
- Location data is appended to `locations_output.txt`, so delete this file before a fresh run
- The script removes duplicate company names before processing