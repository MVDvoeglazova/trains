from math import cos, sin, radians
from pydoc import classname
from random import uniform
from tkinter import SEL
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
        self.v = 10
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
        self.line1_2 = None
        self.line2_3 = None
        self.line3_4 = None
        self.line1_4 = None
        self.len_path = 0
        self.path = []
        self.box = []
        self.go = False
        self.up_pulse = False
        self.down = True
        self.last_class = None

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
                    if new_point not in self.points:
                        self.points.append(new_point)
 
        
        else:
            self.distance = None


    def info(self) -> dict:


        figures = {
            "lines": self.lines ,  # не замкнутая
            "circles": self.circle,
            "points": self.points
        }

        return {
            "params": (self.x, self.y, self.v, self.alpha),
            "maps": figures
        }
    def make(self):
        #-------???--------line_1, line_2, line_3, line_4 = self.box[-4:0]
        line_1, line_2, line_3, line_4 = self.box

        lines = [(line_1.begin, line_1.end, color3), (line_2.begin, line_2.end, color3), (line_3.begin, line_3.end, color3), (line_4.begin, line_4.end, color3),]


        angle1_2 = Angle((self.x, self.y), line_1, line_2)
        angle2_3 = Angle((self.x, self.y), line_2, line_3)
        angle3_4 = Angle((self.x, self.y), line_3, line_4)
        angle1_4 = Angle((self.x, self.y), line_1, line_4)
        angle1_2.intersection_point()
        angle2_3.intersection_point()
        angle3_4.intersection_point()
        angle1_4.intersection_point()



        point_1 = (angle1_2.x_intersection, angle1_2.y_intersection)
        point_2 = (angle2_3.x_intersection, angle2_3.y_intersection)
        point_3 = (angle3_4.x_intersection, angle3_4.y_intersection)
        point_4 = (angle1_4.x_intersection, angle1_4.y_intersection)



        lines = [(point_1, point_2, color2), (point_2, point_3, color2), (point_3, point_4, color2), (point_4, point_1, color2)]
        self.lines += lines


        #-------???--------
        self.box = []

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
        if (0 <= self.count < self.ROTATION) or (3*self.ROTATION <= self.count < 4*self.ROTATION):
            
            self.move(-1)
            self.count += 1

        elif self.ROTATION <= self.count < 3*self.ROTATION:
            self.move(1)
            self.count += 1


        elif self.count >= 4*self.ROTATION:
            #----------------------
            #self.count = 0
            #self.alpha += radians(90)
            #self.v = 10
            #-----------------------
            it = 0
            while it < len(self.points):
                if self.new_point_is_border(self.points[it]):
                    self.points.pop(it)
                else:
                    it += 1


            class_name, out_class = what_is_it(self.points, (self.x, self.y))


            self.move()

            return class_name, out_class
        return None, None

        



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
            self.v = 10 
            self.count = 0
            self.move()
            return class_name, out_class
        return None, None


    def search_border(self):

        if len(self.list_of_directions) >= 2:
            point_1 = self.list_of_directions[-1]
            point_2 = self.list_of_directions[-2]
            line = Line(point_1, point_2)
            line.update()
            if line.lenght() < self.locator.range()*0.6:
                self.alpha = radians(90+45+self.delta)

                self.count += 1
                self.list_of_directions = []
            else:
                self.list_of_directions = []


        elif self.count:
   
            class_name, out_class = self.rotation()
            
            if class_name == 'Angle':
                  print(out_class.isborder())
                  self.vertices_of_border.append((out_class.x_intersection, out_class.y_intersection))
                  self.delta = 180
                  self.alpha = radians(270)
                  self.v = 10
             
            
        elif not self.distance or (self.distance and self.distance > self.locator.range()*0.6):
            self.v = 10
            self.move()
        else:
            self.count += 1
            self.move()

        if len(self.vertices_of_border) == 2:
            point_1 = self.vertices_of_border[0]
            point_3 = self.vertices_of_border[1] 
            point_2 = point_1[0], point_3[1]
            point_4 = point_3[0], point_1[1]
            self.line1_2 = Line(point_1, point_2)
            self.line2_3 = Line(point_2, point_3)
            self.line3_4 = Line(point_3, point_4)
            self.line1_4 = Line(point_1, point_4)
            self.line1_2.update()
            self.line2_3.update()
            self.line3_4.update()
            self.line1_4.update()

            lines = [(point_1, point_2, color1), (point_2, point_3, color1), (point_3, point_4, color1), (point_4, point_1, color1)]
            self.lines += lines
            self.border = True
            self.delta = radians(0)
            self.alpha = radians(90)
            self.points = []
            



    def snake(self):
        if (self.distance and self.distance  <= self.locator.range()*0.1 and  self.points and self.new_point_is_border(self.points[-1])) or self.len_path > self.locator.range()*0.3:
            self.points = []
            if self.alpha < radians(270+self.delta):
                self.delta = 0   
                
                        
            else:
                self.delta = -180
               

           
            self.alpha += radians(90+self.delta)
           
              

        if self.alpha == radians(0) or self.alpha == radians(180):
            self.path.append((self.x, self.y))
            self.len_path = (((self.path[0][0] - self.path[-1][0]) ** 2 + (self.path[0][1] - self.path[-1][1]) ** 2) ** 0.5)
        else:
            self.path = []
            self.len_path = 0
        if self.distance and self.distance <= self.locator.range()*0.1:
            self.v = 0
        else:
            self.v = 10

        if self.alpha == radians(0):
            self.alpha = radians(180)
            self.delta = 0
        self.move()


        

    def new_point_is_border(self, new_point):
        return max(self.line1_2.isline(new_point), self.line2_3.isline(new_point), self.line3_4.isline(new_point), self.line1_4.isline(new_point))
    
    def going(self):
        if self.len_path < self.locator.range()*0.5:
            self.path.append((self.x, self.y))
            self.len_path = (((self.path[0][0] - self.path[-1][0]) ** 2 + (self.path[0][1] - self.path[-1][1]) ** 2) ** 0.5)
            self.move()

        else:
      
            self.alpha += radians(90)

            self.v = 0
            self.len_path = 0
            self.path = []

            if self.distance and (self.points and not self.new_point_is_border(self.points[-1])):
            
                    self.alpha -= radians(90)
              
                    self.v = 5

            else:
                self.go = False
                self.count = 1
                #self.explore()
             
            self.move()

  
            #self.alpha -= radians(90)
            #self.alpha += radians(90)

            
      

        


    def search_shapes(self): 

        if self.count == 0 and (not self.points or (self.points and self.new_point_is_border(self.points[-1]))):
                self.snake()
                if self.distance:
                    if   self.alpha > radians(180):
                        self.down = True
                    

        elif self.go:

            self.going()
                
        else:
                if len(self.box) == 8:
                    #------------------------------------------------------
                    self.box = [self.box[0], self.box[2], self.box[4], self.box[7]]
                    #------------------------------------------------------
                    self.make()
                    
                    self.v = 0
                    
                self.v = 0
                class_name, out_class = self.explore()

                if class_name == 'Line':

                    if self.last_class and (not out_class.isline(self.last_class.begin) or not out_class.isline(self.last_class.end)):
                        self.up_pulse = not self.up_pulse
                        if not self.up_pulse:
                            self.down = not self.down

                        self.box.append(self.last_class)
                        self.box.append(out_class) 
                            


                   
                    self.count = 1
                    self.points = []
 
                    if self.down:
                        self.alpha = out_class.alpha() + radians(180)
                    else:
                         self.alpha = out_class.alpha()



                    
                    self.last_class = out_class

                

                    self.go = True
                    self.v = 5
                elif class_name == 'not points':
                 

                    self.go = True
                    self.v = 5

                elif class_name == 'Angle':

                    line1 = out_class.line1
                    line2 = out_class.line2
                    self.box.append(line1)
                    self.box.append(line2) 







   

    def processing_auto(self):
        
        if self.border:
            self.v = 5
            self.search_shapes()
        else:
            self.search_border()
        
 
 

