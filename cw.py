import random
import copy

#function to calculate the maximum number of non-conflict pairs for n-queens
def calculate_max_fitness(num):
    return (num * (num - 1)) / 2

class Game:
    def __init__(self, size=8, student_ID="2117937"):
        self.size = size
        self.num_ID = student_ID

        k = int(student_ID[-1])
        l = int(student_ID[-2])
        x = k % 8 
        y = l % 8 

        self.init_queen = (x, y)

        self.board = self.generate_board(self.size, self.init_queen)

    #generate a board with random position for n-queens
    def generate_board(self, size, first_queen):
        board = [random.randint(0, size - 1) for _ in range(size)]

        #forcefully place student number queen
        x = first_queen[0] 
        y = first_queen[1]

        board[x] = y

        return board

    #get the total amount of conflicts in the current board
    def get_conflicts(self):
        conflicts = 0

        for i in range(self.size):
            for j in range(i+1, self.size):
                if self.board[i] == self.board[j]:
                    conflicts+=1
                elif abs(self.board[i]-self.board[j]) == abs(i-j):
                    conflicts+=1

        return conflicts

    #calculate the fitness of the board
    def fitness(self):
        all_conflicts = self.get_conflicts()
        max_fitness = calculate_max_fitness(self.size)

        self.fitness_value = max_fitness - all_conflicts
    
    #place the student number queen
    def place_init_queen(self):
        x = self.init_queen[0]
        self.board[x] = self.init_queen[1]

    #generate an empty board (-1 for empty spot), beside the student number queen
    def generate_empty_board(self):
        self.board = [-1 for _ in range(self.size)]
        self.place_init_queen()

    #check if the queen in the index is safe(have no conflicts)
    def is_safe(self, x, y):
        if y < 0 or y > self.size:
            return False
        
        for i in range(self.size):
            if i == x or self.board[i] == -1:
                continue

            if self.board[i] == y or abs(self.board[i] - y) == abs(i-x):
                return False
        
        return True
    
    #place the queen at index
    def place_queen(self, x, y):
        self.board[x] = y

    #check if every spot is occupied
    def all_placed(self):
        for i in range(self.size):
            if self.board[i] == -1:
                return False
        
        return True

    #check the class by board
    def __eq__(self, other) -> bool:
        return isinstance(other, Game) and self.board == other.board
    
    #to_string by board
    def __str__(self) -> str:
        return str(self.board)
    

#tournament selection
def selection(population, size):
    tournament = random.choices(population, k=size)

    parent = sorted(tournament, key=lambda board: board.fitness_value, reverse=True)

    return parent[0], parent[1]

#one-point crossover 
def crossover(parents: tuple[Game, Game], size):
    crossover_point = random.randint(1, size - 2)
    parent_1 = parents[0]
    parent_2 = parents[1]

    child_1 = Game()
    child_2 = Game()

    child_1.board = parent_1.board[:crossover_point] + parent_2.board[crossover_point:]
    child_2.board = parent_2.board[:crossover_point] + parent_1.board[crossover_point:]

    child_1.place_init_queen()
    child_2.place_init_queen()

    return child_1, child_2

#mutation for each element of the child
def mutate(child: Game, size):
    r = [random.random() for _ in range(size)]
    prob = 1/size

    for i in range(size):
        if r[i] < prob:
            random_move = random.randint(0, size - 1)
            child.board[i] = random_move
    child.place_init_queen()
    return child

#main genetic algorithm
def genetic_algorithm(population_size, size, student_num):
    #generate the initial population
    population = []
    for _ in range(population_size):
        population.append(Game(size, student_num))
    
    found_solution = False

    generation = 1

    #keep running till it can find a solution
    while not found_solution: 

        #recalculate the fitness of each board
        for entity in population:
            entity.fitness()
        
        #sort the population by the best to worst
        population = sorted(population, key=lambda board:board.fitness_value, reverse=True)
        
        #get the best solution
        solution:Game = population[0]
        
        #stop if the best solution is solved
        if solution.fitness_value == calculate_max_fitness(solution.size):
            found_solution = True
            return solution

        new_generation = []

        #do selection, crossover and mutate to create new generation
        for _ in range(population_size//2):
            parents = selection(population, size)
            children = crossover(parents, size)

            child_1 = mutate(children[0], size)
            child_2 = mutate(children[1], size)

            new_generation.append(child_1)
            new_generation.append(child_2)

        population = new_generation[:population_size]
        generation+=1
    




POPULATION = 100
SIZE = 8

student_num = "2117937"

empty_board = Game(SIZE, student_num)

empty_board.generate_empty_board()

#generate all solution with the student number with DFS
def generate_all_solutions(solutions, board: Game, x=0):
    #print(board)
    #print(x)
    if board.all_placed():
        return solutions.append(copy.deepcopy(board))

    if board.board[x] == -1:
        new_board = copy.deepcopy(board)
        for y in range(board.size):
            if new_board.is_safe(x, y):
                new_board.place_queen(x, y)
                generate_all_solutions(solutions, new_board, x+1)
    else:
        generate_all_solutions(solutions, board, x+1)
        
            
all_solutions = []
generate_all_solutions(all_solutions, empty_board)

print(len(all_solutions)) 

#genetic search for solutions, keep looping till match the all solutions from DFS
all_genetic_solutions = []
while len(all_genetic_solutions) < len(all_solutions):
    solutions = genetic_algorithm(POPULATION,SIZE,student_num)
    if solutions not in all_genetic_solutions:
        all_genetic_solutions.append(solutions)

            
print("All: ")
for i in all_genetic_solutions:
    print(i)
print(len(all_genetic_solutions))


#write to file
output_file = open("output.txt", "w")
output_file.write("There are " + str(len(all_solutions)) + " solutions\n")
output_file.write("Student number Queen position:" + str(empty_board.init_queen) + "\n")
output_file.write("All board: \n")

for i in all_genetic_solutions:
    board = str(i) + "\n"
    output_file.write(board)

