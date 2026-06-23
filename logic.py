class Rect:
    def __init__(self, x, y, width, height) -> None:
        self.x, self.y, self.width, self.height = x, y, width, height
        pass

    def get_values(self):
        return self.x, self.y, self.width, self.height
    
    def contains(self, dx, dy):
        return self.x < dx <= self.x + self.width and self.y < dy <= self.y + self.height
    
class NonagonTree:
    def __init__(self, rect:Rect, steps:int = 0) -> None:
        self.rect = rect
        x, y, width, height = self.rect.get_values()
        if steps == 0:
            self.grid = [[Space(Rect(x + i*width/3, y+j*height/3, width/3, height/3)) for i in range(3)] for j in range(3)]
        else:
            self.grid = [[NonagonTree(Rect(x + i*width/3, y+j*height/3, width/3, height/3), steps - 1) for i in range(3)] for j in range(3)]

        self.winner = 0

    def query(self, dx, dy):
        if self.rect.contains(dx, dy):
            for j in range(len(self.grid)):
                for i in range(len(self.grid[j])):
                    grid_slot = self.grid[j][i].query(dx, dy)
                    if grid_slot != None:
                        return grid_slot
        else:
            return None

class Space:
    def __init__(self, rect:Rect, fill:int = 0) -> None:
        assert fill == 0 or fill == 1 or fill == 2, f"fill: {fill} not a valid input"
        self.value: int = fill
        self.rect = rect

    def query(self, dx, dy):
        if self.rect.contains(dx, dy):
            return self
        else:
            return None


