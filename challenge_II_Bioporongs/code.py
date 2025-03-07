import sys
from Bio import Entrez

def fetch_gene_names(organism):
    # Use NCBI Entrez API to search for genes related to the given organism
    Entrez.email = "luismdc55@gmail.com"  # Always provide your email to NCBI when using their API
    handle = Entrez.esearch(db="gene", term=organism, retmode="xml", retmax=1000)  # Maximum of 1000 genes
    results = Entrez.read(handle)
    handle.close()
    
    # Extract gene IDs from the search result
    gene_ids = results["IdList"]
    
    return gene_ids

def fetch_gene_details(gene_ids):
    # Use NCBI Entrez API to get the gene names from gene IDs
    gene_names = []
    
    if gene_ids:
        handle = Entrez.esummary(db="gene", id=",".join(gene_ids), retmode="xml")
        results = Entrez.read(handle)
        handle.close()
        
        for gene in results:
            gene_name = gene.get("Name")
            if gene_name:
                gene_names.append(gene_name)
    
    return gene_names

def write_genes_to_file(gene_names, output_file):
    # Write the gene names to an output file, one gene per line
    with open(output_file, 'w') as file:
        for gene in gene_names:
            file.write(gene + '\n')

def main():
    # Ensure we have the correct number of arguments
    if len(sys.argv) != 2:
        print("Usage: python my_program.py <Organism Name> <Output File Path>")
        sys.exit(1)

    # Get the organism name and output file path from the command line arguments
    organism = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        # Fetch gene IDs for the organism
        print(f"Fetching gene names for {organism}...")
        gene_ids = fetch_gene_names(organism)
        
        # Fetch gene names from the gene IDs
        gene_names = fetch_gene_details(gene_ids)
        
        # Write gene names to the output file
        write_genes_to_file(gene_names, output_file)
        
        print(f"Gene names for {organism} have been written to {output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()