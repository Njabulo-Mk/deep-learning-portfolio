import random
from Genome import Genome
from Species import Species


def speciated_offspring(genomes, population_size, compatibility_threshold, add_node_rate=0.3, add_conn_rate=0.6,
                        adjust_weight_rate=0.8, perturb=0.3):

    # add species and calculate using the distance function
    species = []
    species = Species(genomes[0]).speciate(genomes, species, compatibility_threshold)

    # the new population and calculate the total fitness
    new_genomes = []
    total_fitness = sum([specie.calc_average_fitness() for specie in species])
    remaining_pop = population_size


    for specie in species:
        total_fitness = max(0.001, total_fitness)
        # calculate species average
        num_children = max(1, int(specie.calc_average_fitness() / total_fitness * population_size))
        remaining_pop -= num_children
        sorted_specie = calculate_probability(specie)

        # choose parents and crossover to create a child.
        for _ in range(num_children):
            parent1 = proportional_selection(sorted_specie)
            parent2 = proportional_selection(sorted_specie, avoid=parent1)
            child = crossover(parent1, parent2, add_node_rate, add_conn_rate, adjust_weight_rate, perturb)
            new_genomes.append(child)

    # choose a random genome and crossover the best genomes
    while len(new_genomes) < population_size:
        weights = [s.calc_average_fitness() for s in species]
        if sum(weights) <= 0:
            specie = random.choices(species, k=1)[0]
            genome = random.choices(specie.members, k=1)[0]
            genome.alive = True
            new_genomes.append(genome)
        else:
            new_genomes.append(best_genome(genomes))
            specie = random.choices(species, weights=weights, k=1)[0]
            if len(specie.members) >= 2:
                parent1, parent2 = random.sample(specie.members, k=2)
                new_genomes.append(crossover(parent1, parent2))

    return new_genomes


def proportional_selection(sorted_specie, avoid=None):
    rand = random.random()
    cumulative_prob = 0.0
    for genome, probability in sorted_specie.items():
        if genome == avoid:
            continue
        cumulative_prob += probability
        if rand <= cumulative_prob:
            return genome
    return random.choice(list(sorted_specie.keys()))


def calculate_probability(specie):
    prop = {}
    total_fitness = max(0.0001, sum([genome.fitness for genome in specie.members]))
    for genome in specie.members:
        prop[genome] = genome.fitness / total_fitness
    prop_sorted = dict(sorted(prop.items(), key=lambda item: item[1], reverse=True))
    return prop_sorted


def crossover(parent1, parent2, add_node_rate=0.3, add_conn_rate=0.6, adjust_weight_rate=0.8, perturb=0.3):
    if parent1.fitness < parent2.fitness:
        parent1, parent2 = parent2, parent1

    child = Genome()

    for innovation_num in parent1.connections.keys():
        gene1 = parent1.connections.get(innovation_num)
        gene2 = parent2.connections.get(innovation_num)

        if gene1 is not None and gene2 is not None:
            if random.random() < 0.5:
                child.add_connections(gene1)
            else:
                child.add_connections(gene2)
        elif gene1 is not None and gene2 is None:
            child.add_connections(gene1)

    for conn in child.connections.values():
        if conn.in_ not in child.nodes:
            child.add_node(conn.in_)
        if conn.out not in child.nodes:
            child.add_node(conn.out)

    child.mutate(add_node_rate, add_conn_rate, adjust_weight_rate, perturb)
    return child


def best_genome(genomes):
    genome = genomes[0]

    for current in genomes:
        if current.fitness > genome.fitness:
            genome = current
    genome.alive = True
    return genome
