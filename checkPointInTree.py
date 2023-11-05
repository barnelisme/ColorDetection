import math


class QuadNode:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.points = []
        self.children = [None] * 4


def insert(node, point_index, x, y):
    if node is None:
        return

    if len(node.points) < 4:
        node.points.append(point_index)
        return

    if x < node.x + node.width / 2:
        if y < node.y + node.height / 2:
            if node.children[0] is None:
                node.children[0] = QuadNode(node.x, node.y, node.width / 2, node.height / 2)
            insert(node.children[0], point_index, x, y)
        else:
            if node.children[1] is None:
                node.children[1] = QuadNode(node.x, node.y + node.height / 2, node.width / 2, node.height / 2)
            insert(node.children[1], point_index, x, y)
    else:
        if y < node.y + node.height / 2:
            if node.children[2] is None:
                node.children[2] = QuadNode(node.x + node.width / 2, node.y, node.width / 2, node.height / 2)
            insert(node.children[2], point_index, x, y)
        else:
            if node.children[3] is None:
                node.children[3] = QuadNode(node.x + node.width / 2, node.y + node.height / 2, node.width / 2,
                                            node.height / 2)
            insert(node.children[3], point_index, x, y)


def is_within_radius_of_any(point, radius, points_dict):
    for existing_point in points_dict:
        distance = calculate_distance(existing_point, point)
        if distance <= radius:
            return True
    return False


def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Example usage
root = QuadNode(0, 0, 10, 10)
#point_dict = []  # List of points

#new_point = (4, 5)
testListOfPoints = [[2, 2], [2, 3], [5, 3], [3.2, 4]]
radius = 2.2

def checkNewPoint(new_point, listOfPoints):
        if not is_within_radius_of_any(new_point, radius, listOfPoints):
            index = len(listOfPoints)
            listOfPoints.append(new_point)
            insert(root, index, new_point[0], new_point[1])
            print(f"Added {new_point} to the list of points")
            return True
        else:
            print(f"Point {new_point} already exists in the list")
            return False

# print("Points in the list:")
# for point in point_dict:
#     print(point)
