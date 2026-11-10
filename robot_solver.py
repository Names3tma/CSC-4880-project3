import sys
import random

# read file
def parse_cnf(path):
    num_vars = num_clauses = 0
    clauses = []

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                _, _, v, c = line.split()
                num_vars = int(v)
                num_clauses = int(c)
                continue
            temp_clauses = [int(x) for x in line.split()]
            assert temp_clauses[-1] == 0, "line does not end in 0"
            clauses.append(temp_clauses[:-1])
    assert len(clauses) == num_clauses, "unequal clauses from header"

    occurences = [[] for _ in range(num_vars + 1)]
    for i, clause in enumerate(clauses):
        for lit in clause:
            occurences[abs(lit)].append(i)

    return num_vars, clauses, occurences

# verify CNF solution
def walksat(num_vars, clauses, occurences, max_flips=1000000):
    assignment = [False] + [random.random() < 0.5 for _ in range(num_vars)]

    # Checks singular literal can be satisfied
    def lit_true(lit):
        return assignment[abs(lit)] == (lit > 0)

    true_count = [sum(lit_true(l) for l in c) for c in clauses]
    unsat = {i for i, t in enumerate(true_count) if t == 0}

    # changes the vars around
    def flip(var):
        assignment[var] = not assignment[var]
        for i in occurences[var]:
            lit = var if var in clauses[i] else -var
            if lit_true(lit):
                true_count[i] += 1
                if true_count[i] == 1:
                    unsat.discard(i)
            else:
                true_count[i] -= 1
                if true_count[i] == 0:
                    unsat.add(i)

    for _ in range(max_flips):
        if not unsat:
            return assignment #solved
        clause = clauses[random.choice(tuple(unsat))]
        var = abs(random.choice(clause))
        flip(var)

    return None #failed(timed out)

def main():
    if len(sys.argv) != 2:
        print("no file asked")
        sys.exit(1)

    path = sys.argv[1]
    num_vars, clauses, occurences = parse_cnf(path)
    result = walksat(num_vars, clauses, occurences)

    if result is None: 
        print("timed out")
        return

    print("success")
    for i in range(1, num_vars + 1):
        print(f"x{i} = {result[i]}")

if __name__ == "__main__":
    main()