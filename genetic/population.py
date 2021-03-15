from enum import Enum
import random


class Direction(Enum):
    SAME_LEVEL = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    HORIZONTAL = 5
    VERTICAL = 6

    @staticmethod
    def get_random_direction(dir_one, dir_two):
        rand = random.randint(1, 2)
        if rand == 1:
            return dir_one
        return dir_two


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_available_directions(self, other, last_dir):
        directions = list()
        if last_dir != Direction.HORIZONTAL:
            if self.x < other.x:
                directions.append(Direction.RIGHT)
            elif self.x > other.x:
                directions.append(Direction.LEFT)
        if last_dir != Direction.VERTICAL:
            if self.y < other.y:
                directions.append(Direction.UP)
            elif self.y > other.y:
                directions.append(Direction.DOWN)
        return directions

    def update_point_coordinates(self, segment):
        if segment.direction == Direction.UP:
            self.y += segment.path_length
        elif segment.direction == Direction.DOWN:
            self.y -= segment.path_length
        elif segment.direction == Direction.LEFT:
            self.x -= segment.path_length
        elif segment.direction == Direction.RIGHT:
            self.x += segment.path_length

    def get_next_point(self, direction, step):
        next_point = Point(self.x, self.y)
        if direction == Direction.UP:
            next_point.y += step
        elif direction == Direction.DOWN:
            next_point.y -= step
        elif direction == Direction.LEFT:
            next_point.x -= step
        elif direction == Direction.RIGHT:
            next_point.x += step
        return next_point

    @staticmethod
    def is_point_inside_coordinates(x, y, plate_x, plate_y):
        if 0 < x < plate_x:
            if 0 < y < plate_y:
                return True
        return False

    def __str__(self):
        return f"Point ({self.x}, {self.y})"

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


class Connection:
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.weight = 1

    def get_right_directions(self):
        if self.start_point.x < self.end_point.x:
            dir_x = Direction.RIGHT
        elif self.start_point.x == self.end_point.x:
            dir_x = Direction.SAME_LEVEL
        else:
            dir_x = Direction.LEFT

        if self.start_point.y < self.end_point.y:
            dir_y = Direction.UP
        elif self.start_point.y == self.end_point.y:
            dir_y = Direction.SAME_LEVEL
        else:
            dir_y = Direction.DOWN

        return dir_x, dir_y

    def __str__(self):
        return f"{self.start_point} -> {self.end_point}"


class Segment:
    def __init__(self, segment_length=0, direction=0):
        self.path_length = segment_length
        self.direction = direction

    def __str__(self):
        return f"Length: {self.path_length}, Direction: {self.direction}"


class Gene:
    def __init__(self):
        self.segments = list()

    def generate_gene(self, start_point, end_point, plate_x, plate_y):
        current_p = Point(start_point.x, start_point.y)
        last_direction = -1
        while not current_p.__eq__(end_point):
            new_data = self.generate_next_segment(current_p, end_point, last_direction, plate_x, plate_y)
            last_direction = new_data[1]
            current_p.update_point_coordinates(new_data[0])

    def generate_next_segment(self, current_point, end_point, last_dir, plate_x, plate_y):
        next_segment = Segment()
        current_dir = Direction.HORIZONTAL
        if current_point.x == end_point.x:
            if last_dir != Direction.VERTICAL:
                current_dir = Direction.VERTICAL
                segment_len = random.randint(1, abs(current_point.y - end_point.y))
                next_segment.path_length = segment_len
                if current_point.y > end_point.y:
                    next_segment.direction = Direction.DOWN
                else:
                    next_segment.direction = Direction.UP
            else:
                current_dir = Direction.HORIZONTAL
                segment_len = random.randint(1, abs(plate_x - current_point.x))
                random_dir = Direction.get_random_direction(Direction.LEFT, Direction.RIGHT)
                next_segment.path_length = segment_len
                next_segment.direction = random_dir

        elif current_point.y == end_point.y:
            if last_dir != Direction.HORIZONTAL:
                current_dir = Direction.HORIZONTAL
                segment_len = random.randint(1, abs(current_point.x - end_point.x))
                next_segment.path_length = segment_len
                if current_point.x > end_point.x:
                    next_segment.direction = Direction.LEFT
                else:
                    next_segment.direction = Direction.RIGHT
            else:
                current_dir = Direction.VERTICAL
                segment_len = random.randint(1, abs(plate_y - current_point.y))
                random_dir = Direction.get_random_direction(Direction.UP, Direction.DOWN)
                next_segment.path_length = segment_len
                next_segment.direction = random_dir

        else:
            directions = current_point.get_available_directions(end_point, last_dir)
            random_dir = directions[random.randint(0, len(directions) - 1)]
            if last_dir == Direction.HORIZONTAL:
                segment_len = random.randint(1, abs(current_point.y - end_point.y))
                current_dir = Direction.VERTICAL
            elif last_dir == Direction.VERTICAL:
                segment_len = random.randint(1, abs(current_point.x - end_point.x))
                current_dir = Direction.HORIZONTAL
            next_segment.path_length = segment_len
            next_segment.direction = random_dir

        self.segments.append(next_segment)
        return next_segment, current_dir

    def get_all_visited_points(self, start_point):
        visited = list()
        visited.append(start_point)
        next_point = start_point
        for segment in self.segments:
            for i in range(segment.path_length):
                next_point = next_point.get_next_point(segment.direction, 1)
                visited.append(next_point)
        return visited

    def calculate_total_path_length(self):
        length = 0
        for segment in self.segments:
            length += segment.path_length
        return length

    def get_segments_amount(self):
        return len(self.segments)

    def is_path_outside(self, start_point, plate_x, plate_y):
        current_p = start_point
        for segment in self.segments:
            if segment.direction == Direction.UP:
                current_p.y += segment.path_length
                if current_p.y > plate_y:
                    return True
            if segment.direction == Direction.DOWN:
                current_p.y -= segment.path_length
                if current_p.y < 0:
                    return True
            if segment.direction == Direction.LEFT:
                current_p.x -= segment.path_length
                if current_p.x < 0:
                    return True
            if segment.direction == Direction.RIGHT:
                current_p.x += segment.path_length
                if current_p.x > plate_x:
                    return True
        return False

    def get_outside_path_length(self, start_point, plate_x, plate_y):
        current_p = Point(start_point.x, start_point.y)
        outside_length = 0

        for segment in self.segments:
            outside_length += Gene.calculate_outside_length(current_p.x, current_p.y,
                                                            segment.path_length, segment.direction, plate_x, plate_y)
            if segment.direction == Direction.UP:
                current_p.y += segment.path_length
            if segment.direction == Direction.DOWN:
                current_p.y -= segment.path_length
            if segment.direction == Direction.LEFT:
                current_p.x -= segment.path_length
            if segment.direction == Direction.RIGHT:
                current_p.x += segment.path_length

        return outside_length

    @staticmethod
    def calculate_outside_length(point_x, point_y, step, direction, plate_x, plate_y):
        length = 0
        for i in range(step):
            next_x = point_x
            next_y = point_y
            if direction == Direction.UP:
                next_y += 1
            if direction == Direction.DOWN:
                next_y -= 1
            if direction == Direction.LEFT:
                next_x -= 1
            if direction == Direction.RIGHT:
                next_x += 1
            if not (Point.is_point_inside_coordinates(point_x, point_y, plate_x, plate_y) and Point.is_point_inside_coordinates(next_x, next_y, plate_x, plate_y)):
                length += 1
            point_x = next_x
            point_y = next_y
        return length

    def __str__(self):
        ret = ""
        for segment in self.segments:
            ret += segment.__str__()
            ret += "\n"
        return ret


class Individual:
    def __init__(self):
        self.genotype = list()

    def generate_genotype(self, connections, plate_x, plate_y):
        for connection in connections:
            gene = Gene()
            gene.generate_gene(connection.start_point, connection.end_point, plate_x, plate_y)
            self.genotype.append(gene)

    def get_intersection_points(self, connections):
        crossing_connections_by_point = dict()
        intersection_points = list()
        crossing_connections = set()
        for i in range(len(self.genotype)):
            visited_points = self.genotype[i].get_all_visited_points(connections[i].start_point)
            for point in visited_points:
                if point in crossing_connections_by_point.keys():
                    crossing_connections_by_point[point].append(connections[i])
                    crossing_connections.add(connections[i])
                else:
                    crossing_connections_by_point[point] = list()
                    crossing_connections_by_point[point].append(connections[i])
        for cross in crossing_connections_by_point.values():
            if len(cross) > 1:
                intersection_points.append(cross)
        return intersection_points, crossing_connections

    def calculate_total_path_length(self):
        total = 0
        for gene in self.genotype:
            total += gene.calculate_total_path_length()
        return total

    def get_total_outside_paths_number(self, connections, plate_x, plate_y):
        total = 0
        for i in range(len(self.genotype)):
            if self.genotype[i].is_path_outside(connections[i].start_point, plate_x, plate_y):
                total += 1
        return total

    def get_total_segments_amount(self):
        total = 0
        for gene in self.genotype:
            total += gene.get_segments_amount()
        return total

    def get_total_outside_path_length(self, connections, plate_x, plate_y):
        total = 0
        for i in range(len(self.genotype)):
            total += self.genotype[i].get_outside_path_length(connections[i].start_point, plate_x, plate_y)
        return total

    def get_intersections_penalty(self, intersection_points):
        total = 0
        point_penalty = 1.0
        for intersection in intersection_points:
            for connection in intersection:
                point_penalty = point_penalty * connection.weight
            total += point_penalty
            point_penalty = 1.0
        return total

    def calculate_total_individual_penalty(self, connections, weights, intersection_points, plate_x, plate_y):
        total = self.calculate_total_path_length() * weights['path_length']
        total += self.get_total_segments_amount() * weights['segments_am']
        total += self.get_total_outside_paths_number(connections, plate_x, plate_y) * weights['outside_number']
        total += self.get_total_outside_path_length(connections, plate_x, plate_y) * weights['outside_length']
        total += self.get_intersections_penalty(intersection_points) * weights ['intersections']

        return total

    def print_genes(self):
        for gene in self.genotype:
            print(gene, "\n")


class Population:
    def __init__(self, plate_x=0, plate_y=0):
        self.plate_x = plate_x
        self.plate_y = plate_y
        self.connections = list()
        self.population = list()
        self.weights = dict()

    def set_weights(self, weights):
        self.weights = weights

    def generate_population(self, individuals_num):
        for i in range(individuals_num):
            next_ind = Individual()
            next_ind.generate_genotype(self.connections, self.plate_x, self.plate_y)
            self.population.append(next_ind)

    def find_best_individual(self):
        for i in range(len(self.population)):
            intersection_points, crossing_connections = self.population[i].get_intersection_points(self.connections)
            print("Penalty for individual: ", i, ":", self.population[i].calculate_total_individual_penalty(self.connections, self.weights, intersection_points, self.plate_x, self.plate_y))
            self.population[i].print_genes()


class Solution:
    def __init__(self):
        self.population = Population()

    def read_solution_from_file(self, filename):
        with open(filename) as fp:
            for count, line in enumerate(fp):
                data = line.rstrip('\n').split(';')
                if count == 0:
                    self.population.plate_x = int(data[0])
                    self.population.plate_y = int(data[1])
                else:
                    self.population.connections.append(Connection(Point(int(data[0]), int(data[1])),
                                                       Point(int(data[2]), int(data[3]))))

    def __str__(self):
        conns = ""
        for c in self.population.connections:
            conns += c.__str__() + "\n"

        return f"Plate: {self.population.plate_x}x{self.population.plate_y}, Connections:\n{conns}"


if __name__ == '__main__':
    solution = Solution()
    solution.read_solution_from_file('./testdata/zad0.txt')
    print(solution)
    ind = Individual()
    ind.generate_genotype(solution.population.connections, solution.population.plate_x, solution.population.plate_y)
    ind.print_genes()
    solution.population.generate_population(10)
    solution.population.set_weights({'path_length': 0.08, 'segments_am': 0.08, 'outside_number': 0.2, 'outside_length': 0.2, 'intersections': 0.3})
    solution.population.find_best_individual()



