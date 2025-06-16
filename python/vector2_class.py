
import math
import random

class Vector2:
    #smple vector class
    def __init__(self,x=0,y=0):
        try:
            y = x[1]
            x = x[0]
        
        except:
            self.x = x
            self.y = y


    def update(self,xy_list):
        self.x = xy_list(0)
        self.y = xy_list(1)
        
    def rotate(self, angle):
        # Convert the angle to radians
        angle_rad = math.radians(angle)

        # Compute the new components
        new_x = self.x * math.cos(angle_rad) - self.y * math.sin(angle_rad)
        new_y = self.x * math.sin(angle_rad) + self.y * math.cos(angle_rad)

        # Update the vector components
        self.x = new_x
        self.y = new_y
    
    def norm(self):
        
        #normalizes the vector

        if self.x*self.y == 0:
            
            if self.x == 0:
                self.y = 1
            else:
                self.x = 1
                
        else:   
            h = math.sqrt(self.x**2 + self.y**2)
            self.x /= h
            self.y /= h
        return self
    
    
    def is_equal(self,other):
        if self.x == other.x and self.y  == other.y:
            return True
        else: return False
        
    
    def get_tup(self):
        return self.x,self.y
        
    def add(self,other):
        
        #performs a vector adition 
        
        self.x += other.x
        self.y += other.y
        return self

    
    def sub(self,other):
        
        #performs a vector subtraction  
        
        self.x -= other.x
        self.y -= other.y
        return self
        
    def scale(self,factor):
        
        #vector is multiplied by an integer or real scalar 
        
        self.x *= factor
        self.y *= factor
        return self
    
    def dist(self,other):
        
        #returns the distance between the vectors
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def mag(self):
        
        #returns the size of magnitude of a vector
        return math.sqrt(self.x**2 + self.y**2)
    
    def sine(self):
        
        #sine function
        try: return self.y/mag(self)
        except: return 0
        
    def dotprod(self,other):
        
        #dot product between this and another vector
        return((self.x*other.x)+(self.y*other.y))/(self.mag()*other.mag)
    
    def roundv(self,precission):
        
        #returns the vector with the specified degree of precision
        
        self.x = round(self.x,precission) 
        self.y = round(self.y,precission)
        
        return self
   
    def update(self,array):
        self.x = array[0]
        self.y = array[1]

def norm(vector):
    
     #normalizes the vector
    if vector.x*vector.y == 0:
        if vector.x == 0:
            vector.y = 1
        else:
            vector.y = 1
    else:   
        h = math.sqrt(vector.x**2 + vector.y**2)
        vector.x /= h
        vector.y /= h
    return vector


        
def add(v1,v2):
    #performs a vector adition using the splecified vectors
    return Vector2(v1.x + v2.x,v1.y + v2.y)
    
def sub(vec1,vec2):
    #performs a vector subtraction using the splecified vectors
    return Vector2(vec1.x - vec2.x ,vec1.y - vec2.y)
    
def scale(vector,factor):
    #vector is scaled by the factor
    return Vector2(vector.x * factor ,vector.y *factor)


def mag(vector):
    #returns the size or scale of the vector
    return (vector.x**2 + vector.y**2)**0.5

def dist(vec1,vec2):
    #returns the distance between 2 vector points
    return ((vec1.x - vec2.x)**2 + (vec1.y - vec2.y)**2)**0.5

def sin(vector):
    #returns the sine of the vector
    try: return vector.y/mag(vector)
    except: return 0

def cos(vector):
    #returns the cosine of the vector
    try: return vector.x/mag(vector)
    except: return 0
    
def rotate(vector, angle):
    
    # Convert the angle to radians
    angle_rad = math.radians(angle)

    # Compute the new components
    new_x = vector.x * math.cos(angle_rad) - vector.y * math.sin(angle_rad)
    new_y = vector.x * math.sin(angle_rad) + vector.y * math.cos(angle_rad)

    # Update the vector components
    vector.x = new_x
    vector.y = new_y
    
    return vector
        
        
def dotprod(vector1,vector2):
    #performs a dotproduct operation between the 2 vector
    return((vector1.x*vector2.x)+(vector1.y*vector2.y))

def roundv(vector,precission):
    
    #returns the vector with  with the specified degree of precision
    vector.x = round(vector.x,precission) 
    vector.y = round(vector.y,precission)
    return vector

def update_vector(vector,array):
    vector.x = array[0]
    vector.y = array[1]
    return vector

def copy_vector(vector):
    return Vector2(vector.x,vector.y)


def random_vector(x_start,x_end,y_start,y_end):
    return (Vector2(random.randint(x_start,x_end),random.randint(y_start,y_end)))
    