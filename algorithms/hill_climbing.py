# -*- coding: utf-8 -*-
# algorithms/hill_climbing.py
""" Các biến thể của thuật toán Hill Climbing """

import random
import copy
# Import các thành phần cần thiết từ puzzle package
from puzzle.state import Goal, Moves, Tim_0, Check, DiChuyen, change_matran_string
from puzzle.heuristics import khoang_cach_mahathan # Dùng Manhattan làm heuristic

def simple_hill_climbing_first_choice(start_node, max_steps=1000, goal_state=Goal):
    """Simple Hill Climbing (First Choice)."""
    print(f"Running Simple Hill Climbing (First Choice) with max_steps={max_steps}")
    current_state = start_node
    path = [current_state] # Track sequence of states
    steps = 0
    nodes_evaluated = 0
    goal_str = change_matran_string(goal_state)

    while steps < max_steps:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("SHC Error: Invalid current state."); return []
        nodes_evaluated += 1

        if current_state_str == goal_str:
            print(f"  Goal found after {steps} steps. Evaluated {nodes_evaluated} states.")
            return path # Return path of states

        x, y = Tim_0(current_state)
        if x == -1: print("  Error: Cannot find blank tile."); return []
        h_current = khoang_cach_mahathan(current_state, goal_state)
        if h_current == float('inf'): print("SHC Error: Current state invalid vs Goal."); return []

        moved = False
        # Generate neighbors and check in random order
        random_moves = random.sample(Moves, len(Moves))
        for dx, dy in random_moves:
            new_X, new_Y = dx + x, dy + y
            if Check(new_X, new_Y):
                neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                if neighbor_state:
                    nodes_evaluated += 1 # Count neighbor evaluation
                    h_neighbor = khoang_cach_mahathan(neighbor_state, goal_state)
                    # Accept the first strictly better neighbor
                    if h_neighbor < h_current:
                        current_state = neighbor_state
                        path.append(current_state) # Add new state to path
                        moved = True
                        break # Take the first better move found

        if not moved:
            print(f"  Stuck at local optimum after {steps} steps (h={h_current}). Evaluated {nodes_evaluated} states.")
            return path # Return path found so far, even if stuck

        steps += 1

    print(f"  Reached max steps ({max_steps}) without finding goal. Evaluated {nodes_evaluated} states.")
    return path # Return path found so far

def steepest_ascent_hill_climbing(start_node, max_steps=1000, goal_state=Goal):
    """Steepest Ascent Hill Climbing."""
    print(f"Running Steepest Ascent Hill Climbing with max_steps={max_steps}")
    current_state = start_node
    path = [current_state]
    steps = 0
    nodes_evaluated = 0
    goal_str = change_matran_string(goal_state)

    while steps < max_steps:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("SAHC Error: Invalid current state."); return []
        nodes_evaluated += 1

        if current_state_str == goal_str:
            print(f"  Goal found after {steps} steps. Evaluated {nodes_evaluated} states.")
            return path

        x, y = Tim_0(current_state)
        if x == -1: print("  Error: Cannot find blank tile."); return []
        h_current = khoang_cach_mahathan(current_state, goal_state)
        if h_current == float('inf'): print("SAHC Error: Current state invalid vs Goal."); return []

        best_neighbor = None
        h_best_neighbor = h_current # Initialize with current heuristic

        # Evaluate all neighbors
        for dx, dy in Moves:
            new_X, new_Y = dx + x, dy + y
            if Check(new_X, new_Y):
                neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                if neighbor_state:
                    nodes_evaluated += 1
                    h_neighbor = khoang_cach_mahathan(neighbor_state, goal_state)
                    # Find neighbor with the strictly lowest heuristic
                    if h_neighbor < h_best_neighbor:
                        h_best_neighbor = h_neighbor
                        best_neighbor = neighbor_state # Store the best state found

        # Move to the best neighbor only if it's strictly better than current
        if best_neighbor is not None:
            current_state = best_neighbor
            path.append(current_state)
        else:
            # Stuck at local optimum or plateau
            print(f"  Stuck at local optimum after {steps} steps (h={h_current}). Evaluated {nodes_evaluated} states.")
            return path

        steps += 1

    print(f"  Reached max steps ({max_steps}) without finding goal. Evaluated {nodes_evaluated} states.")
    return path

def stochastic_hill_climbing(start_node, max_steps=1000, goal_state=Goal):
    """Stochastic Hill Climbing."""
    print(f"Running Stochastic Hill Climbing with max_steps={max_steps}")
    current_state = start_node
    path = [current_state]
    steps = 0
    nodes_evaluated = 0
    goal_str = change_matran_string(goal_state)

    while steps < max_steps:
        current_state_str = change_matran_string(current_state)
        if not current_state_str: print("StochHC Error: Invalid current state."); return []
        nodes_evaluated += 1

        if current_state_str == goal_str:
            print(f"  Goal found after {steps} steps. Evaluated {nodes_evaluated} states.")
            return path

        x, y = Tim_0(current_state)
        if x == -1: print("  Error: Cannot find blank tile."); return []
        h_current = khoang_cach_mahathan(current_state, goal_state)
        if h_current == float('inf'): print("StochHC Error: Current state invalid vs Goal."); return []

        better_neighbors = [] # List of states that are strictly better

        # Find all strictly better neighbors
        for dx, dy in Moves:
            new_X, new_Y = dx + x, dy + y
            if Check(new_X, new_Y):
                neighbor_state = DiChuyen(current_state, x, y, new_X, new_Y)
                if neighbor_state:
                    nodes_evaluated += 1
                    h_neighbor = khoang_cach_mahathan(neighbor_state, goal_state)
                    if h_neighbor < h_current:
                        better_neighbors.append(neighbor_state)

        # Choose randomly among the better neighbors if any exist
        if better_neighbors:
            next_state = random.choice(better_neighbors)
            current_state = next_state
            path.append(current_state)
        else:
            # Stuck if no better neighbors
            print(f"  Stuck at local optimum after {steps} steps (h={h_current}). Evaluated {nodes_evaluated} states.")
            return path

        steps += 1

    print(f"  Reached max steps ({max_steps}) without finding goal. Evaluated {nodes_evaluated} states.")
    return path