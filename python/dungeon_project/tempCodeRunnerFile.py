f.pos.get_tup(1))
        if self.pos.x > size+80:
            self.pos.x = -80
class Bullet:
    def __init__(self,pos,direction,speed=1,special = 0) -> None:
        self.pos = pos