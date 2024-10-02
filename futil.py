import random
from typing import List, Dict


class ParkData:
    def __init__(self, park_name: str, num_rides: int):
        self.num_rides = num_rides
        self.park_name: str = park_name
        self.ride_times: List[int] = self._generate_ride_times(num_rides)
        self.travel_times: List[List[int]] = self._generate_travel_times(num_rides)
        self.ride_categories: List[str] = self._generate_ride_categories(num_rides)
        self.category_time_addition: Dict[str, int] = self._generate_category_time_addition()
        self.day_category_affect: Dict[str, str] = self._generate_day_category_affect()

    def _generate_ride_times(self, num_rides: int) -> List[int]:
        return [random.randint(3, 20) for _ in range(num_rides)]

    def _generate_travel_times(self, num_rides: int) -> List[List[int]]:
        return [[random.randint(3, 15) if i != j else 0 for j in range(num_rides)] for i in range(num_rides)]

    def _generate_ride_categories(self, num_rides: int) -> List[str]:
        categories = ['Family', 'Thrill', 'Adventure', 'Adults', 'Food', 'No Shelter', 'Maintenance']
        return [random.choice(categories) for _ in range(num_rides)]

    def _generate_category_time_addition(self) -> Dict[str, int]:
        return {
            'Family': random.randint(1, 20),
            'Thrill': random.randint(3, 25),
            'Adventure': random.randint(5, 45),
            'Adults': 20,
            'Food': 40,
            'No Shelter': 60,
            'Maintenance': 80
        }

    def _generate_day_category_affect(self) -> Dict[str, str]:
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        categories = ['Family', 'Thrill', 'Adventure', 'Adults', 'Food', 'No Shelter', 'Maintenance']
        return {day: random.choice(categories) for day in days_of_week}

    def print_data(self):
        print(f"--- {self.park_name} Data ---")
        print(f"Travel Times: {self.travel_times}")
        print(f"Ride Times: {self.ride_times}")
        print(f"Ride Categories: {dict(enumerate(self.ride_categories))}")
        print(f"Category Time Addition: {self.category_time_addition}")
        print(f"Day Category Affect: {self.day_category_affect}")
        print()


class UserData:
    def __init__(self, num_rides: int = None, desired_rides: List[int] = None, total_time_available: int = None,
                 visit_day: str = None):
        if desired_rides is not None and total_time_available is not None and visit_day is not None:
            # User has provided all required data
            self.desired_rides = desired_rides
            self.total_time_available = total_time_available
            self.visit_day = visit_day
        else:
            # Generate random data
            if num_rides is None:
                raise ValueError("num_rides must be provided to generate random data.")
            self.desired_rides = self._generate_desired_rides(num_rides)
            self.total_time_available = random.randint(10, 50)
            self.visit_day = random.choice(
                ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])

    def _generate_desired_rides(self, num_rides: int) -> List[int]:
        num_desired_rides = random.randint(1, num_rides)
        return random.sample(range(num_rides), num_desired_rides)

    def print_data(self):
        print(f"Desired Rides: {self.desired_rides}")
        print(f"Total Time Available: {self.total_time_available} minutes")
        print(f"Visit Day: {self.visit_day}")
        print()


def generate_park_data(park_name: str, num_rides: int) -> ParkData:
    return ParkData(park_name, num_rides)


def generate_user_data(num_rides: int) -> UserData:
    return UserData(num_rides)
