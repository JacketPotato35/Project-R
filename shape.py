from dataclasses import dataclass
@dataclass
class Shape:
    left: float
    right: float
    top: float
    bottom: float

    def collides_with(self, other: "Shape") -> bool:
        return (
            self.right > other.left
            and self.left < other.right
            and self.top < other.bottom
            and self.bottom > other.top
        )
    
    
    @staticmethod
    #left, right, otherleft, other right (can be changed for y axis)
    def collision_time(smin, smax, velocity, omin, omax):
        dist: float
        #if its going left or right (negative or positive velocity)
        if velocity > 0:
            dist = omin - smax 
        elif velocity < 0:
            dist = omax - smin
        else:
            return float("inf")
        #velocity=time/distance
        time = (dist / velocity)
        return time if time >= 0 else float("inf")