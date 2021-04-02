import copy

NATIONALITIES = ['Norwegian', 'English', 'Danish', 'German', 'Swedish']
COLORS = ['Red', 'White', 'Blue', 'Yellow', 'Green']
TOBACCO = ['Light', 'Pipe', 'Unfiltered', 'Menthol', 'Cigar']
BEVERAGES = ['Tea', 'Coffee', 'Milk', 'Water', 'Beer']
PETS = ['Cat', 'Dog', 'Fish', 'Bird', 'Horse']


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
        assignment = [House(0), House(1), House(2), House(3), House(4)]
        res = self.backtracking(0, assignment, 0, available_values)
        if res:
            return res
        else:
            print('No solution.')

    def backtracking(self, feature, assignment, value_index, values):
        if not self.check_constraints(assignment):
            return False
        if self.are_values_finished(values):
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

    def are_values_finished(self, values):
        for val in values:
            if len(val) > 0:
                return False
        return True

    def check_constraints(self, assignment):
        if not Solution.constraint_one(assignment):
            return False
        if not Solution.constraint_two(assignment):
            return False
        if not Solution.constraint_three(assignment):
            return False
        if not Solution.constraint_four(assignment):
            return False
        if not Solution.constraint_five_and_nine(assignment):
            return False
        if not Solution.constraint_six(assignment):
            return False
        if not Solution.constraint_seven(assignment):
            return False
        if not Solution.constraint_eight(assignment):
            return False
        if not Solution.constraint_ten(assignment):
            return False
        if not Solution.constraint_eleven(assignment):
            return False
        if not Solution.constraint_twelve(assignment):
            return False
        if not Solution.constraint_thirteen(assignment):
            return False
        if not Solution.constraint_fourteen(assignment):
            return False
        if not Solution.constraint_fifteen(assignment):
            return False
        return True

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
        for i in range(5):
            if assignment[i].color == 'Yellow':
                if assignment[i].tobacco != 'Cigar' and assignment[i].tobacco is not None:
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
        if assignment[2].beverage != 'Milk' and assignment[2].beverage is not None:
            return False
        return True

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


if __name__ == '__main__':
    s = Solution()
    res = s.begin_backtracking()
    for r in res:
        print(r)
