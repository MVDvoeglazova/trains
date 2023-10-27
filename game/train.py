from math import cos, sin, radians
from random import uniform
from typing import Counter
from game.locator import Locator
from game.geometry import Line, Angle, Circle, what_is_it



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
        self.ROTATION = 30

        self.count = 0

        self.lastpoint = (x0, y0)
        self.points = list()

        self.line = []
        self.angle = []
        self.circle = []





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
                if 0 < self.count < 3*self.ROTATION - 1:
                    self.points.append(new_point)
                elif self.points:
                   name_class, out_class =  what_is_it(self.points, (self.x, self.y))
                  
            
                   if name_class == 'Line':
                        self.line.append((out_class.begin, out_class.end, color1))
                        self.line = sorted(self.line)
                        #line = Line(self.line[0][0], self.line[0][1])
                        #line.update()
                        #for num in range(1, len(self.line)):
                        #    if line.isline(self.line[num][1]):
                        #        line.update()
                        #        self.line[num] = (line.begin, line.end, color1)
                        #        self.line.pop(num)
                        #    else:
                        #        line = Line(self.line[num][0], self.line[num][1])
                        #        line.update()


                   elif name_class == 'Angle':
                       point_intersection = (out_class.x_intersection, out_class.y_intersection)
                       if point_intersection[0] and point_intersection[1]:
                           self.line.append((out_class.line1.begin, point_intersection, color2))
                           self.line.append((out_class.line2.begin, point_intersection, color2))
                           self.line.append((out_class.line1.begin, out_class.line1.end, color2))
                           self.line.append((out_class.line2.begin, out_class.line2.end, color2))
                   elif name_class == 'Circle':
                      
                       self.circle.append((out_class.xc, out_class.yc), out_class.radius, color3)
                   else:
                        pass


                            
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
            "lines": self.line ,  # не замкнутая
            "circles": self.circle,
            "points": [(0,0)]
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

    def move(self, angle = 0):
        self.alpha += radians(angle)

        self.x += self.v * cos(self.alpha)
        self.y += self.v * sin(self.alpha)

        self.locator.make_query(self.x, self.y, self.alpha)
        


    def processing_auto(self):
    
        if self.distance:

            if self.distance >= self.locator.range()//2:
                self.v = 2
                self.move()
            else:
                self.v = 0
                self.count += 1

        if self.count:
                if self.count < self.ROTATION:
                    self.move(1) 
                    self.count += 1

                elif self.count < 3* self.ROTATION:
                    self.move(-1) 
                    self.count += 1

                else:
                    self.count = 0
                    self.alpha += radians(150)
                    self.v = 2
                    self.move()

        else: 
                self.v = 2
                self.move()
        #elif self.count:

        #    if self.count < self.ROTATION:
        #        self.move(-1)
        #        self.count += self.ROTATION
        #    else:
        #        self.count = 0
                
        #        self.move(-1)

 
