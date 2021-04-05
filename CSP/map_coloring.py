import random
import matplotlib.pyplot as plt
import copy
COLORS = ['purple', 'red', 'lime', 'green', 'grey']
COUNTER = 0


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.available_connections = list()
        self.domain = list()
        self.color = ""

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def get_connection_if_valid(self, connections, points):
        valid_point = None
        not_available = list()

        for point in self.available_connections:
            if self.is_connection_valid(connections, point, points):
                valid_point = point
                if self in point.available_connections:
                    point.available_connections.remove(self)
                not_available.append(point)
                break
            else:
                not_available.append(point)
                if self in point.available_connections:
                    point.available_connections.remove(self)
        for bad in not_available:
            self.available_connections.remove(bad)
        return valid_point

    def is_connection_valid(self, connections, connection_candidate, points):
        for conn in connections:
            if Point.do_connections_intersect(self, connection_candidate, conn[0], conn[1]):
                return False
        return True

    @staticmethod
    def on_segment(p, q, r):
        if q != p and q != r:
            if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
                    (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
                return True
        return False

    @staticmethod
    def orientation(p, q, r):
        value = (float(q.y - p.y) * float(r.x - q.x)) - (float(r.y - q.y) * float(q.x - p.x))

        # clockwise
        if value > 0:
            return 1
        # counterclockwise
        elif value < 0:
            return 2
        # collinear
        else:
            return 0

    @staticmethod
    def do_connections_intersect(p1, q1, p2, q2):
        o1 = Point.orientation(p1, q1, p2)
        o2 = Point.orientation(p1, q1, q2)
        o3 = Point.orientation(p2, q2, p1)
        o4 = Point.orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4 and (p1 != p2 and p1 != q2 and q1 != q2 and q1 != p2):
            return True

        if o1 == 0 and Point.on_segment(p1, p2, q1):
            return True
        if o2 == 0 and Point.on_segment(p1, q2, q1):
            return True
        if o3 == 0 and Point.on_segment(p2, p1, q2):
            return True
        if o4 == 0 and Point.on_segment(p2, q1, q2):
            return True

        return False


class Graph:

    def __init__(self, edge_x, edge_y):
        self.edge_x = edge_x
        self.edge_y = edge_y
        self.connections = list()
        self.connections_dictionary = dict()
        self.points = list()
        self.points_amount = 0

    def generate_points(self):
        max_points_am = self.edge_y * self.edge_x
        self.points_amount = random.randint(round(0.25 * max_points_am), round(0.5 * max_points_am))
        for i in range(self.points_amount):
            new_point = False
            while not new_point:
                next_x = random.randint(0, self.edge_x - 1)
                next_y = random.randint(0, self.edge_y - 1)
                new_point = self.is_point_new(next_x, next_y)
                if new_point:
                    next_point = Point(next_x, next_y)
                    self.points.append(next_point)
                    self.connections_dictionary[next_point] = list()

    def set_beginning_available_points(self):
        for i in range(self.points_amount):
            new_connections = self.points[0:i] + self.points[i + 1:self.points_amount]
            new_connections.sort(key=lambda p: (p.x - self.points[i].x) ** 2 + (p.y - self.points[i].y) ** 2)
            self.points[i].available_connections = new_connections

    def set_beginning_domain(self, colors_am):
        for i in range(self.points_amount):
            for j in range(colors_am):
                self.points[i].domain.append(COLORS[j])

    def generate_connections(self):
        unfinished_points = list()
        for point in self.points:
            unfinished_points.append(point)

        while len(unfinished_points) > 0:
            if len(unfinished_points) == 1:
                current_point = unfinished_points.pop(0)
            else:
                rand_index = random.randint(0, len(unfinished_points) - 1)
                current_point = unfinished_points.pop(rand_index)
            connected_point = current_point.get_connection_if_valid(self.connections, self.points)
            if connected_point is not None:
                self.connections_dictionary[current_point].append(connected_point)
                self.connections_dictionary[connected_point].append(current_point)
                self.connections.append((current_point, connected_point))
            if len(current_point.available_connections) > 0:
                unfinished_points.append(current_point)

    def begin_backtracking(self, colors, colors_am):
        assignment = [None] * self.points_amount
        assignment[0] = colors[0]
        result = self.backtracking(assignment, 1, colors[0:colors_am])
        if result:
            self.draw_colored_graph(result)
        else:
            print("Could not find any solutions.")

    def backtracking(self, assignment, position, colors):
        global COUNTER
        COUNTER += 1
        if not self.is_assignment_valid(assignment):
            return False
        if self.points_amount == position:
            return assignment
        for color in colors:
            assignment[position] = color
            next_assignment = copy.deepcopy(assignment)
            sol = self.backtracking(next_assignment, position + 1, colors)
            if sol:
                return sol
            else:
                del next_assignment
        return False

    def is_assignment_valid(self, assignment):
        for point in self.points:
            point_index = self.points.index(point)
            for neighbour in self.connections_dictionary[point]:
                neighbour_ind = self.points.index(neighbour)
                if assignment[point_index] == assignment[neighbour_ind] and assignment[point_index] is not None and assignment[neighbour_ind] is not None:
                    return False
        return True

    def assignment_valid(self, point, color):
        for p in self.connections_dictionary[point]:
            if p.color == color:
                return False
        return True

    def begin_forward_checking(self, colors_num):
        self.set_beginning_domain(colors_num)
        result = self.forward_checking(0)
        if all(p.color != '' for p in self.points):
            self.draw_colored_graph_forward_checking()
        return result

    def forward_checking(self, position):
        global COUNTER
        COUNTER += 1
        for color in self.points[position].domain:
            if self.assignment_valid(self.points[position], color):
                self.points[position].color = color
                for conn in self.connections_dictionary[self.points[position]]:
                    if color in conn.domain:
                        conn.domain.remove(color)
                if position + 1 < len(self.points):
                    sol = self.forward_checking(position + 1)
                    if sol:
                        return sol
                    else:
                        for conn in self.connections_dictionary[self.points[position]]:
                            if color not in conn.domain:
                                conn.domain.append(color)
        return False

    def is_point_new(self, x, y):
        for point in self.points:
            if point.x == x and point.y == y:
                return False
        return True

    def draw_graph(self):
        for conn in self.connections:
            plt.plot([conn[0].x, conn[1].x], [conn[0].y, conn[1].y], 'blue')
        for point in self.points:
            plt.plot(point.x, point.y, 'o', color="black", markersize=12)
        plt.show()

    def draw_colored_graph(self, assignment):
        for conn in self.connections:
            plt.plot([conn[0].x, conn[1].x], [conn[0].y, conn[1].y], 'blue')
        for point in self.points:
            plt.plot(point.x, point.y, 'o', color=assignment[self.points.index(point)], markersize=12)
        plt.show()

    def draw_colored_graph_forward_checking(self):
        for conn in self.connections:
            plt.plot([conn[0].x, conn[1].x], [conn[0].y, conn[1].y], 'blue')
        for point in self.points:
            plt.plot(point.x, point.y, 'o', color=point.color, markersize=12)
        plt.show()


def test_csp(plate_x, plate_y, colors_am):
    g = Graph(plate_x, plate_y)
    g.generate_points()
    g.set_beginning_available_points()
    g.generate_connections()
    g.draw_graph()
    g.begin_backtracking(COLORS, colors_am)
    # g.begin_forward_checking(colors_am)


if __name__ == '__main__':
    test_csp(5, 5, 4)
    print(COUNTER)



