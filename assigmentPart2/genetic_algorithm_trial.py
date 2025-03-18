import numpy as np
import concurrent.futures
import random
import time


class GeneticAlgorithm:
    """
    Genetic Algorithm to solve the Traveling Salesman Problem (TSP).

    Attributes:
        distance_matrix (np.array): A 2D array representing the distance matrix between cities.
        num_cities (int): The number of cities in the distance matrix.
        population_size (int): The number of individuals in the population.
        generations (int): The number of generations to run the genetic algorithm.
        crossover_rate (float): The probability of crossover occurring between two parents.
        mutation_rate (float): The probability of mutation occurring in an individual.
    """

    def __init__(self, distance_matrix, population_size=100, generations=100, crossover_rate=0.8, mutation_rate=0.1):
        """
        Initializes the Genetic Algorithm with the provided parameters.

        Args:
            distance_matrix (np.array): A 2D array representing the distance matrix between cities.
            population_size (int): The number of individuals in the population. Defaults to 100.
            generations (int): The number of generations to evolve. Defaults to 100.
            crossover_rate (float): The probability of crossover between two parents. Defaults to 0.8.
            mutation_rate (float): The probability of mutation. Defaults to 0.1.
        """
        self.distance_matrix = distance_matrix
        self.num_cities = len(distance_matrix)
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def initialize_population(self):
        """
        Initializes a population of random routes (permutations of city indices).

        Returns:
            list: A list of `population_size` routes (each route is a list of city indices).
        """
        return [np.random.permutation(self.num_cities).tolist() for _ in range(self.population_size)]

    def fitness(self, route):
        """
        Calculates the fitness of a route. The fitness is the negative of the total distance traveled in the route.

        Args:
            route (list): A list of city indices representing the route.

        Returns:
            float: The negative of the total distance traveled in the route (fitness).
        """
        total_distance = sum(self.distance_matrix[route[i]][route[i + 1]] for i in range(len(route) - 1))
        total_distance += self.distance_matrix[route[-1]][route[0]]  # Return to the start
        return -total_distance  # Negative because we want to minimize the distance

    def tournament_selection(self, population):
        """
        Selects a parent from the population using tournament selection. 
        It randomly samples a subset of individuals, sorts them by fitness, 
        and returns the best individual.

        Args:
            population (list): A list of tuples where each tuple contains an individual and its fitness.

        Returns:
            list: The best individual from the tournament selection.
        """
        tournament_size = 5
        selected = random.sample(population, tournament_size)
        selected.sort(key=lambda x: x[1], reverse=True)
        return selected[0]

    def crossover(self, parent1, parent2):
        """
        Performs crossover between two parent routes to produce a child route. 
        It uses a two-point crossover method where a segment from one parent 
        is inherited, and the rest is filled by the second parent.

        Args:
            parent1 (list): The first parent route.
            parent2 (list): The second parent route.

        Returns:
            list: A new child route formed by the crossover of parent1 and parent2.
        """
        if random.random() > self.crossover_rate:
            return parent1[:]  # No crossover, return parent1 as child

        start, end = sorted(random.sample(range(self.num_cities), 2))
        child = [-1] * self.num_cities
        child[start:end] = parent1[start:end]

        pos = end
        for city in parent2:
            if city not in child:
                if pos >= self.num_cities:
                    pos = 0
                child[pos] = city
                pos += 1
        return child

    def mutate(self, route):
        """
        Performs mutation on a route by swapping two random cities. 
        The mutation rate determines the probability of mutation.

        Args:
            route (list): A list representing a route.

        Returns:
            list: The mutated route.
        """
        if random.random() < self.mutation_rate:
            i, j = random.sample(range(self.num_cities), 2)
            route[i], route[j] = route[j], route[i]  # Swap two cities
        return route

    def evolve(self, population):
        """
        Evolves the population for one generation. It evaluates the population, 
        selects parents using tournament selection, applies crossover and mutation, 
        and creates a new population.

        Args:
            population (list): The current population of routes.

        Returns:
            tuple: A new population and the best individual in the current population.
        """
        new_population = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_fitness = {executor.submit(self.fitness, individual): individual for individual in population}
            fitness_results = {future: future.result() for future in concurrent.futures.as_completed(future_fitness)}

        evaluated_population = [(individual, fitness_results[future]) for future, individual in future_fitness.items()]
        evaluated_population.sort(key=lambda x: x[1], reverse=True)

        while len(new_population) < self.population_size:
            parent1 = self.tournament_selection(evaluated_population)[0]
            parent2 = self.tournament_selection(evaluated_population)[0]
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)

        return new_population, evaluated_population[0]

    def run(self):
        """
        Runs the genetic algorithm for the specified number of generations. 
        It evolves the population and keeps track of the best solution found.

        Returns:
            tuple: The best solution found and its fitness.
        """
        population = self.initialize_population()
        best_solution = None
        best_fitness = float('-inf')

        for generation in range(1, self.generations + 1):
            population, best_in_population = self.evolve(population)

            if best_in_population[1] > best_fitness:
                best_solution = best_in_population[0]
                best_fitness = best_in_population[1]

            if generation % 10 == 0:
                print(f"Generation {generation}: Best fitness = {best_fitness}")

        print("Best Solution:", best_solution)
        print("Total Distance:", -best_fitness)
        return best_solution, best_fitness


def generate_random_distance_matrix(num_cities):
    """
    Generates a random distance matrix of size `num_cities x num_cities`. 
    The diagonal is filled with zeros, as the distance from a city to itself is zero.

    Args:
        num_cities (int): The number of cities.

    Returns:
        np.array: A 2D numpy array representing the random distance matrix.
    """
    matrix = np.random.randint(10, 1000, size=(num_cities, num_cities))
    np.fill_diagonal(matrix, 0)
    return matrix


# Main execution
distance_matrix = generate_random_distance_matrix(100)  # Generate a distance matrix for 100 cities
ga = GeneticAlgorithm(distance_matrix, population_size=100, generations=60)  # Initialize GeneticAlgorithm

start_time = time.time()  # Start the timer
best_solution, best_fitness = ga.run()  # Run the genetic algorithm
end_time = time.time()  # End the timer

execution_time = end_time - start_time  # Calculate the execution time
print(f"Execution Time: {execution_time:.2f} seconds")  # Print the execution time






