# Amusement Park Optimizer

This project provides an optimizer to find the best path for visiting rides in an amusement park using various algorithms such as Greedy, Hill Climbing, and Genetic Algorithm. The program can run in two modes:
1. **User-Provided Data Mode:** Users provide the desired ride list, total available time, and day of the visit as command-line arguments.
2. **Random Data Mode:** If no command-line arguments are provided, the program will randomly generate user and park data.

## Installation

1. Clone the repository to your local machine.
2. Ensure you have Python installed (Python 3.x is recommended).
3. Install any necessary dependencies by running:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Project

You can run the `main.py` file with or without arguments.

### 1. Running with User-Provided Data

To run the program with user-specified data, you need to provide the following command-line arguments:
- `algorithm`: The algorithm to use (e.g., `greedy`, `hill`, `genetic`)
- `num_rides`: The total number of rides in the park.
- `total_time_available`: The time you have available for the visit (in minutes).
- `visit_day`: The day of the week (e.g., `Monday`, `Tuesday`, etc.).
- `desired_rides`: A comma-separated list of ride IDs that the user wants to visit.

Example:
```bash
python main.py greedy 10 240 Saturday 1,3,5,7
```

In this example:
- The greedy algorithm is chosen. 
- There are 10 rides in the park. 
- The user has 240 minutes available. 
- The visit is planned for Saturday. 
- The user wants to visit rides 1, 3, 5, and 7.

 ### 2. Running with Random Data
If you do not provide any command-line arguments, the program will generate random data for the park and user visit. To do this, simply run:

```bash
python main.py
```
This mode is useful for testing and simulation purposes.
