class CSP:
    def __init__(self, variables, domains, constraints, puzzle_state_map=None):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.neighbors = self._get_neighbors()
        self.puzzle_state_map = puzzle_state_map if puzzle_state_map else {}

    def _get_neighbors(self):
        neighbors = {var: set() for var in self.variables}
        for var1, var2 in self.constraints:
            neighbors[var1].add(var2)
            neighbors[var2].add(var1)
        return neighbors

    def get_all_arcs(self):
        arcs = []
        for var1 in self.variables:
            for var2 in self.neighbors[var1]:
                arcs.append((var1, var2))
        return arcs

    def get_domain(self, variable):
        return self.domains.get(variable, set())

    def remove_from_domain(self, variable, value):
        if value in self.domains[variable]:
            self.domains[variable].remove(value)
            return True
        return False

    def get_neighbors_of(self, variable):
        return self.neighbors.get(variable, set())

    def is_consistent(self, var1, val1, var2, val2, constraint_type='different'):
        if constraint_type == 'different':
            return val1 != val2

        if self.puzzle_state_map:
            num1_on_puzzle = self.puzzle_state_map.get(var1)
            num2_on_puzzle = self.puzzle_state_map.get(var2)

            if num1_on_puzzle is None or num2_on_puzzle is None:
                return True

            if val1 == num1_on_puzzle and val2 == num2_on_puzzle:
                return True
            if val1 != num1_on_puzzle and val2 != num2_on_puzzle:
                return True
            if val1 == num1_on_puzzle and val2 != num2_on_puzzle and val1 != val2:  # val1 ok, val2 try other
                return True
            if val1 != num1_on_puzzle and val2 == num2_on_puzzle and val1 != val2:  # val2 ok, val1 try other
                return True

        return False


def revise(csp, xi, xj):
    revised = False
    domain_xi = list(csp.get_domain(xi))
    for x_val in domain_xi:
        satisfies = False
        for y_val in csp.get_domain(xj):
            if csp.is_consistent(xi, x_val, xj, y_val):
                satisfies = True
                break
        if not satisfies:
            csp.remove_from_domain(xi, x_val)
            revised = True
    return revised


def ac3_algorithm(csp):
    queue = list(csp.get_all_arcs())
    while queue:
        (xi, xj) = queue.pop(0)
        if revise(csp, xi, xj):
            if not csp.get_domain(xi):
                return False, csp.domains
            for xk in csp.get_neighbors_of(xi):
                if xk != xj:
                    queue.append((xk, xi))
    return True, csp.domains


def ac3_for_8_puzzle(puzzle_state_matrix):
    variables = []
    initial_domains = {}
    value_to_initial_pos = {}

    for r in range(3):
        for c in range(3):
            var_name = (r, c)
            variables.append(var_name)
            value = puzzle_state_matrix[r][c]
            initial_domains[var_name] = {value} if value != 0 else set(range(1, 9))
            if value != 0:
                value_to_initial_pos[value] = var_name

    puzzle_map_for_constraints = {}
    for r_idx, row in enumerate(puzzle_state_matrix):
        for c_idx, val_in_cell in enumerate(row):
            puzzle_map_for_constraints[(r_idx, c_idx)] = val_in_cell

    constraints = []
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            constraints.append((variables[i], variables[j]))

    csp = CSP(variables, initial_domains, constraints, puzzle_map_for_constraints)

    is_consistent, final_domains = ac3_algorithm(csp)

    result_puzzle = [[0, 0, 0] for _ in range(3)]
    if is_consistent:
        for var, domain_values in final_domains.items():
            r, c = var
            if len(domain_values) == 1:
                result_puzzle[r][c] = list(domain_values)[0]
            elif not domain_values and puzzle_map_for_constraints.get(var) == 0:  # ô trống ban đầu
                result_puzzle[r][c] = 0
            elif not domain_values:  # mâu thuẫn
                result_puzzle[r][c] = -1
    else:
        for r_idx in range(3):
            for c_idx in range(3):
                result_puzzle[r_idx][c_idx] = -1  # Indicate inconsistency

    return {
        "type": "ac3_result",
        "is_consistent": is_consistent,
        "final_domains": final_domains,
        "final_puzzle_state": result_puzzle
    }