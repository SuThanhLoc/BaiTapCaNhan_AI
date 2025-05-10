import random
import numpy as np
from puzzle.state import Moves, Tim_0, Check, DiChuyen, change_matran_string, Goal


class SARSAAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_rate=1.0, exploration_decay=0.995,
                 min_exploration_rate=0.01):
        self.q_table = {}
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.epsilon_decay = exploration_decay
        self.min_epsilon = min_exploration_rate

        if not hasattr(puzzle.state, 'Moves_List_Named'):
            puzzle.state.Moves_List_Named = [
                ('U', (-1, 0)), ('D', (1, 0)), ('L', (0, -1)), ('R', (0, 1))
            ]
        self.actions_map_idx_to_named_move = {i: named_move for i, named_move in
                                              enumerate(puzzle.state.Moves_List_Named)}
        self.actions_count = len(puzzle.state.Moves_List_Named)

    def get_q_value(self, state_str, action_idx):
        return self.q_table.get((state_str, action_idx), 0.0)

    def _get_valid_action_indices(self, state_matrix):
        valid_action_indices = []
        x0, y0 = Tim_0(state_matrix)
        if x0 == -1: return []
        for idx in range(self.actions_count):
            _, (dx, dy) = self.actions_map_idx_to_named_move[idx]
            if Check(x0 + dx, y0 + dy):
                valid_action_indices.append(idx)
        return valid_action_indices

    def choose_action(self, state_matrix, use_exploration=True):
        state_str = change_matran_string(state_matrix)
        if not state_str: return None

        valid_actions_indices = self._get_valid_action_indices(state_matrix)
        if not valid_actions_indices: return None

        if use_exploration and random.uniform(0, 1) < self.epsilon:
            action_idx = random.choice(valid_actions_indices)
        else:
            q_values_valid = {idx: self.get_q_value(state_str, idx) for idx in valid_actions_indices}
            if not q_values_valid: return random.choice(valid_actions_indices)

            max_q = -float('inf')
            for idx in valid_actions_indices:
                q_val = self.get_q_value(state_str, idx)
                if q_val > max_q: max_q = q_val

            best_actions_indices = [idx for idx in valid_actions_indices if self.get_q_value(state_str, idx) == max_q]
            if best_actions_indices:
                action_idx = random.choice(best_actions_indices)
            else:
                action_idx = random.choice(valid_actions_indices)
        return action_idx

    def update_q_table_sarsa(self, state_str, action_idx, reward, next_state_str, next_action_idx):
        if not state_str or action_idx is None: return

        old_q_value = self.get_q_value(state_str, action_idx)

        next_q_value_for_update = 0.0  # If next_state is terminal or next_action is None
        if next_state_str and next_action_idx is not None:
            next_q_value_for_update = self.get_q_value(next_state_str, next_action_idx)

        new_q_value = old_q_value + self.lr * (reward + self.gamma * next_q_value_for_update - old_q_value)
        self.q_table[(state_str, action_idx)] = new_q_value

    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


def run_sarsa_training(start_node_matrix, goal_state_matrix=Goal, episodes=1000, max_steps_per_episode=100):
    agent = SARSAAgent()
    goal_str = change_matran_string(goal_state_matrix)
    rewards_log = []

    for episode in range(episodes):
        current_s_matrix = [row[:] for row in start_node_matrix]
        current_s_str = change_matran_string(current_s_matrix)
        if not current_s_str: continue

        action_idx = agent.choose_action(current_s_matrix, use_exploration=True)
        if action_idx is None: continue

        episode_reward = 0
        for step in range(max_steps_per_episode):
            _, (dx, dy) = agent.actions_map_idx_to_named_move[action_idx]
            x0, y0 = Tim_0(current_s_matrix)
            next_s_matrix = DiChuyen(current_s_matrix, x0, y0, x0 + dx, y0 + dy)

            reward = 0
            is_terminal = False
            next_s_str = None

            if not next_s_matrix:
                reward = -200
                next_s_matrix = current_s_matrix
                next_s_str = change_matran_string(next_s_matrix)
                is_terminal = True
            else:
                next_s_str = change_matran_string(next_s_matrix)
                if next_s_str == goal_str:
                    reward = 100
                    is_terminal = True
                elif next_s_str == current_s_str:
                    reward = -10
                else:
                    reward = -1

            next_action_idx = None
            if not is_terminal:
                next_action_idx = agent.choose_action(next_s_matrix, use_exploration=True)
                if next_action_idx is None:  # Can't move from next_s_matrix, effectively terminal for this path
                    is_terminal = True  # Treat as terminal for Q-update if no valid next action

            agent.update_q_table_sarsa(current_s_str, action_idx, reward, next_s_str, next_action_idx)
            episode_reward += reward

            if is_terminal: break

            current_s_matrix = next_s_matrix
            current_s_str = next_s_str
            action_idx = next_action_idx  # Crucial for SARSA

            if action_idx is None: break  # End episode if no next action could be chosen

        agent.decay_epsilon()
        rewards_log.append(episode_reward)
        if (episode + 1) % (episodes // 10 if episodes >= 10 else 1) == 0:
            pass

    return {"agent": agent, "rewards_log": rewards_log, "type": "sarsa_result"}