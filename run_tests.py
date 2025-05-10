import time
import copy

try:
    from puzzle.state import Start, Goal, print_matrix, change_matran_string

    if not hasattr(puzzle.state, 'Moves_Dir_Name'):
        puzzle.state.Moves_Dir_Name = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    if not hasattr(puzzle.state, 'Moves_List_Named'):
        puzzle.state.Moves_List_Named = [('U', (-1, 0)), ('D', (1, 0)), ('L', (0, -1)), ('R', (0, 1))]

    from algorithms.bfs import bfs_search
    from algorithms.dfs import dfs_search
    from algorithms.ucs import ucs_search
    from algorithms.iddfs import iddfs_search
    from algorithms.greedy import greedy_search
    from algorithms.a_star import a_star_search
    from algorithms.ida_star import ida_star_search
    from algorithms.hill_climbing import (simple_hill_climbing_first_choice,
                                          steepest_ascent_hill_climbing,
                                          stochastic_hill_climbing)
    from algorithms.simulated_annealing import simulated_annealing_search
    from algorithms.beam_search import beam_search
    from algorithms.genetic_algorithm import genetic_algorithm_search
    from algorithms.conformant_bfs import conformant_bfs_search
    from algorithms.backtracking_search import solve_with_backtracking
    from algorithms.ac3_solver import ac3_for_8_puzzle
    from algorithms.and_or_search import solve_with_and_or_search
    from algorithms.q_learning_solver import run_q_learning_training
    from algorithms.td_learning_solver import run_sarsa_training
except ImportError as e:
    exit()

if __name__ == "__main__":
    algorithms_to_test = {
        "BFS": bfs_search,
        "UCS": ucs_search,
        "DFS (Depth=30)": lambda s: dfs_search(s, max_depth=30),
        "IDDFS (Depth=20)": lambda s: iddfs_search(s, max_depth=20),
        "Greedy": greedy_search,
        "A*": a_star_search,
        "IDA* (Thresh=80)": lambda s: ida_star_search(s, max_threshold=80),
        "Simple HC": lambda s: simple_hill_climbing_first_choice(s, max_steps=2000),
        "Steepest Ascent HC": lambda s: steepest_ascent_hill_climbing(s, max_steps=2000),
        "Stochastic HC": lambda s: stochastic_hill_climbing(s, max_steps=2000),
        "Simulated Annealing": lambda s: simulated_annealing_search(s, initial_temp=50, cooling_rate=0.98,
                                                                    min_temp=0.01, max_iterations=15000),
        "Beam Search (k=5)": lambda s: beam_search(s, beam_width=5, max_iterations=1000),
        "Genetic Algorithm": lambda s: genetic_algorithm_search(s, Goal, population_size=100, generations=100,
                                                                mutation_rate=0.2),
        "Backtracking (D=20)": lambda s: solve_with_backtracking(s, Goal, max_depth_bt=20),
        "AC-3 Solver": lambda s: ac3_for_8_puzzle(s),
        "AND-OR Search": lambda s: solve_with_and_or_search(s),
        "Q-Learning (1k eps)": lambda s: run_q_learning_training(s, Goal, episodes=1000, max_steps_per_episode=100),
        "TD (SARSA) (1k eps)": lambda s: run_sarsa_training(s, Goal, episodes=1000, max_steps_per_episode=100),
    }

    results = {}
    for name, func in algorithms_to_test.items():
        start_state_copy = copy.deepcopy(Start)

        start_time = time.time()
        try:
            if name == "Conformant BFS":  # Handled separately later
                continue
            result_data = func(start_state_copy)
        except Exception as e:
            result_data = f"EXECUTION ERROR: {e}"

        end_time = time.time()
        elapsed = end_time - start_time

        path_len_display = "N/A"
        status = "Unknown"

        if isinstance(result_data, str) and "ERROR" in result_data:
            status = "Exec Error"
        elif isinstance(result_data, dict) and "type" in result_data:  # New result types
            res_type = result_data["type"]
            if res_type == "ac3_result":
                status = f"AC-3: Cons={result_data.get('is_consistent')}"
                path_len_display = "-"
            elif res_type == "and_or_result":
                if result_data.get("path"):
                    status = "AND-OR: Path Found"
                    path_len_display = len(result_data["path"])
                else:
                    status = "AND-OR: No Path"
                    path_len_display = "0"
            elif res_type in ["q_learning_result", "sarsa_result"]:
                status = f"{name.split(' ')[0]}: Trained"  # Q-Learning: Trained
                path_len_display = f"{len(result_data.get('rewards_log', []))} eps"
            else:
                status = f"Dict: {res_type}"

        elif isinstance(result_data, list):  # Standard path
            if result_data:
                path_len_display = len(result_data)
                final_state_str = change_matran_string(result_data[-1])
                goal_state_str = change_matran_string(Goal)
                if final_state_str == goal_state_str:
                    status = "Goal Found"
                else:  # Hill climbing might end not at goal
                    status = "Path Found (Non-Goal)"
            else:  # Empty list
                status = "No Path Found"
                path_len_display = "0"
        else:  # None or other
            status = "No Result / Failed"
            path_len_display = "0"

        results[name] = (status, path_len_display, elapsed)

    initial_belief_state = [
        [[2, 6, 5], [0, 8, 7], [4, 3, 1]],
        [[2, 6, 5], [8, 0, 7], [4, 3, 1]],
        [[2, 0, 5], [6, 8, 7], [4, 3, 1]]
    ]
    name = "Conformant BFS"
    start_time = time.time()
    try:
        conf_bfs_result_path_names = conformant_bfs_search(initial_belief_state, Goal)
    except Exception as e:
        conf_bfs_result_path_names = f"EXECUTION ERROR: {e}"
    end_time = time.time()
    elapsed = end_time - start_time
    if isinstance(conf_bfs_result_path_names, str) and "ERROR" in conf_bfs_result_path_names:
        results[name] = ("Exec Error", "-", elapsed)
    elif conf_bfs_result_path_names is not None:
        results[name] = ("Path Found (Moves)", len(conf_bfs_result_path_names), elapsed)
    else:
        results[name] = ("No Path Found", "0", elapsed)

    for name, data in results.items():
        res_status, length_info, duration = data
        print(f"{name:<25}: Status = {res_status:<25} | Len/Info = {str(length_info):<10} | Time = {duration:.4f}s")