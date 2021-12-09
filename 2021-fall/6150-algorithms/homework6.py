# pulp
import pulp
import random

# Question 1a
# Set n (people), m (skills), and d (skills per person)
n = 500
m = 500
d = 25

# Generate skills and people
skills = list(range(m))
people = [list() for x in range(n)]
for i in range(n):
    people[i] = random.sample(skills, d)

## Question 1b
# Binary variable that represents the whether a person was chosen
possible_chosen_people = [p for p in range(n)]
x = pulp.LpVariable.dicts('choose', possible_chosen_people, lowBound=0, upBound=1, cat=pulp.LpContinuous)

# The problem
prob = pulp.LpProblem("SetCover", pulp.LpMinimize)

# The objective function (minimize total number of selected people)
prob += pulp.lpSum(x)

# Constraints
# Every skill must be covered
for i, skill in enumerate(skills):
    prob += (
        # Sum of all people with skill must be at least 1
        pulp.lpSum([x[p] for p in possible_chosen_people if skill in people[p]]) >= 1,
        f"Every skill covered {i}",
    )


prob.solve()
print(prob)
print(x)
print("")


print(pulp.value(prob.objective))
print(pulp.LpStatus[prob.status])

# Write coefficients out to file
with open('LPoutput.txt', 'w') as f:
    f.write(f"objective: {pulp.value(prob.objective)}\n\n")
    for p in range(n):
        f.write(f"{p}: {pulp.value(x[p])}\n")


# The below only works for integer programming

# a = []
# for chosen_person in possible_chosen_people:
#     if x[chosen_person].value() >= 1:
#         print(chosen_person, people[chosen_person])
#         a += [y for y in people[chosen_person]]


# print(f"solution contains every skill: {list(set(a)) == skills}")



# Question 1d
random.seed(10)
hired = []
t = 8
for p in range(n):
    hiring_prob = min(1, t * pulp.value(x[p]))
    
    if hiring_prob > random.random():
        hired.append(people[p])

hired_skills = list(set([val for sublist in hired for val in sublist]))
uncovered = 500 - len(hired_skills)
print(len(hired))
print(uncovered)







## Question 2
import random
import matplotlib.pyplot as plt

N = 10 ** 7
arr = [0] * N

for i in range(N):
    arr[random.randint(0, N - 1)] += 1

plt.show(block=True)
fig = plt.hist(arr, bins=20)
plt.title('Requests distribution among servers, randomly')
plt.xlabel("Load (number of requests)")
plt.ylabel("Number of servers (millions)")
plt.savefig('fig2a.png')

arr2 = [0] * N

for i in range(N):
    first_index = random.randint(0, N - 1)
    second_index = random.randint(0, N - 1)
    if arr[first_index] < arr[second_index]:
        arr[first_index] += 1
    else:
        arr[second_index] += 1
        

plt.show(block=True)
fig = plt.hist(arr, bins=20)
plt.title('Requests distribution among servers, less loaded of 2 servers')
plt.xlabel("Load (number of requests)")
plt.ylabel("Number of servers (millions)")
plt.savefig('fig2b.png')
