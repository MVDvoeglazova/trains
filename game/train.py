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

        self.alpha = radians(90) #alpha0  # строительная ось от оси x против часовой стрелки
        self.x = x0
        self.y = y0
        self.v_max = 15
        self.locator = locator
        self.v = 5
        self.distance = None
        self.auto = True
        self.ROTATION = 30

        self.count = 0

  
        self.points = list()

        self.line = []
        self.circle = []
#----------------------------------------------------------
        self.border = False
        self.vertices_of_border = list()
        self.around = 0
        self.list_of_directions = []
        self.delta = 0
        self.lines = []
#----------------------------------------------------------



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
                
                if self.v == 0:
                    self.points.append(new_point)

        
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
            "lines": self.lines ,  # не замкнутая
            "circles": self.circle,
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

    def move(self, angle = 0):
        self.alpha += radians(angle)

        self.x += self.v * cos(self.alpha)
        self.y += self.v * sin(self.alpha)

        self.locator.make_query(self.x, self.y, self.alpha)
        

    def explore(self):
        pass
    def rotation_around(self):
        self.v = 0
        self.move(1)
        self.around += 1

    def rotation(self):

        if (0 < self.count <= self.ROTATION) or (3*self.ROTATION < self.count <= 4*self.ROTATION):
            self.v = 0
            self.move(-1)
            self.count += 1

        elif self.ROTATION < self.count <= 3*self.ROTATION:
            self.move(1)
            self.count += 1


        elif self.count >= 4*self.ROTATION:
     

            class_name, out_class = what_is_it(self.points, (self.x, self.y))
            self.points = []
            if class_name == 'Line':
                
               
                self.line = out_class
            elif class_name == 'Angle':
                self.v = 0
            

            if self.alpha < radians(100+self.delta):
                self.alpha = radians(180+self.delta)
                self.list_of_directions.append((self.x, self.y))
            else:
                self.alpha = radians(90+self.delta)
                self.list_of_directions.append((self.x, self.y))
            self.v = 5 
            self.count = 0
            self.move()
            return class_name, out_class
        return None, None


    def search_border(self):

        if len(self.list_of_directions) > 3:
            point_1 = self.list_of_directions[-1]
            point_2 = self.list_of_directions[-2]
            line = Line(point_1, point_2)
            line.update()
            if line.lenght() < self.locator.range()*0.6:
                self.alpha = radians(90+45+self.delta)

                self.count += 1
                self.list_of_directions = []


        elif self.count:
   
            class_name, out_class = self.rotation()
            
            if class_name == 'Angle':
                  print(out_class.isborder())
                  self.vertices_of_border.append((out_class.x_intersection, out_class.y_intersection))
                  self.delta = 180
                  self.alpha = radians(270)
                  self.v = 5
             
            
        elif not self.distance or (self.distance and self.distance > self.locator.range()*0.6):
            self.v = 5
            self.move()
        else:
            self.count += 1
            self.move()

        if len(self.vertices_of_border) == 2:
            point_1 = self.vertices_of_border[0]
            point_3 = self.vertices_of_border[1] 
            point_2 = point_1[0], point_3[1]
            point_4 = point_3[0], point_1[1]
            lines = [(point_1, point_2, color1), (point_2, point_3, color1), (point_3, point_4, color1), (point_4, point_1, color1)]
            self.lines += lines
            self.border = True
            
            


    def search_shapes(self): 
        pass

    def processing_auto(self):
        
        if self.border:
            self.search_shapes()
        else:
            self.search_border()
        
 
 
