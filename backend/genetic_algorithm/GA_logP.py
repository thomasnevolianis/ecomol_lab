from rdkit import Chem
import numpy as np
import time
import crossover as co
import scoring_functions as sc
import GB_GA as ga
import sys
import pickle
import random

from rdkit import rdBase


def main():
    n_tries = 5  # Adjust as needed
    population_size = 5  # Adjust as needed
    mating_pool_size = 20  # Adjust as needed
    generations = 2  # Adjust as needed
    mutation_rate = 0.05  # Adjust as needed
    co.average_size = 39.15
    co.size_stdev = 3.50
    scoring_function = sc.logP_max
    max_score = 9999.
    scoring_args = []
    seeds = np.random.randint(100_000, size=2 * n_tries)

    file_name = "ZINC_first_1000.smi"

    print('* RDKit version', rdBase.rdkitVersion)
    # ... (print other parameters)

    high_scores_list = []
    for prune_population in [True, False]:
        index = slice(0, n_tries) if prune_population else slice(n_tries, 2 * n_tries)
        temp_args = [[population_size, file_name, scoring_function, generations, mating_pool_size,
                      mutation_rate, scoring_args, max_score, prune_population] for i in range(n_tries)]
        args = []
        for x, y in zip(temp_args, seeds[index]):
            x.append(y)
            args.append(x)

        output = []
        for arg in args:
            result = ga.GA(arg)
            output.append(result)

        for i in range(n_tries):
            (scores, population, high_scores, generation) = output[i]
            smiles = Chem.MolToSmiles(population[0], isomericSmiles=True)
            high_scores_list.append(high_scores)
            print(f'{i},{scores[0]:.2f},{smiles},{generation},Graph,{prune_population}')

    pickle.dump(high_scores_list, open('test.p', 'wb'))


if __name__ == "__main__":
    main()