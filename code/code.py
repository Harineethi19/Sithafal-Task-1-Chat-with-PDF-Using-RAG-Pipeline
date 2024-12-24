import fitz  # PyMuPDF for PDF parsing
import pandas as pd

# Function to extract text from a specific page
def extract_text_from_page(doc, page_number):
    page = doc[page_number - 1]  # Page numbers are 0-indexed
    text = page.get_text("text")
    return text

# Function to extract unemployment information from page 2
def get_unemployment_info(doc):
    text = extract_text_from_page(doc, 2)
    # Example parsing logic for unemployment rates by degree
    unemployment_data = {}
    for line in text.splitlines():
        if "degree" in line.lower():
            parts = line.split(":")
            if len(parts) == 2:
                degree, rate = parts
                unemployment_data[degree.strip()] = rate.strip()
    return unemployment_data

# Function to extract tabular data from page 6
def get_table_data(doc):
    text = extract_text_from_page(doc, 6)
    # Extract table rows
    rows = []
    for line in text.splitlines():
        row = line.split()
        if len(row) > 1:  # Basic heuristic for a table row
            rows.append(row)
    # Convert rows to a DataFrame
    if len(rows) > 1:
        df = pd.DataFrame(rows[1:], columns=rows[0])  # Assuming first row is the header
    else:
        df = pd.DataFrame()  # Empty DataFrame if no table found
    return df

# Main function for online compiler
def main():
    # Upload PDF file
    pdf_path = input("Enter the path to your PDF file (uploaded): ").strip()

    try:
        with fitz.open(pdf_path) as doc:
            # Extract unemployment information
            unemployment_info = get_unemployment_info(doc)
            print("Unemployment Information:", unemployment_info)

            # Extract tabular data
            table_data = get_table_data(doc)
            if not table_data.empty:
                print("\nTable Data:")
                print(table_data)
            else:
                print("\nNo table data found on page 6.")
    except Exception as e:
        print(f"Error processing the file: {e}")

# Run the main function
if __name__ == "__main__":
    main()

