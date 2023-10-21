from math import cos, sin, radians
from random import uniform
from game.locator import Locator


def isline(k, b, x1, y1, eps = 0.01):
    if y1-eps <= k * x1 + b <= y1 + eps:
        return True
    else:
        return False

def iscircle(xc, yc, r, x1, y1, eps = 0.05):

    if (1-eps) * r**2<= (x1-xc)**2 + (y1-yc)**2 <= (1+eps) * r**2:
        return True
    else:
        return False

#получение коэффициентов уравнения прямой по 2 точкам
def straight_line(x1, y1, x2, y2):
            if x1-x2 != 0:
                k = (y1 - y2) / (x1 - x2)
            else:
                k = 0
            b = y2 - k*x2
            return k, b

#реализация уравнения прямой, возвращает значение y по заданному х
def f(k,x,b):
            return k*x + b

#возвращает коэф. уравнения прямой нормальной к заданной 
def normal(x1, y1, k):
        return -1/k, (x1/k+y1)

#середина отрезка
def median(x1, y1, x2, y2):
        x = 0.5 * (x1 + x2)
        y = 0.5 * (y1 + y2)
        return x, y
# возвоащает точку пересечения прямых 
def line_intersection(k1, b1, k2, b2):
    if k1-k2!=0:
        x = (b2-b1)/(k1-k2)
        y = k1*x + b1
    else: return
    return x, y
 #длина отрезка между заданными точками 
def len_a_b(x1, y1, x2, y2):
    return (((x1-x2)**2 + (y1-y2)**2)**0.5)


color1 = (255, 0, 0)
color2 = (0, 120, 0)
color3 = (255, 0, 150)




class Train:

    def __init__(self,
                 x0: float,
                 y0: float,
                 alpha0: float,
                 v_max: float,
                 locator: Locator,
                 ):

        self.alpha = alpha0  # строительная ось от оси x против часовой стрелки
        self.x = x0
        self.y = y0
        self.v_max = 15
        self.locator = locator
        self.v = 5
        self.distance = None
        self.auto = True


        self.lastpoint = (x0, y0)
        self.points = list()
        #circles = (xc, yc, r, list: points)
        self.points_of_circles = list()
        self.circles = dict()
        self.lines = dict()
        self.dictionary_of_shapes = dict()






    def update(self, x: float, y: float):

        # TODO в будющих версиях боты сами будут счислять свое положение
        if self.auto:
            self.x = x
            self.y = y

        # дергаем измерение локатора
        measurement = self.locator.measurement

        if measurement['query']:
            x_q, y_q, alpha_q = measurement['query'][0]
            self.distance = measurement['distance']

            if self.distance:
                new_point = (
                    x_q + self.distance * cos(alpha_q),
                    y_q + self.distance * sin(alpha_q)
                )

                self.points.append(new_point)

                if len(self.points) > 2:
                    x0, y0 = self.points[0]
                    x1, y1 = self.points[1]
                    x2, y2 = self.points[-1]
                    xmin = min(x0, x1, x2)
                    xmax = max(x0, x1, x2)
                    ymin = min(y0, y1, y2)
                    ymax = max(y0, y1, y2)
                    k_point, b_point = straight_line(x0, y0, x1, y1)
                    if isline(k_point, b_point, x2, y2):
                        for line in self.lines:
                              if isline(k_point, b_point, self.lines[line][0][0], self.lines[line][0][0]):
                                  if xmin not in range(self.lines[line][0][0], self.lines[line][1][0]):
                                      self.lines[line][0] = (xmin, self.lines[line][0][1])
                                  if xmax not in range(self.lines[line][0][0], self.lines[line][1][0]):
                                      self.lines[line][1] = (self.lines[line][0][1], xmax)
                                  if ymin not in range(self.lines[line][0][1], self.lines[line][1][1]):
                                      self.lines[line][0] = (ymin, self.lines[line][1][1])
                                  if ymax not in range(self.lines[line][0][1], self.lines[line][1][1]):
                                      self.lines[line][1] = (self.lines[line][1][1], xmax)
                                  self.points = []
                                  break
                        if self.points:
                            self.lines[f'line_{1+len(self.lines)}'] = [(x0, y0), (x2, y2), color1]
                            self.points = [] 

                    elif 0.098 * x0 <= x1 <= 1.02 * x0:
                        self.points_of_circles = [self.points[0], self.points[1], self.points[2]]
                        k1_2, b1_2 = k_point, b_point
                        k2_3, b2_3 = straight_line(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1])
                        point1_2 = median(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1])
                        point2_3 = median(self.points[0][0], self.points[0][1], self.points[-1][0], self.points[-1][1])
                        k1, b1 = normal(point1_2[0], point1_2[1], k1_2)
                        k2, b2 = normal(point2_3[0], point2_3[1], k2_3)
                        center = line_intersection(k1, b1, k2, b2)
                        if center:
                                len_ab = len_a_b(center[0], center[1], point1_2[0], point1_2[1])
                                for num in self.circles:
                                    if iscircle(self.circles[num][0][0], self.circles[num][0][1], self.circles[num][1], x1, x2):
                                        for xi, yi in self.points:
                                            self.circles[num][3].append((xi,yi))
                                        self.points_of_circles = sorted(self.circles[num][3])
                                        
                                        lenght = len(self.points_of_circle)
                                        point_1 = self.points_of_circle[0]
                                        point_2 = self.points_of_circle[lenght//2]
                                        point_3 = self.points_of_circle[lenght-1]
                                        k1_2, b1_2 = straight_line(point_1[0], point_1[1], point_2[0], point_2[1])
                                        k2_3, b2_3 = straight_line(point_3[0], point_3[1], point_2[0], point_2[1])
                                        point1_2 = median(point_1[0], point_1[1], point_2[0], point_2[1])
                                        point2_3 = median(point_3[0], point_3[1], point_2[0], point_2[1])
                                        k1, b1 = normal(point1_2[0], point1_2[1], k1_2)
                                        k2, b2 = normal(point2_3[0], point2_3[1], k2_3)
                                        center = line_intersection(k1, b1, k2, b2)
                                        self.circles[num][0] = center[0]
                                        self.circles[num][1] = center[1]
                                        len_ab = len_a_b(center[0], center[1], point1_2[0], point1_2[1])
                                        self.circles[num][2] = len_ab
                                        self.circles[num][3].append(self.points[0])
                                        self.circles[num][3].append(self.points[1])
                                        self.circles[num][3].append(self.points[2])
                                        self.points = []
                                        break
                                if self.points:
                                    if iscircle(center[0], center[1], len_ab, x0, y0) and iscircle(center[0], center[1], len_ab, x1, y1):
                                        self.circles[f'circl{1+len(self.circles)}'] = [(center[0], center[1]), len_ab,[self.points[0], self.points[1], self.points[2]] ,color2]
                                    self.points = []
                                #center = None
                    else:
                        self.points = []





                        

        else:
            self.distance = None

    def info(self) -> dict:

        # TODO!
        color1 = (255, 0, 0)
        color2 = (0, 120, 0)
        color3 = (255, 0, 150)
        line1 = [(100, 200,), (100, 300), color1]
        line2 = [(150, 250), (150, 350), color2]
        line3 = [(0, 0), (500, 500), color3]
        circle1 = ((100, 200), 20, color3)  # (point, radius)
        circle2 = ((200, 400), 30, color3)  # (point, radius)
        circle3 = ((400, 600), 40, color2)  # (point, radius)




        figures = {
            "lines": self.lines.values() ,  # не замкнутая
            "circles": self.circles.values(),
            "points": self.points
        }

        return {
            "params": (self.x, self.y, self.v, self.alpha),
            "maps": figures
        }

    def processing(self):
        if self.auto:
            self.processing_auto()

    def manual_update(self, x: float, y: float, alpha: float):
        if not self.auto:
            self.x += x
            self.y += y
            self.alpha += alpha

        self.locator.make_query(self.x, self.y, self.alpha)

    def processing_auto(self):

        if self.distance:
            self.v = 0
            self.alpha += radians(2.0)

        else:
            self.v = 5


        self.x += self.v * cos(self.alpha)
        self.y += self.v * sin(self.alpha)



        self.locator.make_query(self.x, self.y, self.alpha)