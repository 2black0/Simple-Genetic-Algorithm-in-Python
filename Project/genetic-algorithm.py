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
    # Generate random ASCII values between 32-125 (printable characters)
    random_number = np.random.randint(32, 126, size=panjang_target)
    # Convert ASCII values to characters and join them into a string
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
    # Count matching characters at corresponding positions
    for i in range(panjang_target):
        if gen[i:i+1] == target[i:i+1]:
            fitness += 1
    # Convert to percentage (0-100)
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
    # Generate specified number of random genes
    for i in range(max_population):
        gen = create_gen(panjang_target)
        # Calculate and store fitness score for each gene
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
    # Create a copy to avoid modifying the original dictionary
    pop = dict(populasi)
    parent = {}
    # Select the two genes with highest fitness scores
    for i in range(2):
        gen = max(pop, key=pop.get)  # Gene with highest fitness
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
    # Set crossover point at middle of gene
    cp = round(len(list(parent)[0])/2)
    
    # Create two children by swapping parts of parents
    for i in range(2):
        # Create child by combining first half of one parent with second half of other
        gen = list(parent)[i][:cp] + list(parent)[1-i][cp:]
        # Calculate fitness of new child
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
    # Process each child gene
    for i in range(len(child)):     
        data = list(list(child)[i])  # Convert gene string to character list
        # Potentially mutate each character in the gene
        for j in range(len(data)):
            # Apply mutation based on mutation rate probability
            if np.random.rand(1) <= mutation_rate:
                ch = chr(np.random.randint(32, 126))  # Generate random ASCII character
                data[j] = ch  # Replace character with mutated one
        # Convert back to string and calculate new fitness
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
    # Remove worst genes from population (equal to number of mutants)
    for i in range(len(mutant)):
        bad_gen = min(populasi, key=populasi.get)  # Find gene with lowest fitness
        del populasi[bad_gen]  # Remove worst gene
        
    # Add new mutant genes to population
    populasi.update(mutant)
    return populasi

def bestgen(parent):
    """
    Get best gene from a population/parent dictionary.
    
    Args:
        parent (dict): Dictionary mapping genes to fitness scores
        
    Returns:
        str: Gene with highest fitness score
    """
    # Find and return gene with maximum fitness
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
    # Return the highest fitness value
    fitness = parent[max(parent, key=parent.get)]
    return fitness

def display(parent):
    """
    Display current best gene, its fitness, and elapsed time.
    
    Args:
        parent (dict): Dictionary with parent genes
    """
    # Calculate elapsed time since algorithm start
    timeDiff = datetime.datetime.now() - startTime
    # Print best gene, fitness score, and elapsed time
    print('{}\t{}%\t{}'.format(bestgen(parent), round(bestfitness(parent), 2), timeDiff))

# =====================================================
# Main Program: Genetic Algorithm Implementation
# =====================================================

# Configuration parameters
target = 'Hello World!'      # Target string to evolve towards
max_population = 10          # Size of population in each generation
mutation_rate = 0.2          # Probability of gene mutation (20%)

# Display configuration parameters
print('Target Word :', target)
print('Max Population :', max_population)
print('Mutation Rate :', mutation_rate)

# Initialize algorithm parameters
panjang_target = len(target)  # Length of target string
startTime = datetime.datetime.now()  # Record start time

# Set up results display header
print('----------------------------------------------')
print('{}\t{}\t{}'.format('The Best', 'Fitness', 'Time'))
print('----------------------------------------------')

# Initialize the genetic algorithm process
# Step 1: Create initial random population
populasi = create_population(target, int(max_population), panjang_target)

# Step 2: Select initial parents (best two genes)
parent = selection(populasi)

# Display the initial best gene
display(parent)

# Main evolution loop - continues until perfect match is found
while 1:
    # Step 3: Create offspring through crossover (mating)
    child = crossover(parent, target, panjang_target)
    
    # Step 4: Apply random mutations to offspring
    mutant = mutation(child, target, float(mutation_rate), panjang_target)
    
    # Skip iteration if no improvement in fitness
    if bestfitness(parent) >= bestfitness(mutant):
        continue
    
    # Step 5: Update population by replacing worst genes with improved mutants
    populasi = regeneration(mutant, populasi)
    
    # Step 6: Select new parents from updated population
    parent = selection(populasi)
    
    # Display current best solution
    display(parent)
    
    # Exit condition: perfect match found (100% fitness)
    if bestfitness(mutant) >= 100:
        break