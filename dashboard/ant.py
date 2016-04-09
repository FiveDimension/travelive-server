from collections import defaultdict
import random, math


def greedy_tour(graph, start_node):
    """
    Compute a greedy TSP solution for a given graph
    """
    solution = [start_node]
    visited = set([start_node])

    nodes = graph.keys()

    # Complete the rest of the tour
    for i in range(len(nodes) - 1):
        last_node = solution[i]
        new_node = min([n for n in nodes if n not in visited],
                       key=lambda n: graph[last_node][n])
        solution.append(new_node)
        visited.add(new_node)
    # Close the tour
    solution.append(solution[0])
    return solution


def chain_cost(g, node_list):
    """
    Compute the cost of a chain in a graph
    """
    if len(node_list) <= 1:
        return 0
        total_cost = 0
        for i in range(len(node_list) - 1):
            cost = g[node_list[i]][node_list[i + 1]]
            if cost is None:
                return None
        total_cost += cost
        return total_cost


class AntSystemTSP:
    def __init__(self, graph, no_ants=None, alpha=1.0, beta=3.0, rho=0.5, iterations=10):
        self.graph = graph
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.iterations = iterations
        self.pheromones = defaultdict(lambda: defaultdict(lambda: 0))
        self.choice_value = defaultdict(lambda: defaultdict(lambda: 0))
        # Assign a start node
        self.nodes = graph.keys()
        self.start_node = self.nodes[0]
        # Assign a number of ants
        if not no_ants:
            self.no_ants = len(self.nodes)
        else:
            self.no_ants = no_ants
            self.ants = []
            # Init the pheromone matrix
            self.__init_pheromones()
            # Best so far cost/tour
            self.best_tour = greedy_tour(self.graph, self.start_node)
            self.best_cost = chain_cost(self.graph, self.best_tour)


    def __iter__(self):
        for _ in xrange(self.iterations):
            self.__build_solutions()
            self.__update_pheromones()
            yield (self.best_cost, self.best_tour)


    def __global_evaporation(self):
        """Updates the pheromone matrix"""
        for i in self.nodes:
            for j in self.nodes:
                self.pheromones[i][j] = self.pheromones[j][i] = self.pheromones[i][j] * (1 - self.rho)


    def __compute_pheromones0(self):
        return (float(self.no_ants)) / (float(chain_cost(self.graph, greedy_tour(self.graph, self.start_node))))


    def __init_pheromones(self):
        tau0 = self.__compute_pheromones0()
        for i in self.nodes:
            for j in self.nodes:
                if i != j:
                    self.pheromones[i][j] = self.pheromones[i][j] = tau0
                    self.__compute_heuristic()


    def __compute_heuristic(self):
        for i in self.nodes:
            for j in self.nodes:
                dist = self.graph[i][j]
                if dist > 0:
                    niu = 1.0 / dist
                else:
                    niu = 1.0 / 0.0001
                self.choice_value[i][j] = self.choice_value[j][i] = (
                    math.pow(self.pheromones[i][j], self.alpha) *
                    math.pow(niu, self.beta))


    def __deposit_pheromones(self):
        """ Perform the pheromone deposit operation for all the ants"""
        for ant in self.ants:
            delta_tau = 1.0 / chain_cost(self.graph, ant)
            for i in range(len(self.nodes)):
                self.pheromones[ant[i]][ant[i + 1]] = \
                    self.pheromones[ant[i + 1]][ant[i]] = delta_tau


    def __update_pheromones(self):
        """ Update the pheromones and the heuristic matrix"""
        self.__global_evaporation()
        self.__deposit_pheromones()
        self.__compute_heuristic()


    def __decision_rule(self, start_node, visited):
        """Decides what node to add next to the solution"""
        possible_nodes = [n for n in self.nodes if n not in visited]
        probabilities = [self.choice_value[start_node][n]
                         for n in possible_nodes]
        max_p = sum(probabilities)
        pick = random.uniform(0, max_p)
        accu = probabilities[0]
        idx = 0
        while pick > accu:
            idx += 1
            accu += probabilities[idx]
        return possible_nodes[idx]


    def __build_solutions(self):
        """Each ant builds a solution"""
        self.ants = []
        for _ in xrange(self.no_ants):
            # Init the ant
            ant = []

            # Choose a start node
            start_node = random.choice(self.nodes)
            ant.append(start_node)
            visited = set([start_node])

            # Build the tour
            for _ in xrange(len(self.nodes) - 1):
                choice = self.__decision_rule(ant[-1], visited)
                ant.append(choice)
                visited.add(choice)

            # Close the tour
            ant.append(start_node)
            self.ants.append(ant)

        #Update best tour
        for ant in self.ants:
            cost = chain_cost(self.graph, ant)
            if cost < self.best_cost:
                self.best_cost = cost
                self.best_tour = ant


if __name__ == "__main__":
    tsp_graph = defaultdict(lambda: defaultdict(lambda: float("inf")))

    # Generate a random graph
    for i in range(100):
        for j in range(100):
            if i != j:
                tsp_graph[i][j] = tsp_graph[j][i] = random.randint(1, 100)
    print(tsp_graph)

    ant_system = AntSystemTSP(tsp_graph, iterations=200)
    for solution in ant_system:
        print solution