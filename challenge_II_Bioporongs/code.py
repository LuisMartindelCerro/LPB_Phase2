import sys
import requests
from xml.etree import ElementTree

def fetch_gene_ids(organism):
    # URL to the NCBI Entrez API for gene information
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # Parameters to search for genes of a given organism
    params = {
        "db": "gene",  # Search the gene database
        "term": f"{organism}[Organism]",  # Use more specific query with [Organism]
        "retmode": "xml",  # Get results in XML format
        "retmax": 5000,  # Set the maximum number of results to 5000
        "retstart": 0  # Start at the first record
    }
    
    gene_ids = []
    
    while True:
        # Send request to NCBI Entrez API
        response = requests.get(url, params=params)

        # If the request was successful
        if response.status_code == 200:
            # Parse the XML data
            root = ElementTree.fromstring(response.text)
            # Find all gene IDs from the XML response
            ids = root.findall(".//Id")
            
            # If no IDs were found, print a message
            if not ids:
                print("Warning: No gene IDs found in the response!")
            
            gene_ids.extend([gene_id.text for gene_id in ids])
            
            # Check if we have received less than the requested `retmax` number of results
            if len(ids) < params['retmax']:
                break  # Exit if we have received the last batch
            else:
                # If there are more results, increase `retstart` to fetch the next batch
                params['retstart'] += params['retmax']
        else:
            raise Exception(f"Failed to fetch data from NCBI. HTTP status code: {response.status_code}")
    
    print(f"Total gene IDs retrieved: {len(gene_ids)}")
    return gene_ids

def fetch_gene_names(gene_ids):
    # URL for retrieving detailed gene information
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    
    # List to store gene names
    gene_names = []
    
    # Process gene IDs in batches of 500
    for i in range(0, len(gene_ids), 500):
        batch_ids = gene_ids[i:i+500]  # Get a batch of 500 IDs
        ids_str = ",".join(batch_ids)  # Join the IDs into a comma-separated string
        
        # Parameters to send the gene IDs for detailed information
        params = {
            "db": "gene",
            "id": ids_str,  # Send a batch of IDs
            "retmode": "xml"
        }
        
        # Send POST request for ELink
        response = requests.post(url, data=params)

        if response.status_code == 200:
            gene_info_root = ElementTree.fromstring(response.text)
            for docsum in gene_info_root.findall(".//DocSum"):
                # Extract the gene name from the response
                gene_name = docsum.find(".//Item[@Name='Name']")
                if gene_name is not None:
                    gene_names.append(gene_name.text)
            # Debug: Print how many gene names we got in this batch
            print(f"Fetched {len(gene_names)} gene names so far.")
        else:
            raise Exception(f"Failed to fetch gene details. HTTP status code: {response.status_code}")
    
    return gene_names

def write_genes_to_file(gene_names, output_file):
    # Write gene names to the output file
    with open(output_file, 'w') as file:
        for gene in gene_names:
            file.write(gene + '\n')

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
        
        # Fetch gene names based on the retrieved gene IDs
        print(f"Fetching gene names for {organism}...")
        gene_names = fetch_gene_names(gene_ids)
        
        if not gene_names:
            print("No gene names retrieved. Exiting...")
            sys.exit(1)
        
        # Write gene names to the output file
        write_genes_to_file(gene_names, output_file)
        
        print(f"Gene names for {organism} have been written to {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
