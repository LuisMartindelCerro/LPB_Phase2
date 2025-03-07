import numpy as np
import re
import sys

# Error correction in case of wring unmber of inputs
if len(sys.argv) != 2:
        print("Error: Exactly one argument expected (input file). Provided arguments: {}".format(len(sys.argv) - 1))
        print("Usage: python script.py <input_file>")
        sys.exit(1)


input_file = sys.argv[1]

def parse_input_file(filename):

    with open(filename, 'r') as file:
        content = file.read()
    
    # Extract variables using regex
    try:
        mut = list(map(int, re.search(r'mut\s*=\s*([\d,]+)', content).group(1).split(',')))
    except AttributeError:
        raise ValueError("Error: Missing or incorrect format for 'mut'")
    
    try:
        l = int(re.search(r'l\s*=\s*(\d+)', content).group(1))
    except AttributeError:
        raise ValueError("Error: Missing or incorrect format for 'l'")
    
    try:
        g = int(re.search(r'g\s*=\s*(\d+)', content).group(1))
    except AttributeError:
        raise ValueError("Error: Missing or incorrect format for 'g'")
    
    try:
        b = int(re.search(r'b\s*=\s*(\d+)', content).group(1))
    except AttributeError:
        raise ValueError("Error: Missing or incorrect format for 'b'")

    return mut, l, g, b

mut, l, g, b = parse_input_file(input_file)

#Calculate mean number of mutation rate, calculated as the sum of mutations divided by the lenght of genome (l) times the number of generations (g)
MeanObservedMR = np.sum(mut) / (l * g)        


 #Initialize bootstrap empty list to store the calculated MR for each bootstrap round
bootstrap_mr = []

#For loop through the number of bootstrap replicates requested (stored in b)
for i in range(b):      
    
    #For each replicate, choose random mutations numbers with the same size as mut vector. replace = True for allow choosing the same number more than one time 
    resample_mutations = np.random.choice(mut, size=len(mut), replace=True )
    #Calculate Mutation rate for each replicate
    resample_MR = np.sum(resample_mutations) / (l * g)
    #Append it to the list  
    bootstrap_mr.append(resample_MR)      
                        
#Calculate confidence intervals
ci_lower, ci_upper = np.percentile(bootstrap_mr, [2.5, 97.5])   

 #Create output file to write the results in
with open("output_I.txt", "w") as file:  

    print(f"Observed Mutation Rate: {MeanObservedMR:.2e}", file= file)
    print(f"95% Confidence Interval: [{ci_lower:.1e}, {ci_upper:.1e}]", file= file)
