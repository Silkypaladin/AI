import copy
import math

NATIONALITIES = ['Norwegian', 'English', 'Danish', 'German', 'Swedish']
COLORS = ['Red', 'White', 'Blue', 'Yellow', 'Green']
TOBACCO = ['Light', 'Pipe', 'Unfiltered', 'Menthol', 'Cigar']
BEVERAGES = ['Tea', 'Coffee', 'Milk', 'Water', 'Beer']
PETS = ['Cat', 'Dog', 'Fish', 'Bird', 'Horse']
HEURISTICS_COUNTER = 0
BACKTRACKING_COUNTER = 0


class House:

    def __init__(self, house_number):
        self.house_number = house_number
        self.features = [None, None, None, None, None]
        self.nationality = None
        self.color = None
        self.tobacco = None
        self.beverage = None
        self.pet = None

    def set_feature(self, feature_index, feature):
        self.features[feature_index] = feature
        if feature_index == 0:
            self.nationality = feature
        if feature_index == 1:
            self.color = feature
        if feature_index == 2:
            self.tobacco = feature
        if feature_index == 3:
            self.beverage = feature
        if feature_index == 4:
            self.pet = feature

    def __str__(self):
        res = 'House: ' + str(self.house_number) + "\n"
        res += 'Nationality: ' + self.nationality + "\n"
        res += 'Color: ' + self.color + "\n"
        res += 'Tobacco: ' + self.tobacco + "\n"
        res += 'Beverage: ' + self.beverage + "\n"
        res += 'Pet: ' + self.pet + "\n"
        return res


class Solution:

    def begin_backtracking(self):
        available_values = [NATIONALITIES, COLORS, TOBACCO, BEVERAGES, PETS]
        assignment = [House('0'), House('1'), House('2'), House('3'), House('4')]
        res = self.backtracking(0, assignment, 0, available_values)
        if res:
            return res
        else:
            print('No solution.')

    def backtracking(self, feature, assignment, value_index, values):
        global BACKTRACKING_COUNTER
        BACKTRACKING_COUNTER += 1
        if not self.check_constraints(assignment):
            return False
        if Solution.are_values_finished(values):
            return assignment
        available_values = copy.deepcopy(values)
        next_value = available_values[feature].pop(0)
        n_index = value_index + 1
        next_feature = feature
        if n_index == 5:
            n_index = 0
            next_feature = next_feature + 1
        for i in range(5):
            if assignment[i].features[feature] is None:
                next_assignment = copy.deepcopy(assignment)
                next_assignment[i].set_feature(feature, next_value)
                solution = self.backtracking(next_feature, next_assignment, n_index, available_values)
                if solution:
                    return solution
                else:
                    del next_assignment
        return False

    def begin_augmented_backtracking(self):
        available_values = [NATIONALITIES, COLORS, TOBACCO, BEVERAGES, PETS]
        assignment = [House(0), House(1), House(2), House(3), House(4)]
        domains = list()
        for i in range(5):
            cp = copy.deepcopy(available_values)
            domains.append(cp)
        result = self.augmented_backtracking(0, 0, assignment, domains)
        if result:
            return result
        else:
            print("No solution found")

    def augmented_backtracking(self, position, feature, assignment, domains):
        global HEURISTICS_COUNTER
        HEURISTICS_COUNTER += 1
        if not self.check_constraints(assignment):
            return False
        if Solution.is_any_domain_empty(domains):
            return False
        if Solution.is_every_value_assigned(assignment):
            return assignment
        self.lcv(assignment, domains, position, feature)
        for i in domains[position][feature]:
            next_assignment = copy.deepcopy(assignment)
            next_domains = copy.deepcopy(domains)
            next_assignment[position].set_feature(feature, i)
            next_domains[position][feature] = [i]
            self.ac3(next_assignment, next_domains, position, feature, i)
            house_index, feature_index = self.mrv(next_assignment, next_domains)
            solution = self.augmented_backtracking(house_index, feature_index, next_assignment, next_domains)
            if solution:
                return solution
            else:
                del next_assignment
                del next_domains
        return False

    @staticmethod
    def mrv(assignment, domains):
        min_val = math.inf
        feature_index = 0
        house_index = 0
        for i in range(len(domains)):
            for j in range(len(domains[i])):
                if assignment[i].features[j] is None:
                    if len(domains[i][j]) < min_val:
                        house_index = i
                        feature_index = j
                        min_val = len(domains[i][j])
        return house_index, feature_index

    def lcv(self, assignment, domains, house_index, feature):
        features_order = list()
        assignment_copy = copy.deepcopy(assignment)
        for i in domains[house_index][feature]:
            features_order.append([i, 0])
        for i in features_order:
            what = i[0]
            assignment_copy[house_index].set_feature(feature, what)
            test = 0
            for j in range(5):
                for k in range(len(domains[j])):
                    assignment_test_copy = copy.deepcopy(assignment_copy)
                    for x in domains[j][k]:
                        assignment_test_copy[j].set_feature(k, x)
                        if not self.check_constraints(assignment_test_copy):
                            test += 1
                    del assignment_test_copy
            i[1] = test
        del assignment_copy
        features_order.sort(key=lambda elem: elem[1])
        new_features = list()
        for i in features_order:
            new_features.append(i[0])
        domains[house_index][feature] = new_features

    def ac3(self, assignment, domains, house_index, feature, feature_elem):
        for i in range(5):
            if i != house_index:
                if feature_elem in domains[i][feature]:
                    domains[i][feature].remove(feature_elem)
        for i in range(5):
            for j in range(0, len(domains[i])):
                assignment_copy = copy.deepcopy(assignment)
                for x in domains[i][j]:
                    assignment_copy[i].set_feature(j, x)
                    if not self.check_constraints(assignment_copy):
                        domains[i][j].remove(x)
                del assignment_copy

    @staticmethod
    def are_values_finished(values):
        for val in values:
            if len(val) > 0:
                return False
        return True

    @staticmethod
    def is_every_value_assigned(assignment):
        for house in assignment:
            for feature in house.features:
                if feature is None:
                    return False
        return True

    @staticmethod
    def is_any_domain_empty(domains):
        for dom in domains:
            for feature_dom in dom:
                if len(feature_dom) < 1:
                    return True
        return False

    @staticmethod
    def constraint_one(assignment):
        if assignment[0].nationality == 'Norwegian' or assignment[0].nationality is None:
            return True
        return False

    @staticmethod
    def constraint_two(assignment):
        for house in assignment:
            if house.color == 'Red' and (house.nationality != 'English' and house.nationality is not None):
                return False
        return True

    @staticmethod
    def constraint_three(assignment):
        if assignment[4].color == 'Green':
            return False
        if assignment[0].color == 'White':
            return False
        for i in range(4):
            if assignment[i].color == 'Green':
                if assignment[i+1].color != 'White' and assignment[i + 1].color is not None:
                    return False
        return True

    @staticmethod
    def constraint_four(assignment):
        for house in assignment:
            if house.nationality == 'Danish' and (house.beverage != 'Tea' and house.beverage is not None):
                return False
        return True

    @staticmethod
    def constraint_five_and_nine(assignment):
        for i in range(5):
            if assignment[i].tobacco == 'Light':
                if 0 < i < 4:
                    if assignment[i - 1].pet != 'Cat' and assignment[i - 1].pet is not None and assignment[i + 1].pet != 'Cat' and assignment[i + 1].pet is not None:
                        return False
                    if assignment[i - 1].beverage != 'Water' and assignment[i - 1].beverage is not None and assignment[i + 1].beverage != 'Water' and assignment[i + 1].beverage is not None:
                        return False
                elif i == 4:
                    if assignment[i - 1].pet != 'Cat' and assignment[i - 1].pet is not None:
                        return False
                    if assignment[i - 1].beverage != 'Water' and assignment[i - 1].beverage is not None:
                        return False
                else:
                    if assignment[i + 1].pet != 'Cat' and assignment[i + 1].pet is not None:
                        return False
                    if assignment[i + 1].beverage != 'Water' and assignment[i + 1].beverage is not None:
                        return False
        return True

    @staticmethod
    def constraint_six(assignment):
        for house in assignment:
            if house.color == 'Yellow' and (house.tobacco != 'Cigar' and house.tobacco is not None):
                return False
        return True

    @staticmethod
    def constraint_seven(assignment):
        for house in assignment:
            if house.nationality == 'German' and (house.tobacco != 'Pipe' and house.tobacco is not None):
                return False
        return True

    @staticmethod
    def constraint_eight(assignment):
        return assignment[2].beverage == 'Milk' or assignment[2].beverage is None

    @staticmethod
    def constraint_ten(assignment):
        for house in assignment:
            if house.tobacco == 'Unfiltered' and (house.pet != 'Bird' and house.pet is not None):
                return False
        return True

    @staticmethod
    def constraint_eleven(assignment):
        for house in assignment:
            if house.nationality == 'Swedish' and (house.pet != 'Dog' and house.pet is not None):
                return False
        return True

    @staticmethod
    def constraint_twelve(assignment):
        for i in range(5):
            if assignment[i].nationality == 'Norwegian':
                if 0 < i < 4:
                    if assignment[i - 1].color != 'Blue' and assignment[i - 1].color is not None and assignment[i + 1].color != 'Blue' and assignment[i + 1].color is not None:
                        return False
                elif i == 4:
                    if assignment[i - 1].color != 'Blue' and assignment[i - 1].color is not None:
                        return False
                else:
                    if assignment[i + 1].color != 'Blue' and assignment[i + 1].color is not None:
                        return False
        return True

    @staticmethod
    def constraint_thirteen(assignment):
        for i in range(5):
            if assignment[i].pet == 'Horse':
                if 0 < i < 4:
                    if assignment[i - 1].color != 'Yellow' and assignment[i - 1].color is not None and assignment[i + 1].color != 'Yellow' and assignment[i + 1].color is not None:
                        return False
                elif i == 4:
                    if assignment[i - 1].color != 'Yellow' and assignment[i - 1].color is not None:
                        return False
                else:
                    if assignment[i + 1].color != 'Yellow' and assignment[i + 1].color is not None:
                        return False
        return True

    @staticmethod
    def constraint_fourteen(assignment):
        for house in assignment:
            if house.tobacco == 'Menthol' and (house.beverage != 'Beer' and house.beverage is not None):
                return False
        return True

    @staticmethod
    def constraint_fifteen(assignment):
        for house in assignment:
            if house.color == 'Green' and (house.beverage != 'Coffee' and house.beverage is not None):
                return False
        return True

    @staticmethod
    def check_constraints(assignment):
        return all([
            Solution.check_constraint_basic(assignment, 'house_number', 0, 'nationality', 'Norwegian'),
            Solution.check_constraint_basic(assignment, 'color', 'Red', 'nationality', 'English'),
            Solution.check_constraint_left_to(assignment, 'color', 'Green', 'color', 'White'),
            Solution.check_constraint_basic(assignment, 'nationality', 'Danish', 'beverage', 'Tea'),
            Solution.check_constraint_next_to(assignment, 'tobacco', 'Light', 'pet', 'Cat'),
            Solution.check_constraint_basic(assignment, 'color', 'Yellow', 'tobacco', 'Cigar'),
            Solution.check_constraint_basic(assignment, 'nationality', 'German', 'tobacco', 'Pipe'),
            Solution.check_constraint_basic(assignment, 'house_number', 2, 'beverage', 'Milk'),
            Solution.check_constraint_next_to(assignment, 'tobacco', 'Light', 'beverage', 'Water'),
            Solution.check_constraint_basic(assignment, 'tobacco', 'Unfiltered', 'pet', 'Bird'),
            Solution.check_constraint_basic(assignment, 'nationality', 'Swedish', 'pet', 'Dog'),
            Solution.check_constraint_next_to(assignment, 'nationality', 'Norwegian', 'color', 'Blue'),
            Solution.check_constraint_next_to(assignment, 'pet', 'Horse', 'color', 'Yellow'),
            Solution.check_constraint_basic(assignment, 'tobacco', 'Menthol', 'beverage', 'Beer'),
            Solution.check_constraint_basic(assignment, 'color', 'Green', 'beverage', 'Coffee')
        ])

    @staticmethod
    def check_constraint_left_to(assignment, attr1, attr1_val, attr2, attr2_val):
        if getattr(assignment[-1], attr1) and getattr(assignment[-1], attr1) == attr1_val:
            return False

        if getattr(assignment[0], attr2) and getattr(assignment[0], attr2) == attr2_val:
            return False

        for (left_h, right_h) in zip(assignment, assignment[1:]):
            if getattr(left_h, attr1) == attr1_val and getattr(right_h, attr2) and getattr(right_h, attr2) != attr2_val:
                return False
        return True

    @staticmethod
    def check_constraint_basic(assignment, attr1, attr1_val, attr2, attr2_val):
        for house in assignment:
            if getattr(house, attr1) == attr1_val and getattr(house, attr2) and getattr(house, attr2) != attr2_val:
                return False
        return True

    @staticmethod
    def check_constraint_next_to(assignment, attr1, attr1_val, attr2, attr2_val):
        for i in range(5):
            if getattr(assignment[i], attr1) == attr1_val:
                if i == 0:
                    if getattr(assignment[i + 1], attr2) and getattr(assignment[i + 1], attr2) != attr2_val:
                        return False
                elif i == 4:
                    if getattr(assignment[i - 1], attr2) and getattr(assignment[i - 1], attr2) != attr2_val:
                        return False
                else:
                    if getattr(assignment[i - 1], attr2) and getattr(assignment[i - 1], attr2) != attr2_val and \
                            getattr(assignment[i + 1], attr2) and getattr(assignment[i + 1], attr2) != attr2_val:
                        return False
        return True

    # @staticmethod
    # def check_constraints(ass):
    #     if not Solution.constraint_one(ass):
    #         return False
    #     if not Solution.constraint_two(ass):
    #         return False
    #     if not Solution.constraint_three(ass):
    #         return False
    #     if not Solution.constraint_four(ass):
    #         return False
    #     if not Solution.constraint_five_and_nine(ass):
    #         return False
    #     if not Solution.constraint_six(ass):
    #         return False
    #     if not Solution.constraint_seven(ass):
    #         return False
    #     if not Solution.constraint_eight(ass):
    #         return False
    #     if not Solution.constraint_ten(ass):
    #         return False
    #     if not Solution.constraint_eleven(ass):
    #         return False
    #     if not Solution.constraint_twelve(ass):
    #         return False
    #     if not Solution.constraint_thirteen(ass):
    #         return False
    #     if not Solution.constraint_fourteen(ass):
    #         return False
    #     if not Solution.constraint_fifteen(ass):
    #         return False
    #     return True


if __name__ == '__main__':
    s = Solution()
    res = s.begin_augmented_backtracking()
    print(BACKTRACKING_COUNTER)
    print(HEURISTICS_COUNTER)
    for r in res:
        print(r)
