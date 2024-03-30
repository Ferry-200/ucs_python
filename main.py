from queue import PriorityQueue

class Point:
    name = ""
    # 从这个点射出去的线。
    lines = []

    def __init__(self, name: str, lines: list):
        self.name = name
        self.lines = lines

class Line:
    cost = 0
    edge_1 = Point(None, None)
    edge_2 = Point(None, None)
    
    def __init__(self, cost: int, edge_1: Point, edge_2: Point):
        self.cost = cost
        self.edge_1 = edge_1
        self.edge_2 = edge_2
    
    def next_of(self, point: Point) -> Point:
        if(point == self.edge_1):
            return self.edge_2
        else:
            return self.edge_1
        
# data of map
# points
POINTS = {
    "a": Point("a", None), "b": Point("b", None), "c": Point("c", None),
    "d": Point("d", None), "e": Point("e", None), "f": Point("f", None),
    "h": Point("h", None), "p": Point("p", None), "q": Point("q", None),
    "r": Point("r", None), "s": Point("s", None), "g": Point("g", None)
}

# lines
LINES = {
    1: Line(2, POINTS["a"], POINTS["b"]), 2: Line(2, POINTS["a"], POINTS["c"]),
    3: Line(3, POINTS["c"], POINTS["f"]), 4: Line(2, POINTS["f"], POINTS["g"]),
    5: Line(1, POINTS["b"], POINTS["d"]), 6: Line(8, POINTS["c"], POINTS["d"]),
    7: Line(3, POINTS["d"], POINTS["s"]), 8: Line(2, POINTS["d"], POINTS["e"]),
    9: Line(9, POINTS["e"], POINTS["s"]), 10: Line(8, POINTS["e"], POINTS["h"]),
    11: Line(2, POINTS["e"], POINTS["r"]), 12: Line(2, POINTS["f"], POINTS["r"]),
    13: Line(1, POINTS["p"], POINTS["s"]), 14: Line(4, POINTS["h"], POINTS["p"]),
    15: Line(4, POINTS["h"], POINTS["q"]), 16: Line(15, POINTS["p"], POINTS["q"])
}

# link points and lines
POINTS["a"].lines = []
POINTS["b"].lines = [LINES[1]]
POINTS["c"].lines = [LINES[2]]
POINTS["d"].lines = [LINES[5], LINES[6], LINES[8]]
POINTS["e"].lines = [LINES[10], LINES[11]]
POINTS["f"].lines = [LINES[3], LINES[4]]
POINTS["h"].lines = [LINES[14], LINES[15]]
POINTS["p"].lines = [LINES[16]]
POINTS["q"].lines = []
POINTS["r"].lines = [LINES[12]]
POINTS["s"].lines = [LINES[7], LINES[9], LINES[13]]
POINTS["g"].lines = []

class PointAndCost:
    # cost so far
    cost = 0
    point = Point(None, None)

    def __init__(self, cost: int, point: Point):
        self.cost = cost
        self.point = point
        
    # define the '<' operation between PointAndCosts
    # the PriorityQueue need '<' operation to compare items when sorting the queue
    def __lt__(self, other):
        return self.cost < other.cost

def build_path(came_from: dict[Point, Point], start: Point, goal: Point) -> list[Point]:
    curr = goal
    path = []
    while curr != start:
        path.append(curr)
        curr = came_from[curr]
    path.append(start)
    path.reverse()
    return path

def uniform_cost_search(start: Point, goal: Point) -> int:
    frontier = PriorityQueue[PointAndCost]()
    frontier.put(PointAndCost(0, start))
    explored = set[Point]()

    # save the path
    # the path is saved as a -> b, b -> c, c -> d, ...
    # the function build_path() will turn it into a list like [a, b, c, d, ...],
    # which is easier to read
    came_from = dict[Point, Point]()
    came_from[start] = None

    while(not frontier.empty()):
        current_state = frontier.get()
        cost_so_far = current_state.cost
        current = current_state.point

        if(current == goal):
            path = build_path(came_from, start, goal)
            for p in path:
                print(p.name, end=", ")
            
            return cost_so_far
        
        explored.add(current)
        for l in current.lines:
            next = l.next_of(current)
            if(next not in explored):
                new_cost = cost_so_far + l.cost
                frontier.put(PointAndCost(new_cost, next))
                came_from[next] = current
    return None

cost = uniform_cost_search(POINTS["s"], POINTS["g"])
print(cost)