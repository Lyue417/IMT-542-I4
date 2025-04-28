"""
Accessing different information structures with different technologies

This script demonstrates how to access three different information structures:
1. JSON data via API
2. XML data via direct file download 
3. CSV data via pandas library

Each function includes pros and cons of the respective access methodology.
"""

import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
from pathlib import Path

def access_json_api():
    """
    Access JSON data from a public API (Washington State Electric Vehicle data)
    
    Pros:
    - Real-time access to current data
    - No need to store large datasets locally
    - Data structure is already parsed into JSON format
    - Updates are managed by the data provider
    - JSON is lightweight and easy to work with in Python
    
    Cons:
    - Requires internet connection
    - API might have rate limits or change unexpectedly
    - No access if the API service is down
    - Response times depend on network and server conditions
    - May need to handle various error states
    """
    try:
        # Washington State Electric Vehicle data API endpoint
        api_url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.json?accessType=DOWNLOAD"
        print(f"Accessing JSON data from API: {api_url}")
        
        # Send request to API
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        # Extract and print sample data (first 3 records)
        print("\nJSON API Access Sample:")
        
        # Handle Socrata API JSON structure
        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            print(f"Total records: {len(data['data'])}")
            
            # Print first 3 records (or fewer if less available)
            sample_size = min(3, len(data["data"]))
            for i in range(sample_size):
                record = data["data"][i]
                print(f"\nRecord #{i+1}:")
                
                # Try to find columns that might contain interesting vehicle data
                for j, value in enumerate(record):
                    if j < 5:  # Limit to first 5 fields to keep output clean
                        print(f"  Field {j}: {value}")
            
            return data
        else:
            print("JSON data structure is different than expected. Sample output:")
            print(str(data)[:500] + "..." if len(str(data)) > 500 else str(data))
            return data
            
    except Exception as e:
        print(f"Error accessing JSON API: {e}")
        return None


def download_and_read_xml():
    """
    Download and read XML data (Washington State Electric Vehicle data)
    
    Pros:
    - XML provides strict data validation with defined schemas
    - Hierarchical structure can represent complex relationships
    - Human and machine readable format
    - Widely supported across platforms
    
    Cons:
    - More verbose than other formats, resulting in larger file sizes
    - Parsing can be more complex and resource-intensive
    - Requires internet connection for initial download
    - Must handle file management (saving, cleanup)
    - XML parsing libraries can vary in functionality
    """
    try:
        # XML data source URL
        xml_url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.xml?accessType=DOWNLOAD"
        temp_file = "electric_vehicle_data.xml"
        
        print(f"Downloading XML file from: {xml_url}")
        
        # Download XML file
        response = requests.get(xml_url)
        response.raise_for_status()
        
        # Save to temporary file
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        print(f"File downloaded to: {temp_file}")
        
        # Parse XML
        tree = ET.parse(temp_file)
        root = tree.getroot()
        
        # Find data rows
        rows = root.findall('.//row')
        print(f"Found {len(rows)} records in XML file")
        
        # Extract and print sample data (first 3 records)
        print("\nXML File Access Sample:")
        sample_records = []
        
        for i, row in enumerate(rows[:3]):  # Process first 3 rows
            print(f"\nRecord #{i+1}:")
            record = {}
            
            # Print first 5 fields from each record
            field_count = 0
            for child in row:
                # Remove namespace if present
                tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                if field_count < 5:  # Limit to 5 fields for clarity
                    print(f"  {tag}: {child.text}")
                    record[tag] = child.text
                    field_count += 1
            
            sample_records.append(record)
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"Temporary file {temp_file} removed")
        
        return sample_records
    
    except Exception as e:
        print(f"Error downloading and reading XML: {e}")
        return None


def access_csv_with_pandas():
    """
    Access CSV data using the pandas library (Washington State Electric Vehicle data)
    
    Pros:
    - Pandas provides powerful data manipulation capabilities
    - Efficient handling of tabular data
    - Built-in functions for analysis and statistics
    - CSV files are widely supported across most systems
    - Easy to read and understand structure
    
    Cons:
    - Requires additional pandas library installation
    - Memory intensive for large datasets
    - Lacks nested data representation compared to JSON or XML
    - May have challenges with complex data types
    - Need to handle potential CSV format variations (delimiters, encoding, etc.)
    """
    try:
        # CSV data source URL
        csv_url = "https://data.wa.gov/api/views/f6w7-q2d2/rows.csv?accessType=DOWNLOAD"
        temp_file = "electric_vehicle_data.csv"
        
        print(f"Downloading CSV file from: {csv_url}")
        
        # Download CSV file
        response = requests.get(csv_url)
        response.raise_for_status()
        
        # Save to temporary file
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        
        print(f"File downloaded to: {temp_file}")
        
        # Read CSV with pandas
        df = pd.read_csv(temp_file)
        
        # Print data overview
        print("\nCSV Pandas Access Sample:")
        print(f"Data dimensions: {df.shape} (rows, columns)")
        
        # Display column names (first 5 for brevity)
        print(f"Columns: {', '.join(df.columns[:5])}...")
        
        # Display first 3 rows
        print("\nFirst 3 records:")
        print(df.head(3).to_string())
        
        # Show some basic statistics using pandas
        print("\nBasic statistics (first numeric column):")
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            print(df[numeric_cols[0]].describe())
        
        # Clean up temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"Temporary file {temp_file} removed")
        
        return df
    
    except Exception as e:
        print(f"Error accessing CSV with pandas: {e}")
        return None


if __name__ == "__main__":
    print("Accessing different information structures with different technologies")
    print("=" * 80)
    
    # 1. Access JSON data via API
    print("\n1. JSON DATA VIA API")
    print("-" * 80)
    json_data = access_json_api()
    
    # 2. Download and read XML data
    print("\n\n2. XML DATA VIA DOWNLOAD")
    print("-" * 80)
    xml_data = download_and_read_xml()
    
    # 3. Access CSV data using pandas
    print("\n\n3. CSV DATA VIA PANDAS LIBRARY")
    print("-" * 80)
    csv_data = access_csv_with_pandas()
    
    print("\n\nAll data access methods completed.")