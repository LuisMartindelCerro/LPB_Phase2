import sys
import requests
from xml.etree import ElementTree

def fetch_gene_names(organism):
    # URL to the NCBI Entrez API for gene information
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    
    # Parameters to search for genes of a given organism
    params = {
        "db": "gene",  # Search the gene database
        "term": organism,  # Organism name provided as input
        "retmode": "xml",  # Get results in XML format
        "retmax": "1000"  # Max number of results to fetch, adjust as needed
    }
    
    # Send request to NCBI Entrez API
    response = requests.get(url, params=params)
    
    # If the request was successful
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Failed to fetch data from NCBI. HTTP status code: {response.status_code}")

def extract_gene_names(xml_data):
    # Parse the XML data
    root = ElementTree.fromstring(xml_data)
    
    # Find all gene IDs from the XML response
    gene_ids = root.findall(".//Id")
    
    # List of gene names to be returned
    gene_names = []
    
    for gene_id in gene_ids:
        # Fetch details for each gene
        gene_info_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        params = {
            "db": "gene",
            "id": gene_id.text,
            "retmode": "xml"
        }
        
        # Get gene details
        gene_info_response = requests.get(gene_info_url, params=params)
        
        if gene_info_response.status_code == 200:
            gene_info_root = ElementTree.fromstring(gene_info_response.text)
            gene_name = gene_info_root.find(".//Name")
            
            if gene_name is not None:
                gene_names.append(gene_name.text)
    
    return gene_names

def write_genes_to_file(gene_names, output_file):
    # Write gene names to the output file
    with open(output_file, 'w') as file:
        for gene in gene_names:
            file.write(gene + '\n')

def main():
    # Ensure we have the correct number of arguments
    if len(sys.argv) != 3:
        print("Usage: python my_program.py <Organism Name> <Output File Path>")
        sys.exit(1)

    # Get the organism name and output file path from the command line arguments
    organism = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Fetch gene names from the Entrez API
        print(f"Fetching gene names for {organism}...")
        xml_data = fetch_gene_names(organism)
        
        # Extract the gene names
        gene_names = extract_gene_names(xml_data)
        
        # Write gene names to the output file
        write_genes_to_file(gene_names, output_file)
        
        print(f"Gene names for {organism} have been written to {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
    