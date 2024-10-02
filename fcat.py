import random
from typing import List


class GeneticAlgorithm:
    def __init__(self, ride_durations, travel_times, ride_categories, category_delays, day_category_effects,
                 desired_rides, day, time_limit):
        self.ride_durations = ride_durations
        self.travel_times = travel_times
        self.ride_categories = ride_categories
        self.category_delays = category_delays
        self.day_category_effects = day_category_effects
        self.desired_rides = desired_rides
        self.day = day
        self.affected_categories = self.day_category_effects.get(self.day, [])
        self.time_limit = time_limit
        self.population_size = 80
        self.generations = 30
        self.mutation_rate = 0.05
        self.path = []
        self.total_time = 0

    def is_feasible(self, chromosome):
        if not chromosome:
            return True
        total_time = self.travel_times[0][chromosome[0]]
        for i in range(len(chromosome) - 1):
            ride = chromosome[i]
            next_ride = chromosome[i + 1]
            total_time += self.ride_durations[ride] + self.travel_times[ride][next_ride] + self.get_penalty(ride)
            if total_time > self.time_limit:
                return False
        if total_time + self.ride_durations[chromosome[-1]] + self.get_penalty(chromosome[-1]) + self.get_penalty(
                chromosome[-1]) > self.time_limit:
            return False
        return True

    def get_penalty(self, ride):
        penalties = 0
        categories = [self.ride_categories[ride]]
        for category in categories:
            if category in self.day_category_effects[self.day]:
                percentage_delay = self.category_delays.get(category, 0)  # Get the percentage delay
                penalties += (percentage_delay / 100) * self.ride_durations[ride]
        return penalties

    def generate_chromosome(self):
        chromosome = self.desired_rides.copy()
        random.shuffle(chromosome)
        while chromosome and not self.is_feasible(chromosome):
            chromosome.pop()
        return chromosome

    def generate_population(self, size):
        population = []
        while len(population) < size:
            chromosome = self.generate_chromosome()
            if self.is_feasible(chromosome):
                population.append(chromosome)
        return population

    def fitness_function(self, chromosome):
        total_time = 0
        rides_visited = 0
        if not chromosome:
            return 0
        for i in range(len(chromosome) - 1):
            ride = chromosome[i]
            next_ride = chromosome[i + 1]
            total_time += self.ride_durations[ride] + self.travel_times[ride][next_ride] + self.get_penalty(ride)
            if total_time > self.time_limit:
                return rides_visited
            rides_visited += 1
        if total_time + self.ride_durations[chromosome[-1]] + self.get_penalty(chromosome[-1]) <= self.time_limit:
            rides_visited += 1
        return rides_visited

    def selection(self, population, fitnesses):
        total_fitness = sum(fitnesses)
        pick = random.uniform(0, total_fitness)
        current = 0
        for individual, fitness in zip(population, fitnesses):
            current += fitness
            if current >= pick:
                return individual

    def crossover(self, parent1, parent2):
        size = min(len(parent1), len(parent2))
        if size < 2:
            return parent1
        start, end = sorted(random.sample(range(size), 2))
        child = parent1[start:end] + [gene for gene in parent2 if gene not in parent1[start:end]]
        unique_child = []
        for gene in child:
            if gene not in unique_child:
                unique_child.append(gene)
        return unique_child

    def mutate(self, chromosome):
        if random.random() < self.mutation_rate:
            if len(chromosome) < 2:
                return chromosome
            i, j = random.sample(range(len(chromosome)), 2)
            chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
        if not self.is_feasible(chromosome):
            return None
        return chromosome

    def calculate_total_time(self, path: List[int]) -> int:
        total_time = 0
        current_ride = 0  # Start from ride 0
        for ride in path:
            # Calculate the delay for the ride
            delay = self.get_penalty(ride)
            # Add travel time and ride duration with delay
            total_time += self.travel_times[current_ride][ride] + self.ride_durations[ride] + delay
            current_ride = ride
        return total_time

    def run(self):
        population = self.generate_population(self.population_size)

        for generation in range(self.generations):
            fitnesses = [self.fitness_function(chromosome) for chromosome in population]
            new_population = []
            sorted_population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
            new_population.append(sorted_population[0][0])
            while len(new_population) < self.population_size:
                parent1 = self.selection(population, fitnesses)
                parent2 = self.selection(population, fitnesses)
                child = self.crossover(parent1, parent2)
                if self.is_feasible(child):
                    mutated_child = self.mutate(child)
                    if mutated_child:
                        new_population.append(mutated_child)
                    else:
                        new_population.append(child)
            population = new_population
        best_solution = max(zip(population, fitnesses), key=lambda x: x[1])
        total_time = self.calculate_total_time(best_solution[0])
        self.path = best_solution[0]
        self.total_time = total_time

        return len(best_solution[0]), total_time
