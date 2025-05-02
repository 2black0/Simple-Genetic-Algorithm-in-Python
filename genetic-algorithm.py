import numpy as np
import datetime

def create_gen(panjang_target):
    """
    Generate a random gene string of specified length.
    
    Args:
        panjang_target (int): Length of the target string/gene to generate
        
    Returns:
        str: Random gene string with ASCII characters (32-125)
    """
    random_number = np.random.randint(32, 126, size=panjang_target)
    gen = ''.join([chr(i) for i in random_number])
    return gen

def calculate_fitness(gen, target, panjang_target):
    """
    Calculate fitness score by comparing gene with target string.
    
    Args:
        gen (str): Gene string to evaluate
        target (str): Target string to compare against
        panjang_target (int): Length of the target string
        
    Returns:
        float: Fitness percentage (0-100) representing match quality
    """
    fitness = 0
    for i in range(panjang_target):
        if gen[i:i+1] == target[i:i+1]:
            fitness += 1
    fitness = fitness / panjang_target * 100
    return fitness

def create_population(target, max_population, panjang_target):
    """
    Create initial population of random genes with their fitness scores.
    
    Args:
        target (str): Target string
        max_population (int): Maximum number of individuals in population
        panjang_target (int): Length of target string
        
    Returns:
        dict: Dictionary mapping genes to their fitness scores
    """
    populasi = {}
    for i in range(max_population):
        gen = create_gen(panjang_target)
        genfitness = calculate_fitness(gen, target, panjang_target)
        populasi[gen] = genfitness
    return populasi

def selection(populasi):
    """
    Select the two best genes from population based on fitness.
    
    Args:
        populasi (dict): Dictionary mapping genes to fitness scores
        
    Returns:
        dict: Dictionary with two best genes and their fitness scores
    """
    pop = dict(populasi)
    parent = {}
    for i in range(2):
        gen = max(pop, key=pop.get)
        genfitness = pop[gen]
        parent[gen] = genfitness
        if i == 0:
            del pop[gen]  # Remove first best to find second best
    return parent

def crossover(parent, target, panjang_target):
    """
    Perform crossover between parent genes to create offspring.
    
    Args:
        parent (dict): Dictionary with parent genes and fitness scores
        target (str): Target string
        panjang_target (int): Length of target string
        
    Returns:
        dict: Dictionary with child genes and their fitness scores
    """
    child = {}
    cp = round(len(list(parent)[0])/2)  # Crossover point at middle of gene
    for i in range(2):
        # Create child by combining first half of one parent with second half of other
        gen = list(parent)[i][:cp] + list(parent)[1-i][cp:]
        genfitness = calculate_fitness(gen, target, panjang_target)
        child[gen] = genfitness
    return child

def mutation(child, target, mutation_rate, panjang_target):
    """
    Apply random mutations to child genes based on mutation rate.
    
    Args:
        child (dict): Dictionary with child genes and fitness scores
        target (str): Target string
        mutation_rate (float): Probability of mutation for each character (0-1)
        panjang_target (int): Length of target string
        
    Returns:
        dict: Dictionary with mutated genes and their fitness scores
    """
    mutant = {}
    for i in range(len(child)):     
        data = list(list(child)[i])
        for j in range(len(data)):
            if np.random.rand(1) <= mutation_rate:
                ch = chr(np.random.randint(32, 126))  # Generate random ASCII character
                data[j] = ch  # Replace character with mutated one
        gen = ''.join(data)
        genfitness = calculate_fitness(gen, target, panjang_target)
        mutant[gen] = genfitness
    return mutant

def regeneration(mutant, populasi):
    """
    Create new population by replacing worst genes with mutant genes.
    
    Args:
        mutant (dict): Dictionary with mutant genes
        populasi (dict): Current population dictionary
        
    Returns:
        dict: Updated population with mutants replacing worst genes
    """
    for i in range(len(mutant)):
        bad_gen = min(populasi, key=populasi.get)  # Find gene with lowest fitness
        del populasi[bad_gen]  # Remove worst gene
    populasi.update(mutant)  # Add mutant genes to population
    return populasi

def bestgen(parent):
    """
    Get best gene from a population/parent dictionary.
    
    Args:
        parent (dict): Dictionary mapping genes to fitness scores
        
    Returns:
        str: Gene with highest fitness score
    """
    gen = max(parent, key=parent.get)
    return gen

def bestfitness(parent):
    """
    Get highest fitness score from population/parent dictionary.
    
    Args:
        parent (dict): Dictionary mapping genes to fitness scores
        
    Returns:
        float: Highest fitness score in population
    """
    fitness = parent[max(parent, key=parent.get)]
    return fitness

def display(parent):
    """
    Display current best gene, its fitness, and elapsed time.
    
    Args:
        parent (dict): Dictionary with parent genes
    """
    timeDiff = datetime.datetime.now() - startTime
    print('{}\t{}%\t{}'.format(bestgen(parent), round(bestfitness(parent), 2), timeDiff))

# Main program configuration
target = 'Hello World!'      # Target string to evolve towards
max_population = 10          # Size of population in each generation
mutation_rate = 0.2          # Probability of gene mutation (20%)

# Display configuration parameters
print('Target Word :', target)
print('Max Population :', max_population)
print('Mutation Rate :', mutation_rate)

# Initialize genetic algorithm
panjang_target = len(target)
startTime = datetime.datetime.now()
print('----------------------------------------------')
print('{}\t{}\t{}'.format('The Best', 'Fitness', 'Time'))
print('----------------------------------------------')

# Create initial population and select parents
populasi = create_population(target, int(max_population), panjang_target)
parent = selection(populasi)

# Display initial best parent
display(parent)

# Main evolution loop
while 1:
    # Create offspring through crossover and mutation
    child = crossover(parent, target, panjang_target)
    mutant = mutation(child, target, float(mutation_rate), panjang_target)
    
    # Skip if no improvement
    if bestfitness(parent) >= bestfitness(mutant):
        continue
    
    # Update population with improved mutants
    populasi = regeneration(mutant, populasi)
    parent = selection(populasi)
    display(parent)
    
    # Exit condition: perfect match found
    if bestfitness(mutant) >= 100:
        break