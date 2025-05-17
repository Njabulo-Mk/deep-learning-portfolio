class Species:
    def __init__(self, representative):
        self.representative = representative
        self.members = [representative]
        self.average_fitness = 0.0

    '''distance of genomes - is if keys are the same, calculate the distance'''
    def distance(self, genome1, genome2, c1=1.0, c2=1.0, c3=0.4):
        disjoint, excess, weight_diff, matching_genes = 0, 0, 0.0, 0
        max_innovation1 = max(genome1.connections.keys())
        max_innovation2 = max(genome2.connections.keys())

        all_innov = set(genome1.connections.keys()).union(set(genome2.connections.keys()))

        for innovation_num in all_innov:
            gene1 = genome1.connections.get(innovation_num)
            gene2 = genome2.connections.get(innovation_num)

            if gene1 is None and gene2 is not None:
                if innovation_num > max_innovation1:
                    excess += 1
                else:
                    disjoint += 1
            elif gene1 is not None and gene2 is None:
                if innovation_num > max_innovation2:
                    excess += 1
                else:
                    disjoint += 1
            elif gene1 is not None and gene2 is not None:
                matching_genes += 1
                weight_diff += abs(gene1.weight - gene2.weight)

        if matching_genes > 0:
            weight_diff /= matching_genes

        N = max(len(genome1.connections), len(genome2.connections))
        if N < 20:
            N = 1

        return (c1 * excess) / N + (c2 * disjoint) / N + c3 * weight_diff

    '''add genomes to the species'''
    def add_member(self, genome):
        self.members.append(genome)

    '''average fitness of the genomes'''
    def calc_average_fitness(self):
        for genome in self.members:
            genome.shared_fitness = genome.fitness/len(self.members)
        self.average_fitness = sum([g.shared_fitness for g in self.members]) / len(self.members)
        return self.average_fitness

    '''calculate the distance and if in the threshold add to species'''
    def speciate(self, genomes, species_list, compatibility_threshold):
        for genome in genomes:
            assigned_species = False
            for species in species_list:
                distance = species.distance(genome, species.representative)
                if distance < compatibility_threshold:
                    species.add_member(genome)
                    assigned_species = True
                    break

            if not assigned_species:
                species_list.append(Species(representative=genome))
        return species_list
