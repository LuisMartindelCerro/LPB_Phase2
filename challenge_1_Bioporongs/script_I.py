from input import mut,l,b,g
import numpy as np



MeanObservedMR = np.sum(mut) / (l * g)          #Calculate mean number of mutation rate, calculated as the sum of mutations divided by the lenght of genome (l) times the number of generations (g)



bootstrap_mr = []           #Initialize bootstrap empty list to store the calculated MR for each bootstrap round

for i in range(b):      #For loop through the number of bootstrap replicates requested (stored in b)
    
    resample_mutations = np.random.choice(mut, size=len(mut), replace=True )        #For each replicate, choose random mutations numbers with the same size as mut vector. replace = True for allow choosing the same number more than one time 
    resample_MR = np.sum(resample_mutations) / (l * g)      #Calculate Mutation rate for each replicate
    bootstrap_mr.append(resample_MR)        #Append it to the list
                        

ci_lower, ci_upper = np.percentile(bootstrap_mr, [2.5, 97.5])       #Calculate confidence intervals


with open("output_I.txt", "w") as file:     #Create output file to write the results in

    print(f"Observed Mutation Rate: {MeanObservedMR:.2e}", file= file)
    print(f"95% Confidence Interval: [{ci_lower:.1e}, {ci_upper:.1e}]", file= file)