class Sudoku_AI_Solver:
    def __init__(self):
        self.domains = {
            (i, j): set(range(1, 10)) for i in range(9) for j in range(9)
        }

    def load_from_file(self, filename):
        """Load Sudoku puzzle from file with error handling to ensure clear instructions"""
        try:
            with open(filename, 'r') as f:
                lines = [line.strip().replace(" ", "") for line in f if line.strip()]

            if len(lines) != 9:
              #ensure there's no empty spaces even though we've added line correction (first issue encountered)
                raise ValueError("File must contain exactly 9 lines")

            for i in range(9):
                if len(lines[i]) != 9:
                    raise ValueError(f"Line {i+1} must contain exactly 9 characters")
                for j in range(9):
                    val = int(lines[i][j])
                    if val == 0:
                        self.domains[(i, j)] = set(range(1, 10))
                    elif 1 <= val <= 9:
                        self.domains[(i, j)] = {val}
                    else:
                        raise ValueError(f"Invalid value {val} at position ({i}, {j})")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")
        except ValueError as e:
            raise ValueError(f"Invalid Sudoku file: {str(e)}")

    def enforce_node_consistency(self):
        for cell in self.domains:
            if len(self.domains[cell]) == 1:
                val = next(iter(self.domains[cell]))
                self.domains[cell] = {val}

    def revise(self, x, y):
        revised = False
        if len(self.domains[y]) == 1:
            val_y = next(iter(self.domains[y]))
            if val_y in self.domains[x]:
                if len(self.domains[x]) > 1:
                    self.domains[x].remove(val_y)
                    revised = True
        return revised

    def ac3(self):
        queue = [(x, y) for x in self.domains for y in self.get_neighbors(x)]
        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.get_neighbors(x):
                    if z != y:
                        queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        return all(len(assignment[cell]) == 1 for cell in assignment)

    def consistent(self, assignment):
        for cell in assignment:
            if len(assignment[cell]) == 1:
                val = next(iter(assignment[cell]))
                for neighbor in self.get_neighbors(cell):
                    if len(assignment[neighbor]) == 1:
                        if val == next(iter(assignment[neighbor])):
                            return False
        return True

    def order_domain_values(self, var, assignment):
        def count_conflicts(value):
            count = 0
            for neighbor in self.get_neighbors(var):
                if value in assignment[neighbor]:
                    count += 1
            return count
        return sorted(assignment[var], key=count_conflicts)

    def select_unassigned_variable(self, assignment):
        unassigned = [v for v in assignment if len(assignment[v]) > 1]
        return min(unassigned, key=lambda var: (len(assignment[var]), -len(self.get_neighbors(var))))

    def backtrack(self, assignment):
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = {k: v.copy() for k, v in assignment.items()}
            new_assignment[var] = {value}
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result
        return None

    def get_neighbors(self, cell):
        i, j = cell
        neighbors = set()
        for k in range(9):
            if k != j:
                neighbors.add((i, k))
            if k != i:
                neighbors.add((k, j))
        top_left_i = 3 * (i // 3)
        top_left_j = 3 * (j // 3)
        for a in range(top_left_i, top_left_i + 3):
            for b in range(top_left_j, top_left_j + 3):
                if (a, b) != cell:
                    neighbors.add((a, b))
        return neighbors

    def solve(self):
        self.enforce_node_consistency()
        if not self.ac3():
            print("AC-3 failed")
            return None
        return self.backtrack(self.domains)

    def display(self, assignment):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                val = next(iter(assignment[(i, j)]))
                print(val if val != 0 else ".", end=" ")
            print()

if __name__ == "__main__":
    solver = Sudoku_AI_Solver()
    try:
        solver.load_from_file("sudoku_easy.txt")
        solution = solver.solve()
        if solution:
            print("Solution found:")
            solver.display(solution)
        else:
            print("No solution found.")
    except Exception as e:
        print(f"Error: {str(e)}")
