import sys
import requests
import re
from xml.etree import ElementTree

def fetch_gene_ids(organism):
    # URL to the NCBI Entrez API for gene information
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # Parameters to search for genes of a given organism
    params = {
        "db": "gene",  # Search the gene database
        "term": f"{organism}[Organism]",  # More specific query with [Organism]
        "retmode": "xml",  # Get results in XML format
        "retmax": 5000,  # Number of results per request
        "retstart": 0     # Start with the first record
    }
    
    gene_ids = []
    
    while True:
        # Send request to NCBI Entrez API
        response = requests.get(url, params=params)
        
        # If the request was successful
        if response.status_code == 200:
            root = ElementTree.fromstring(response.text)
            # Find all gene IDs from the XML response
            ids = root.findall(".//Id")
            
            # If no IDs were found, break the loop (no more results)
            if not ids:
                break
            
            gene_ids.extend([gene_id.text for gene_id in ids])
            
            # If the number of IDs is less than `retmax`, we are done
            if len(ids) < params['retmax']:
                break
            else:
                # Increment `retstart` to fetch the next batch of 5000 IDs
                params['retstart'] += params['retmax']
        else:
            raise Exception(f"Failed to fetch data from NCBI. HTTP status code: {response.status_code}")
    
    print(f"Total gene IDs retrieved: {len(gene_ids)}")  # Added log to confirm gene IDs fetched
    return gene_ids

def extract_gene_names_from_text(response_text):
    # Regular expression to extract gene names between <Name>...</Name>
    gene_names = re.findall(r"<Name>(.*?)</Name>", response_text)
    
    # Log the number of gene names found
    print(f"Found {len(gene_names)} gene names in this response.")
    
    # Optionally, filter out names that are not valid gene names (e.g., identifiers or unwanted symbols)
    valid_gene_names = [name for name in gene_names if is_valid_gene_name(name)]
    
    return valid_gene_names

def is_valid_gene_name(gene_name):
    # Regular expression to match valid gene names (letters, digits, dashes, and underscores)
    gene_name_pattern = r"^[A-Za-z0-9_\-]+$"
    return re.match(gene_name_pattern, gene_name) is not None

def write_genes_to_file(gene_names, output_file):
    # Write gene names to the output file
    with open(output_file, 'w') as file:
        for gene in gene_names:
            file.write(gene + '\n')

def fetch_gene_info_batch(gene_ids_batch):
    # URL to fetch gene details in batch
    gene_info_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    
    # Prepare the comma-separated list of gene IDs for the batch
    gene_ids_str = ','.join(gene_ids_batch)
    
    # Parameters for batch request
    params = {
        "db": "gene",
        "id": gene_ids_str,
        "retmode": "xml"
    }
    
    # Send request for the batch of gene IDs
    response = requests.get(gene_info_url, params=params)
    
    if response.status_code == 200:
        # Extract gene names from the response text using regex
        return extract_gene_names_from_text(response.text)
    else:
        print(f"Failed to fetch gene information for batch. HTTP status code: {response.status_code}")
        return []

def main():
    # Ensure we have the correct number of arguments
    if len(sys.argv) != 3:
        print("Error: Exactly two arguments expected ('organism' & 'output_file'). Provided arguments: {}".format(len(sys.argv) - 1))
        print("Usage: python my_program.py <Organism Name> <Output File Path>")
        sys.exit(1)

    # Get the organism name and output file path from the command line arguments
    organism = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Fetch gene IDs from the Entrez API
        print(f"Fetching gene IDs for {organism}...")
        gene_ids = fetch_gene_ids(organism)
        
        if not gene_ids:
            print("No gene IDs retrieved. Exiting...")
            sys.exit(1)
        
        # Fetch gene names in batches
        gene_names = []
        batch_size = 500  # Adjust the batch size as needed (100, 200, 500...)
        
        for i in range(0, len(gene_ids), batch_size):
            gene_ids_batch = gene_ids[i:i+batch_size]
            print(f"Processing batch {i//batch_size + 1} of size {len(gene_ids_batch)}...")
            # Fetch the gene names for this batch
            batch_gene_names = fetch_gene_info_batch(gene_ids_batch)
            gene_names.extend(batch_gene_names)
            print(f"Fetched {len(batch_gene_names)} gene names so far.")
        
        # Write gene names to the output file
        write_genes_to_file(gene_names, output_file)
        
        print(f"Gene names for {organism} have been written to {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

