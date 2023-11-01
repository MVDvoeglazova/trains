# -*- coding: cp1251 -*-
from math import cos, sin, radians, atan
class Line():

    def __init__(self, begin: tuple, end: tuple):

        self.begin = begin
        self.end = end

        self.start_x = self.begin[0]
        self.start_y = self.begin[1]

        self.end_x = self.end[0]
        self.end_y = self.end[1]

        self.points = [begin, end]
        self.k = None
        self.b = None


        # для случая, когда уравнение имееет вид: x = const or y = const
        self.x = None
        self.y = None
        self.constant = False

    def straight_line(self):
        '''
        Рассчет коэффициентов прямой (k, b)
        '''
        if -0.9 <= self.start_x - self.end_x <= 0.9:
            self.x = self.start_x
            self.constant = self.start_x
        elif -0.9 <= self.start_y - self.end_y <= 0.9:
            self.y = self.start_y
            self.constant = self.start_y
        elif (self.start_x - self.end_x) != 0:
            self.k = (self.start_y - self.end_y) / (self.start_x - self.end_x)
            self.b = self.end_y - self.k * self.end_x

    def f(self, x):
        ''' Возвращает значение координаты у при заданной х'''
        if not self.constant:
            return self.k * x + self.b
        return self.constant

    def lenght(self):
        ''' Возвращает длину линии'''

        return (((self.start_x - self.end_x) ** 2 + (self.start_y - self.end_y) ** 2) ** 0.5)

    def update(self):
        '''
        Обновление границ линии с учетом новых точек,
        пересчет коэффициентов прямой
        '''
        self.points = sorted(self.points)
        self.begin = self.points[0]
        self.end = self.points[-1]
        self.start_x = self.begin[0]
        self.start_y = self.begin[1]
        self.end_x = self.end[0]
        self.end_y = self.end[1]
        self.straight_line()

    def isline(self, new_point: tuple, eps: float = 3):
        '''
        Проверка новой точки на принадлежность к линии
        и запись в список точек линии при положительном исходе
         '''
        new_x = new_point[0]
        new_y = new_point[1]
        if not self.constant:
            if new_y - eps <= self.f(new_x) <= new_y + eps:
                if new_point not in self.points:
                    self.points.append(new_point)
                return True
        elif self.x:
            if self.x - eps <= new_x <= self.x + eps:
                self.points.append(new_point)
                return True
        else:
            if self.y - eps <= new_y <= self.y + eps:
                self.points.append(new_point)
                return True
        return False

    def alpha(self):
        if self.k:
            x = self.end[0] - self.begin[0]
            y = self.end[1] - self.begin[1]
            return atan(y/x)
        elif self.x:
            return radians(90)
        elif self.y:
            return radians(0)



class Angle():

    def __init__(self, current_point, line1: Line, line2: Line):
        self.alpha = radians(90.0)
        self.x_train = current_point[0]
        self.y_train = current_point[1]
        self.line1 = line1
        self.line2 = line2
        self.points = line1.points + line2.points
        self.x_intersection = None
        self.y_intersection = None

    def intersection_point(self):
        '''
        точка пересечения прямых, образующих угол
        '''
        if self.line1.constant:
            if self.line1.x:
                self.x_intersection = self.line1.x
                if self.line2.y:
                    self.y_intersection = self.line2.y
                else:
                    self.y_intersection = self.line2.k * self.x_intersection + self.line2.b

            else:
                self.y_intersection = self.line1.y
                if self.line2.x:
                    self.x_intersection = self.line2.x
                else:
                    self.x_intersection = self.y_intersection / self.line2.k - self.line2.b

        else:
            if self.line2.constant:
                if self.line2.x:
                    self.x_intersection = self.line2.x
                else:
                    self.y_intersection = self.line2.y


            elif self.line1.k - self.line2.k != 0:
                self.x_intersection = (self.line2.b - self.line1.b) / (self.line1.k - self.line2.k)
                self.y_intersection = self.line1.k * self.x_intersection + self.line1.b

    def lenght(self, x, y):
        ''' Возвращает длину отрезка от поезда до заданной точки угла '''
        return (((self.x_train - x) ** 2 + (self.y_train - y) ** 2) ** 0.5)

    def isborder(self):
        '''
        len_intersection -  длина от поезда до точки пересечения
        len_random_point - длина от поезда до рандомной точки линий, образующих угол
    
        Возвращает True в случае, если угол является чатью границ поля
        '''
        # random_point = random.choice(self.points)
        random_point = self.points[0]
        # while random_point[0] == self.x_intersection and random_point[1] == self.y_intersection:
        #   random_point = random.choice(self.points)

        len_intersection = self.lenght(self.x_intersection, self.y_intersection)

        len_random_point = self.lenght(random_point[0], random_point[1])
        if len_intersection > 1.01 * len_random_point:
            return True
        else:
            return False


class Circle():

    def __init__(self, points: list, current_point: tuple):
        
        self.current_point = current_point
        self.points = points
        self.start_point = None
        self.end_point = None
        self.mid_point = None

        self.radius = None
        self.xc = None
        self.yc = None

    def normal(self, point: tuple, line: Line) -> Line:
        if not line.constant:
            k = -1 / line.k
            b = (point[0] / line.k + point[1])
            x2 = point[0] + 100
            y2 = k * x2 + b
            return Line((point[0], point[1]), (x2, y2))

        elif line.x:
            return Line((point[0], point[1]), (point[0] + 100, point[1]))

        else:
            return Line((point[0], point[1]), (point[0], point[1] + 100))

    def median(self, point_1: tuple, point_2: tuple) -> tuple:
        x = 0.5 * (point_1[0] + point_2[0])
        y = 0.5 * (point_1[1] + point_2[1])
        return x, y

    def lenght(self, point: tuple) -> float:
        ''' Возвращает длину отрезка от центра окружности до точки'''

        return (((self.xc - point[0]) ** 2 + (self.yc - point[1]) ** 2) ** 0.5)

    def update(self):
        self.points = sorted(self.points)
        self.start_point = self.points[0]
        self.mid_point = self.points[len(self.points) // 2]
        self.end_point = self.points[-1]

        line1 = Line(self.start_point, self.end_point)
        line2 = Line(self.start_point, self.mid_point)

        line1.update()
        line2.update()

        line1 = self.normal(self.median(self.start_point, self.end_point), line1)
        line2 = self.normal(self.median(self.start_point, self.end_point), line2)

        line1.update()
        line2.update()

        angle = Angle(self.current_point, line1, line2)
        angle.intersection_point()
        self.xc = angle.x_intersection
        self.yc = angle.y_intersection

        if self.xc and self.yc:
            self.radius = self.lenght(self.mid_point)

    def iscircle(self, new_point):
        
        if self.xc and self.yc:
            new_r = ((new_point[0] - self.xc) ** 2 + (new_point[1] - self.yc) ** 2) ** 0.5 
            if self.radius/4 <= new_r < self.radius * (5/4):
                self.points.append(new_point)
                return True
        return False



def isLine(points):
    start = points[0]
    end = points[-1]
    line = Line(start, end)
    line.update()

    it = len(points) - 2

    while it > 0 and line.isline(points[it]):
        it -= 1

    line.update()
    return line.isline(points[it]), line



def isAngle(points: list[tuple], current_point, MIN: float = 5, flag: bool = 0) -> tuple:
    def sort_key(e):
        return e[1]

    if flag:
        points = sorted(points, key=sort_key)
    else:
        points = sorted(points)
    start = points[0]
    end = points[1]
    line_1 = Line(start, end)
    line_1.update()

    it = 2
    len_points = len(points) - 1

    while it != len_points and line_1.isline(points[it]):
        it += 1
        line_1.update()
    if it == len_points:
        return False, None

    start = points[it]
    end = points[-1]
    line_2 = Line(start, end)
    line_2.update()


    while it != len_points and line_2.isline(points[it]):
        it += 1
        line_2.update()

    if len(line_1.points) == 2 or len(line_2.points) == 2:
        return False, None

    if line_1.lenght() > MIN and line_2.lenght() > MIN:
        angle = Angle(current_point, line_1, line_2)
        angle.intersection_point()
        
        return True, angle
    else:
        return False, None


def isCircle(points: list[tuple], current_point):
    start = points[0]
    mid = points[len(points) // 2]
    finish = points[-1]

    circle = Circle([start, mid, finish], current_point)
    circle.update()

    it = 1
    lenght = len(points) - 1

    while it != lenght and circle.iscircle(points[it]):
        it += 1
        circle.update()
    return circle.iscircle(points[it]), circle



def what_is_it(points: list[tuple], current_point: tuple) -> str:
    if not points:
        return 'not points', None
    output = isLine(points)
    if output[0]:
        return 'Line', output[1]
    else:
        output = isAngle(points, current_point)
        #print(points)
        if output[0]:
            return 'Angle', output[1]
        else:
            output = isAngle(points, current_point, flag=1)

            if output[0]:
                return 'Angle', output[1]
            else:
                output = isCircle(points, current_point)

                if output[0]:
                    return 'Circle', output[1]
                else:
                    return 'Unknow', None


