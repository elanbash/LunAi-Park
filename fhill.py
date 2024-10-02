import random
from typing import List, Dict, Tuple


class HillClimbParkOptimizer:
    def __init__(
            self,
            desired_rides: List[int],
            time_limit: int,
            ride_durations: List[int],
            travel_times: List[List[int]],
            ride_categories: List[str],
            category_delays: Dict[str, int],
            day: str,
            day_category_effects: Dict[str, str],
    ):
        self.desired_rides = desired_rides
        self.time_limit = time_limit
        self.ride_durations = ride_durations
        self.travel_times = travel_times
        self.ride_categories = ride_categories
        self.category_delays = category_delays
        self.day = day
        self.day_category_effects = day_category_effects
        self.num_restarts = 5
        self.max_iterations_per_restart = 100
        self.path = []
        self.total_time = 0

        # Get affected categories for the selected day
        self.affected_categories = self.day_category_effects.get(self.day, "")

    def get_ride_delay(self, ride_index: int) -> int:
        """Calculate the additional delay for a given ride based on its categories."""
        delay = 0
        category = self.ride_categories[ride_index] # currently using option of one category per ride
        if category is self.affected_categories:
            delay += (self.category_delays.get(category, 0) / 100) * self.ride_durations[ride_index]
        return delay

    def calculate_total_time(self, path: List[int]) -> int:
        total_time = 0
        current_ride = 0  # Start from ride 0
        for ride in path:
            # Calculate the delay for the ride
            delay = self.get_ride_delay(ride)
            # Add travel time and ride duration with delay
            total_time += self.travel_times[current_ride][ride] + self.ride_durations[ride] + delay
            current_ride = ride
        return total_time

    def is_valid_solution(self, path: List[int]) -> bool:
        return self.calculate_total_time(path) <= self.time_limit

    def generate_random_solution(self) -> List[int]:
        solution = []
        remaining_rides = self.desired_rides.copy()
        random.shuffle(remaining_rides)
        current_time = 0
        current_ride = 0

        for ride in remaining_rides:
            # Calculate the delay for the ride
            delay = self.get_ride_delay(ride)
            # Calculate time to add
            time_to_add = self.travel_times[current_ride][ride] + self.ride_durations[ride] + delay
            if current_time + time_to_add <= self.time_limit:
                solution.append(ride)
                current_time += time_to_add
                current_ride = ride
            else:
                continue  # Continue to check other rides

        return solution

    def get_neighbors(self, solution: List[int]) -> List[List[int]]:
        neighbors = []

        # Add a ride
        for ride in self.desired_rides:
            if ride not in solution:
                for i in range(len(solution) + 1):
                    new_solution = solution[:i] + [ride] + solution[i:]
                    if self.is_valid_solution(new_solution):
                        neighbors.append(new_solution)

        # Swap two rides
        for i in range(len(solution)):
            for j in range(i + 1, len(solution)):
                new_solution = solution.copy()
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                if self.is_valid_solution(new_solution):
                    neighbors.append(new_solution)

        return neighbors

    def hill_climbing(self, initial_solution: List[int]) -> List[int]:
        current_solution = initial_solution
        current_score = (len(current_solution), -self.calculate_total_time(current_solution))

        for _ in range(self.max_iterations_per_restart):
            neighbors = self.get_neighbors(current_solution)
            if not neighbors:
                break

            best_neighbor = max(
                neighbors, key=lambda sol: (len(sol), -self.calculate_total_time(sol))
            )
            best_neighbor_score = (len(best_neighbor), -self.calculate_total_time(best_neighbor))

            if best_neighbor_score <= current_score:
                break

            current_solution = best_neighbor
            current_score = best_neighbor_score

        return current_solution

    def run(self) -> Tuple[int, int]:
        best_solution = []
        best_score = (0, 0)

        for _ in range(self.num_restarts):
            initial_solution = self.generate_random_solution()
            solution = self.hill_climbing(initial_solution)
            score = (len(solution), -self.calculate_total_time(solution))

            if score > best_score:
                best_solution = solution
                best_score = score
        total_time = self.calculate_total_time(best_solution)
        self.path = best_solution
        self.total_time = total_time
        return len(best_solution), total_time
