import time

import matplotlib.pyplot as plt
from fhill import *
from futil import *
from fcat import *
from fbasic import *
import numpy as np


def run_optimization_algorithms(park_data: ParkData, user_data: UserData):
    # Hill climbing optimization
    optimizer = HillClimbParkOptimizer(
        user_data.desired_rides,
        user_data.total_time_available,
        park_data.ride_times,
        park_data.travel_times,
        park_data.ride_categories,
        park_data.category_time_addition,
        user_data.visit_day,
        park_data.day_category_affect
    )
    start_time = time.time()
    num_rides_hill, total_time_hill = optimizer.run()
    end_time = time.time()
    comp_time_hill = end_time - start_time

    # Genetic algorithm optimization
    optimizer = GeneticAlgorithm(
        park_data.ride_times,
        park_data.travel_times,
        park_data.ride_categories,
        park_data.category_time_addition,
        park_data.day_category_affect,
        user_data.desired_rides,
        user_data.visit_day,
        user_data.total_time_available
    )
    start_time = time.time()
    num_rides_genetic, total_time_genetic = optimizer.run()
    end_time = time.time()
    comp_time_gen = end_time - start_time

    # Basic algorithm optimization
    optimizer = GreedyAmusementParkOptimizer(
        user_data.desired_rides,
        user_data.total_time_available,
        park_data.ride_times,
        park_data.travel_times,
        park_data.ride_categories,
        park_data.category_time_addition,
        user_data.visit_day,
        park_data.day_category_affect
    )
    start_time = time.time()
    num_rides_greedy, total_time_greedy = optimizer.run()
    end_time = time.time()
    comp_time_greedy = end_time - start_time

    return (num_rides_hill, total_time_hill, comp_time_hill), (num_rides_genetic, total_time_genetic, comp_time_gen), (
        num_rides_greedy, total_time_greedy, comp_time_greedy)


def generate_park_and_user_data(num_parks: int):
    park_names = [str(i) for i in range(num_parks)]
    park_user_data = []

    for park_name in park_names:
        num_rides = random.randint(10, 40)
        park_data = generate_park_data(park_name, num_rides)
        user_data = generate_user_data(num_rides)
        park_user_data.append((park_data, user_data))

    return park_names, park_user_data


def run_simulations(park_names, park_user_data):
    results = {
        'hill': {'rides': [], 'time': [], 'complexity': []},
        'genetic': {'rides': [], 'time': [], 'complexity': []},
        'greedy': {'rides': [], 'time': [], 'complexity': []}
    }

    for park_data, user_data in park_user_data:

        (num_rides_hill, total_time_hill, comp_time_hill), (num_rides_genetic, total_time_genetic, comp_time_gen), (
            num_rides_greedy, total_time_greedy, comp_time_greedy) = run_optimization_algorithms(park_data, user_data)

        results['hill']['rides'].append(num_rides_hill)
        results['hill']['time'].append(total_time_hill)
        results['hill']['complexity'].append(comp_time_hill)
        results['genetic']['rides'].append(num_rides_genetic)
        results['genetic']['time'].append(total_time_genetic)
        results['genetic']['complexity'].append(comp_time_gen)
        results['greedy']['rides'].append(num_rides_greedy)
        results['greedy']['time'].append(total_time_greedy)
        results['greedy']['complexity'].append(comp_time_greedy)

    return results


def plot_results(park_names, results, park_user_data):
    num_parks = len(park_names)
    algorithms = ['Hill Climbing', 'Genetic Algorithm', 'Greedy Algorithm']
    colors = ['skyblue', 'lightgreen', 'lightcoral']

    x = np.arange(num_parks)  # the label locations
    width = 0.25  # the width of the bars

    # Plot number of rides
    fig, ax = plt.subplots(figsize=(15, 8))
    for i, (algo, color) in enumerate(zip(['hill', 'genetic', 'greedy'], colors)):
        ax.bar(x + i * width, results[algo]['rides'], width, label=algorithms[i], color=color)

    ax.set_xlabel('Park')
    ax.set_ylabel('Number of Rides')
    ax.set_title('Number of Rides in Optimal Sequence')
    ax.set_xticks(x + width)
    ax.set_xticklabels(park_names, rotation=90)
    ax.legend()
    plt.tight_layout()

    # Plot total time
    fig, ax = plt.subplots(figsize=(15, 8))
    for i, (algo, color) in enumerate(zip(['hill', 'genetic', 'greedy'], colors)):
        ax.bar(x + i * width, results[algo]['time'], width, label=algorithms[i], color=color)

    ax.set_xlabel('Park')
    ax.set_ylabel('Total Time (minutes)')
    ax.set_title('Total Time of Rides in Optimal Sequence')
    ax.set_xticks(x + width)
    ax.set_xticklabels(park_names, rotation=90)
    ax.legend()
    plt.tight_layout()

    # Plot time complexity as a function of the number of rides
    num_rides_list = [park_user_data[i][0].num_rides for i in range(num_parks)]

    # Sort the number of rides and get the corresponding sorted indices
    sorted_indices = np.argsort(num_rides_list)
    sorted_num_rides_list = np.array(num_rides_list)[sorted_indices]

    fig, ax = plt.subplots(figsize=(15, 8))
    for i, (algo, color) in enumerate(zip(['hill', 'genetic', 'greedy'], colors)):
        # Sort the complexity times based on the sorted order of num_rides_list
        sorted_complexity = np.array(results[algo]['complexity'])[sorted_indices]
        ax.bar(x + i * width, sorted_complexity, width, label=algorithms[i], color=color)

    ax.set_xlabel('Number of Rides in the Park (sorted)')
    ax.set_ylabel('Computation Time (seconds)')
    ax.set_title('Computation Time as a Function of Number of Rides (Sorted by Park Size)')
    ax.set_xticks(x + width)
    ax.set_xticklabels(sorted_num_rides_list, rotation=90)
    ax.legend()
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # User has provided command-line arguments
        algorithm = sys.argv[1].lower()
        num_rides = int(sys.argv[2])
        total_time_available = int(sys.argv[3])
        visit_day = sys.argv[4].lower()
        desired_rides = list(map(int, sys.argv[5].split(',')))

        # Generate park data and user data
        park_name = "UserPark"
        park_data = generate_park_data(park_name, num_rides)
        user_data = UserData(num_rides, desired_rides, total_time_available, visit_day)

        # Run the selected algorithm
        if algorithm == 'greedy':
            optimizer = GreedyAmusementParkOptimizer(
                user_data.desired_rides,
                user_data.total_time_available,
                park_data.ride_times,
                park_data.travel_times,
                park_data.ride_categories,
                park_data.category_time_addition,
                user_data.visit_day,
                park_data.day_category_affect
            )
        elif algorithm == 'hill':
            optimizer = HillClimbParkOptimizer(
                user_data.desired_rides,
                user_data.total_time_available,
                park_data.ride_times,
                park_data.travel_times,
                park_data.ride_categories,
                park_data.category_time_addition,
                user_data.visit_day,
                park_data.day_category_affect
            )
        elif algorithm == 'genetic':
            optimizer = GeneticAlgorithm(
                park_data.ride_times,
                park_data.travel_times,
                park_data.ride_categories,
                park_data.category_time_addition,
                park_data.day_category_affect,
                user_data.desired_rides,
                user_data.visit_day,
                user_data.total_time_available
            )
        else:
            print(f"Unknown algorithm: {algorithm}")
            sys.exit(1)

        # Measure computation time
        start_time = time.time()
        num_rides_result, total_time_result = optimizer.run()
        end_time = time.time()
        comp_time = end_time - start_time

        # Get the path and total travel time
        path = optimizer.path

        # Print out the results
        print(f"\nAlgorithm used: {algorithm.capitalize()}")
        print(f"Computation Time: {comp_time:.4f} seconds")
        park_data.print_data()
        user_data.print_data()
        print(f"Number of rides in the returned path: {num_rides_result}")
        print(f"Total time of the path: {total_time_result} minutes")
        print(f"Returned path: {path}")

    else:
        # Run simulations as before
        num_parks = 50
        park_names, park_user_data = generate_park_and_user_data(num_parks)
        results = run_simulations(park_names, park_user_data)
        plot_results(park_names, results, park_user_data)
