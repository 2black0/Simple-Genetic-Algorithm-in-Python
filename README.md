# 🧬 Simple Genetic Algorithm in Python

This project demonstrates how to implement a **Genetic Algorithm (GA)** from scratch in Python — a fun way to mimic natural selection and evolve solutions. The goal is to guess a target string using random populations, fitness evaluation, selection, crossover, mutation, and population regeneration.

> Why Python? Because I love it.  
> Hate Python? That's your problem 😛

---

## 📦 Requirements

Make sure to install the only dependency:

```bash
pip install numpy
```

---

## 📊 Genetic Algorithm Flow

A Genetic Algorithm simulates the process of natural evolution to solve optimization problems. The main components are:

1. **Initialization** – Create a random population of possible solutions (strings).
2. **Selection** – Pick the fittest individuals from the population.
3. **Crossover** – Combine parts of parents to produce offspring.
4. **Mutation** – Randomly tweak offspring to introduce diversity.
5. **Evaluation** – Stop if the target is reached or continue to next generation.
6. **Regeneration** – Replace the worst individuals with new ones.

### 🧭 Flowchart Overview

![GA Flowchart](https://cdn-images-1.medium.com/max/1600/1*HP8JVxlJtOv14rGLJfXEzA.png)

---

## 🔧 Step-by-Step Implementation

### 1. Initialize Population

A **population** is a collection of individuals, called **genes**. Each gene is a random string.

```python
def create_gen(panjang_target):
    random_number = np.random.randint(32, 126, size=panjang_target)
    return ''.join([chr(i) for i in random_number])
```

Each gene’s fitness is evaluated against the target string.

```python
def calculate_fitness(gen, target, panjang_target):
    matches = sum([1 for i in range(panjang_target) if gen[i] == target[i]])
    return (matches / panjang_target) * 100
```

All genes are stored with their fitness in a dictionary:

```python
def create_population(target, max_population, panjang_target):
    populasi = {}
    for _ in range(max_population):
        gen = create_gen(panjang_target)
        populasi[gen] = calculate_fitness(gen, target, panjang_target)
    return populasi
```

---

### 2. Selection

Choose the two best genes (with the highest fitness values):

```python
def selection(populasi):
    pop = dict(populasi)
    parent = {}
    for _ in range(2):
        gen = max(pop, key=pop.get)
        parent[gen] = pop[gen]
        del pop[gen]
    return parent
```

---

### 3. Crossover

Mix the selected parents to create two children by swapping halves:

```python
def crossover(parent, target, panjang_target):
    cp = round(panjang_target / 2)
    p = list(parent)
    return {
        p[0][:cp] + p[1][cp:]: calculate_fitness(p[0][:cp] + p[1][cp:], target, panjang_target),
        p[1][:cp] + p[0][cp:]: calculate_fitness(p[1][:cp] + p[0][cp:], target, panjang_target)
    }
```

---

### 4. Mutation

Introduce diversity by randomly changing characters with a certain mutation rate:

```python
def mutation(child, target, mutation_rate, panjang_target):
    mutant = {}
    for c in child:
        data = list(c)
        for j in range(len(data)):
            if np.random.rand() <= mutation_rate:
                data[j] = chr(np.random.randint(32, 126))
        gen = ''.join(data)
        mutant[gen] = calculate_fitness(gen, target, panjang_target)
    return mutant
```

---

### 5. Evaluation and Stopping Criteria

Check if the best individual has reached the target (100% fitness):

```python
if bestfitness(mutant) >= 100:
    break
```

---

### 6. Regeneration

Replace the weakest genes in the population with the newly mutated ones:

```python
def regeneration(mutant, populasi):
    for _ in mutant:
        bad_gen = min(populasi, key=populasi.get)
        del populasi[bad_gen]
    populasi.update(mutant)
    return populasi
```

---

## 🧪 Example Output

```txt
Target Word : Hello World!
Max Population : 10
Mutation Rate : 0.2
----------------------------------------------
The Best        Fitness     Time
----------------------------------------------
HgUewI]W*f`     15.38%      0:00:00.003001
Helpo Worsd!    84.61%      0:00:01.003120
Hello World!    100.0%      0:00:01.994801
```

---

## ▶️ Run the Program

```bash
python genetic_algorithm.py
```

Edit the config at the top of the file:

```python
target = 'Hello World!'
max_population = 10
mutation_rate = 0.2
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Ardy Seto Priambodo**
📧 [2black0@gmail.com](mailto:2black0@gmail.com)

---

## 📚 References

* Goldberg, D. E., *Genetic Algorithms in Search, Optimization, and Machine Learning*
* Mitchell, M., *An Introduction to Genetic Algorithms*
