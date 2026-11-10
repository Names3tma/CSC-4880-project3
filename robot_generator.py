import random
import os

# Convert guest c sit on seat s to a number variable (because .cnf file doesn't understand letter variable)
# Note that g and c count from 1 not 0
def seat_variable(g, s, n):
    return (g - 1) * n + s

# List all the seat variable that guest g is able to sit on
def guest_rules(g, n):
    lst = []
    for i in range(1, n + 1):
        lst.append(seat_variable(g, i, n))
    return lst

# List all the pairs of seat variable so there's no one take 2 seat
def guest_at_most_1(g, n):
    lst = []
    for i in range(1, n + 1):
        for j in range (i + 1, n + 1):
            lst.append([-seat_variable(g, i, n), -seat_variable(g, j, n)])

    return lst

# List all the seat variable so make no one have to stand and all the pairs of seat variable so there's no one take 2 seat
def all_guest_rules(n):
    lst = []
    for i in range(1, n + 1):
        lst.append(guest_rules(i, n))
    for j in range(1, n + 1):
        lst.extend(guest_at_most_1(j, n))
    return lst

# Make seat s have to have any guest sit on it
def seat_rules(s, n):
    lst = []
    for i in range(1, n + 1):
        lst.append(seat_variable(i, s, n))
    return lst

# Make seat s can't have more than 2 guests
def seat_at_most_1(s, n):
    lst = []
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            lst.append([-seat_variable(i, s, n), -seat_variable(j, s, n)])

    return lst

# Make seat s have to have any guest sit on it and can't have more than 2 guests
def all_seat_rules(n):
    lst = []
    for i in range(1, n + 1):
        lst.append(seat_rules(i, n))
    for j in range(1, n + 1):
        lst.extend(seat_at_most_1(j, n))
    return lst

# a and b are beefing so has to make sure they don’t sit next to each other
def enemy_rules(a, b, n):
    lst = []
    for i in range(1, n):
        lst.append([-seat_variable(a, i, n), -seat_variable(b, i + 1, n)])
        lst.append([-seat_variable(b, i, n), -seat_variable(a, i + 1, n)])
    return lst

# a and b secretly have crushes on each other so seat each pair next to one another
def friend_rules(a, b, n):
    lst = []
    for i in range(1, n + 1):
        lst_seat = [-seat_variable(a, i, n)]
        if i - 1 >= 1:
            lst_seat.append(seat_variable(b, i - 1, n))
        if i + 1 <= n:
            lst_seat.append(seat_variable(b, i + 1, n))
        lst.append(lst_seat)

    return lst

# Add guest and seat rules to a completely rule
def base_rule(n):
    lst = []
    lst.extend(all_guest_rules(n))
    lst.extend(all_seat_rules(n))
    return lst

# Given a seat order, list all the pair sit next to each other
def possible_friends(order):
    lst = []
    for i in range(len(order) - 1):
        lst.append([order[i], order[i + 1]])
    return lst

# Given a seat order, list all the pair doesn't sit next to each other
def possible_enemies(order):
    lst = []
    for i in range(len(order) - 1):
        for j in range(i + 1, len(order)):
            if [order[i], order[j]] not in possible_friends(order) and [order[j], order[i]] not in possible_friends(order):
                lst.append([order[i], order[j]])
    return lst

# Randomize all the seat order and get random friend and enemy pairs from order
def choose_random_pairs(n, p, q):
    order = list(range(1, n + 1))
    random.shuffle(order)
    friends = random.sample(possible_friends(order), p)
    enemies = random.sample(possible_enemies(order), q)
    return order, friends, enemies

# Create problem
def generate(n, p, q):
    order, friends, enemies = choose_random_pairs(n, p, q)
    clauses = base_rule(n)
    for a, b in friends:
        clauses.extend(friend_rules(a, b, n))
    for c, d in enemies:
        clauses.extend(enemy_rules(c, d, n))
    return clauses, order

# Problem checker
def check(clauses, order, n):
    lst_true_order = []
    for i in range(n):
        lst_true_order.append(seat_variable(order[i], i + 1, n))

    for i in clauses:
        ok = False
        for j in i:
            if j < 0:
                if -j not in lst_true_order:
                    ok = True
            else:
                if j in lst_true_order:
                    ok = True
        if ok == False:
            return False
    return True

# Copy the clauses to .cnf file
def write_cnf(fn, clauses, n, p, q):
    with open(fn, "w") as f:
        f.write("c Tan Party: n=" + str(n) + ", p=" + str(p) + ", q=" + str(q) + "\n")
        f.write("p cnf " + str(n * n) + " " + str(len(clauses)) + "\n")
        for i in clauses:
            for j in i:
                f.write(str(j) + " ")
            f.write("0\n")

# Create all the problems
def generate_probs(count, n, p, q):
    os.makedirs("problems", exist_ok=True)
    for i in range(count):
        random.seed(i)
        clauses, order = generate(n, p, q)
        if check(clauses, order, n) == False:
            print("There's a bug in problem " + str(i))
        write_cnf("problems/problem_" + str(i) + ".cnf", clauses, n, p, q)

if __name__ == "__main__":
    # 100 problems, each problem has 75 guests, 5 pairs are friends and 15 pairs are enemies
    generate_probs(100, 75, 5, 15)
