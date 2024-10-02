from typing import List, Dict, Tuple


class GreedyAmusementParkOptimizer:
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
        self.path = []
        self.total_time = 0
        # Get the affected categories for the given day
        self.affected_category = self.day_category_effects.get(self.day, [])

    def calculate_extra_delay(self, ride: int) -> float:
        ride_category = self.ride_categories[ride]
        if ride_category == self.affected_category:
            percentage_delay = self.category_delays.get(ride_category, 0)
            return (percentage_delay / 100) * self.ride_durations[ride]
        return 0

    def find_next_ride(self, current_ride: int, visited_rides: List[int], remaining_time: int) -> Tuple[int, float]:
        next_ride = None
        min_travel_time = float('inf')

        for ride in self.desired_rides:
            if ride in visited_rides or ride == current_ride:
                continue

            travel_time = self.travel_times[current_ride][ride]

            if travel_time <= remaining_time and travel_time < min_travel_time:
                min_travel_time = travel_time
                next_ride = ride

        return next_ride, min_travel_time

    def run(self) -> Tuple[int, int]:
        current_ride = 0
        remaining_time = self.time_limit
        visited_rides = []

        while True:
            next_ride, travel_time = self.find_next_ride(current_ride, visited_rides, remaining_time)

            if next_ride is None:
                break

            extra_delay = self.calculate_extra_delay(next_ride)
            total_time_spent = travel_time + self.ride_durations[next_ride] + extra_delay
            remaining_time -= total_time_spent

            if remaining_time < 0:
                break

            visited_rides.append(next_ride)
            current_ride = next_ride

        total_time = self.time_limit - remaining_time
        self.path = visited_rides
        self.total_time = total_time
        return len(visited_rides), total_time
