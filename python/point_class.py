#point_class:
from vector2_class import*


class Point:
    def __init__(self,pos =Vector2(0,0),speed = Vector2(0,0),acce = Vector2(0,0)):

        self.pos = pos
        self.oring = self.pos
        self.speed = speed
        self.acce = acce
    
    def linear_move(self):
        self.pos.add(self.speed)
    
    def colide(self,target,screen,pressure_constant,viscosity_constant):
        elastic = random.randint(1,9)/10
        self.life = 200
        width = screen.get_width()
        height = screen.get_height()
        
        self.acce.scale(0)
        if self.pos.get_tup() == target.pos.get_tup():
            self.pos.add(sub(self.speed,target.speed))
            
        else:
            d = dist(self.pos,target.pos)
            
            if d < self.radius+target.radius:
                corection = sub(self.pos,target.pos)
                corection.norm()
                
                self.pos.add(scale(corection,self.radius+target.radius-d))
                if d < self.radius+target.radius:
                    corection = sub(self.pos,target.pos)
                    corection.norm()
                    relative_velocity = sub(self.speed, target.speed)

                    # Calculate impulse along the collision normal
                    try:impulse = (relative_velocity.dotprod(corection)) / (
                        self.radius + target.radius
                    )
                    except: impulse = 0
                    # Update velocities
                    self.speed.sub(scale(corection, (impulse * target.radius)*elastic))
                    target.speed.add(scale(corection, (impulse * self.radius)*elastic))
                    #pygame.draw.circle(screen,self.randcolor,self.pos.get_tup(),self.radius)

                    
            if d < (self.radius+target.radius+1)*2:
                
                self.acce = sub(self.pos,target.pos)
                self.acce.norm()
                self.acce.scale(self.radius+target.radius/(d))
                self.acce.scale(pressure_constant)
                self.speed.add(scale(self.acce,1/self.radius))
                
        viscosity = scale(self.speed,viscosity_constant)
        self.speed.sub(viscosity)
        self.pos.add(self.speed)
        target.speed.sub(scale(self.acce,1/target.radius))
        bounce = random.randint(1,9)/10
    
   
    def pendulum_update(self,zero,g,rest,tc,fc,size):
            
            distance = dist(self.pos,zero) 
           
                    
            self.acce.scale(0)
            self.acce.sub(sub(self.pos,zero))
            self.acce.norm()

            if distance > rest:
                self.acce.scale(((distance-rest)/size)*tc)
            elif distance < rest:
                self.acce.scale(((-distance+rest)/size)*tc)
            
            self.acce.add(g)
            self.speed.add(self.acce)
            friction = scale(self.speed,-fc)
            self.speed.add(friction)
            
            self.pos.add(self.speed)
            
    def oring_update(self,g,rest,tc,pc,fc,size):
        self.pendulum_update(self.origin,g,rest,tc,pc,fc,size)
    
    
    def wall_bounce(self,size,fc):
        
        if self.pos.x + self.speed.x > size:
            self.pos.x = size-1
            self.speed.x *= -1+fc
        
        if self.pos.x + self.speed.x < 0:
            self.pos.x = 1
            self.speed.x *= -1+fc
        
        if self.pos.y + self.speed.y > size:
            self.pos.y = size-1
            self.speed.y *= -1+fc
        
        if self.pos.y + self.speed.y < 0:
            self.pos.y = 1
            self.speed.y *= -1+fc
