# Information Structure Access

This repository demonstrates accessing 3 different information structures using 3 different access technologies.

## Overview

The script `information_access.py` showcases:

1. **JSON data via API**
   - Accesses Washington State Electric Vehicle data through a REST API
   - Parses and displays results directly from the API response

2. **XML data via direct file download**
   - Downloads an XML file from Washington State's data portal
   - Parses the XML structure and displays data elements

3. **CSV data via pandas library**
   - Downloads a CSV file from Washington State's data portal
   - Uses pandas library to read, analyze and display the data

## Setup & Installation

1. Clone this repository:
- git clone https://github.com/Lyue417/IMT-542-I4.git
- cd IMT-542-I4

2. Install required packages:
- pip install requests pandas

## Running the Code

Simply run:
- python information_access.py

The script will:
1. Access JSON data through an API
2. Download and parse an XML file
3. Download and analyze a CSV file using pandas

Each method will display sample data from the Washington State Electric Vehicle dataset.
