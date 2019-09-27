import sys
import re
import math

class Coordinate(object):
    def __init__ (self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__ (self):
        return '(' + str("{0:.2f}".format(self.x)) + ',' + str("{0:.2f}".format(self.y)) + ')'

class Line(object):
    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def __str__(self):
        return '(' + str(self.src) + ',' + str(self.dst) + ')'

class StreetDB(object):
    def __init__(self):
        self.Street_Names = []
        self.Coordinates = []

    def add(self, name, points):
        if name in self.Street_Names:
            raise Exception( "Error: Existing Street")

        self.Street_Names.append(name)
        self.Coordinates.append(points)

    def change(self, name, points):
        exists = False
        for i in range(len(self.Street_Names)):
            if name == self.Street_Names[i]:
                exists = True
                self.Coordinates[i] = points

        if not exists:
            raise Exception("Error: No such existing street")

    def remove(self, name):
        exists = False
        for i in list(reversed(range(len(self.Street_Names)))):
            if name == self.Street_Names[i]:
                exists = True
                self.Street_Names.pop(i)
                self.Coordinates.pop(i)
                
        if not exists:
            raise Exception("Error: No such existing street")
    
    def generate(self):
        line_db_list = []
        intersection = []
        vertex = []
        edge = []
        for i in range(len(self.Coordinates)):
            line_list = []
            for j in range(len(self.Coordinates[i])-1):
                line_list.append(Line(self.Coordinates[i][j], self.Coordinates[i][j+1]))
            line_db_list.append(line_list)

        for i in range(len(line_db_list)):
            for j in range(i+1, len(line_db_list)):
                line1 = line_db_list[i]
                line2 = line_db_list[j]
                for a in range(len(line1)):
                    for b in range(len(line2)):
                        intersect_point = intersect(line1[a], line2[b])
                        if isinstance(intersect_point, Coordinate):
                            vertex.append(intersect_point)
                            vertex.append(line1[a].src)
                            vertex.append(line1[a].dst)
                            vertex.append(line2[b].src)
                            vertex.append(line2[b].dst)
                            intersection.append(intersect_point)

                        if isinstance(intersect_point, list):
                            vertex.append(line1[a].src)
                            vertex.append(line1[a].dst)
                            vertex.append(line2[b].src)
                            vertex.append(line2[b].dst)
                            vertex.append(intersect_point[0])
                            vertex.append(intersect_point[1])
                            intersection.append(intersect_point[0])
                            intersection.append(intersect_point[1])

        # Remove duplicate intersection points
        for m in range(len(intersection)):
            for n in list(reversed(range(m+1, len(intersection)))):
                if intersection[m].x == intersection[n].x and intersection[m].y == intersection[n].y:
                    intersection.pop(n)

        # Remove duplicate vertex
        for m in range(len(vertex)):
            for n in list(reversed(range(m+1, len(vertex)))):
                if vertex[m].x == vertex[n].x and vertex[m].y == vertex[n].y:
                    vertex.pop(n)

        # Find edge
        for i in range(len(line_db_list)):
            for j in range(len(line_db_list[i])):
                findEdge(line_db_list[i][j], intersection, edge)

        map_vertex = []

        print_vertex(vertex, map_vertex)
        print_edge(edge, map_vertex)


def intersect(l1, l2):
    x1, y1 = l1.src.x, l1.src.y
    x2, y2 = l1.dst.x, l1.dst.y
    x3, y3 = l2.src.x, l2.src.y
    x4, y4 = l2.dst.x, l2.dst.y
    
    x_list1 = [x1, x2]
    x_list1.sort()
    x_list2 = [x3, x4]
    x_list2.sort()  
 
    y_list1 = [y1,y2]
    y_list1.sort()
    y_list2 = [y3,y4]
    y_list2.sort()

    list_x = [x1, x2, x3, x4]
    list_x.sort()
    list_y = [y1, y2, y3, y4]
    list_y.sort()
    
    intersect_list = []
 
    if x1 != x2 and x3 != x4: 
        m1 = (y2-y1)/(x2-x1)
        m2 = (y4-y3)/(x4-x3)
        
        b1 = y1 - (m1 * x1)
        b2 = y3 - (m2 * x3)
    
        if m1 != m2 :
            xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
            xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
            xcoor = xnum / xden

            ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
            yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
            ycoor = ynum / yden

            if x_list1[0] <= xcoor <= x_list1[1] and x_list2[0] <= xcoor <= x_list2[1] and y_list1[0] <= ycoor <= y_list1[1] and y_list2[0] <= ycoor <= y_list2[1]:
                return Coordinate(xcoor, ycoor)
            else:
                return 0
        else:
            if b1 == b2:
                if (x_list1[1] > x_list2[0] > x_list1[0]) or (x_list2[1] > x_list1[0] > x_list2[0]):
                    intersect_list.append(Coordinate(list_x[1], list_y[1]))
                    intersect_list.append(Coordinate(list_x[2], list_y[2]))

                    return intersect_list
                elif x_list1[1] == x_list2[0]:
                    return Coordinate(list_x[1], list_y[1])
                else:
                    return 0
            else:
                return 0
    elif x1 != x2 or x3 != x4:
            xnum = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4))
            xden = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))
            xcoor =  xnum / xden

            ynum = (x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)
            yden = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
            ycoor = ynum / yden
          
            if x_list1[0] <= xcoor <= x_list1[1] and x_list2[0] <= xcoor <= x_list2[1] and y_list1[0] <= ycoor <= y_list1[1] and y_list2[0] <= ycoor <= y_list2[1]:
                return Coordinate (xcoor, ycoor)
            else:
                return 0
    else:
        if x1 == x2 == x3 == x4:
            if list_y[1] != list_y[2]:
                intersect_list.append(Coordinate(x1, list_y[1]))
                intersect_list.append(Coordinate(x2, list_y[2]))

                return intersect_list
            else:
                return Coordinate(x1, list_y[1])
        else:
            return 0


def findEdge(line, intersect, edge):
    flag = False     
    point_edge = [line.src, line.dst]

    for k in range(len(intersect)):        
        if (intersect[k] != line.src or intersect[k] != line.dst) and isBetween(line, intersect[k]):
            point_edge.append(intersect[k])
            flag = True

    if flag:
        point_edge.sort(compare)
        for m in range(len(point_edge)):
            for n in list(reversed(range(m+1, len(point_edge)))):
                if point_edge[m].x == point_edge[n].x and point_edge[m].y == point_edge[n].y:
                    point_edge.pop(n)

        for i in range(len(point_edge)-1):
            edge.append(Line(point_edge[i], point_edge[i+1]))
            i += 1
        return
    else:
        return


def isBetween(line, intersect):
    return distance(line.src, intersect) + distance(intersect, line.dst) - distance(line.src, line.dst) < 0.00001


def distance(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)


def compare(src, dst):
    if src.x == dst.x:
        if src.y < dst.y:
            return -1
        else:
            return 1

    if src.x < dst.x:
        return -1
    else:
        return 1


def print_vertex(vertex, map_vertex):
    sys.stdout.write("V = {\n")
    j = 1
    for i in range(len(vertex)):
        map_vertex.append([j, vertex[i]])
        sys.stdout.write(str(j) + ': ' + str(vertex[i]) + '\n')
        j += 1
    sys.stdout.write("}\n")


def print_edge(edge, map_vertex):
    sys.stdout.write("E = {\n")
    src = ""
    dst = ""

    edge_set = set()

    # for i in range(len(map_vertex)): print(map_vertex[i][1])
    for e in range(len(edge)):
        for v in range(len(map_vertex)):
            if edge[e].src == map_vertex[v][1]:
                src = str(map_vertex[v][0])

            if edge[e].dst == map_vertex[v][1]:
                dst = str(map_vertex[v][0])
    
        edge_set.add(str(src) + ', ' + str(dst))

    for i in range(len(edge_set)):
        if len(edge_set) > 1:
            sys.stdout.write('<' + edge_set.pop() + '>,\n')
        else:
            sys.stdout.write('<' + edge_set.pop()  + '>\n')
    
    sys.stdout.write("}\n")


def read_cmd(line, cmd):
    line = line.strip()
    cmd.append(line[0])
    if line[0] == 'a' or line[0] == 'c':
        if len(line) > 1 and line[1] != ' ':
            raise Exception("Error: Missing space before street name")

        index = read_stname(cmd, line, 2)
        index += 1
        if index < len(line) and line[index] != ' ':
            raise Exception("Error: Missing space after street name")

        index = read_vertex(cmd, line, index)

    elif line[0] == 'r':
        if line[1] != ' ':
            raise Exception("Error: Missing space before street name")

        index = read_stname(cmd, line, 2)
        index = skip_space(line, index + 1)
        if index != len(line):
            raise Exception("Error: Invalid command for remove")

    elif line[0] == 'g':
        index = skip_space(line, 1)
        if index != len(line):
            raise Exception("Error: Invalid command for generate graph")

    else:
        raise Exception("Error: Incorrect command")


def skip_space(line, index):
    while index < len(line) and line[index].isspace():
        index += 1
    return index


def read_stname(cmd, line, index):
    index = skip_space(line, index)
    if line[index] != '"':
        raise Exception("Error: Missing left quotation")

    index += 1
    stname = ""
    while index < len(line) and line[index] != '"' :
        stname = stname + line[index].lower()
        index += 1

    regex = re.compile(r'^[a-zA-Z ]+$')
    if index == len(line):
        raise Exception("Error: Missing right quotation")

    if re.match(regex, stname):
        cmd += [stname]
        return index
    else:
        raise Exception("Error: Invalid street name")


def read_vertex(cmd, line, index):
    index = skip_space(line, index)
    if index >= len(line):
        return index

    if line[index] == '(':
        index += 1
        index = read_coordinate(cmd, line, index)
        index = skip_space(line, index)
        if index < len(line) and line[index] == ",":
            index += 1
        else:
            raise Exception("Error: Missing comma")

        index = read_coordinate(cmd, line, index)
        index = skip_space(line, index)
        if index < len(line) and line[index] == ')':
            index = read_vertex(cmd, line, index + 1)
            return index
        else:
            raise Exception("Error: Missing closing bracket")


def read_coordinate(cmd, line, index):
    index = skip_space(line, index)
    if index >= len(line):
        raise Exception("Error: Missing co-ordinates after (")

    coordinate = ""
    if line[index] == '-':
        coordinate = "-"
        index += 1

    digit = "0123456789"
    if (digit.find(line[index])) < 0 :
        raise Exception("Error: Invalid co-ordinates")

    while index < len(line) and digit.find(line[index]) >= 0 :
        coordinate = coordinate + line[index]
        index += 1
    cmd.append(int(coordinate))
    return index


def list_points(cmd):
    points = []
    index = 2
    while index < len(cmd):
        points.append(Coordinate(cmd[index], cmd[index+1]))
        index += 2

    if len(points) > 1:
        return points
    else:
        raise Exception("Error: Street with one or no point cannot be added")


def main():
    ### YOUR MAIN CODE GOES HERE

    ### sample code to read from stdin.
    ### make sure to remove all spurious print statements as required
    ### by the assignment
    db = StreetDB()
    while True:
        line = sys.stdin.readline()
        if line == '':
            break
        print('read a line:', line)

        cmd = []

        try:
            read_cmd(line, cmd)
            if cmd[0] == 'a':
                db.add(cmd[1], list_points(cmd))
            elif cmd[0] == 'c':
                db.change(cmd[1], list_points(cmd))
            elif cmd[0] == 'r':
                db.remove(cmd[1])
            elif cmd[0] == 'g':
                db.generate()
            else:
                raise Exception("Error: Invalid command")
        except Exception as ex:
            print(ex)
            continue

        sys.stdout.flush()

    print('Finished reading input')
    # return exit code 0 on successful termination
    sys.exit(0)


if __name__ == '__main__':
    main()
