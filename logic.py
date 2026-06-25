class Rect:
    def __init__(self, x, y, width, height) -> None:
        self.x, self.y, self.width, self.height = x, y, width, height
        pass

    def get_values(self):
        return self.x, self.y, self.width, self.height
    
    def contains(self, dx, dy):
        return self.x < dx <= self.x + self.width and self.y < dy <= self.y + self.height
    
class NonagonTree:
    def __init__(self, id:list[int], rect:Rect, steps:int = 0) -> None:
        self.rect = rect
        self.steps = steps
        x, y, width, height = self.rect.get_values()
        self.grid:list[list["Space | NonagonTree"]] = [[] for _ in range(3)]
        for j in range(3):
            for i in range(3):
                lower_id = id.copy()
                lower_id.append(j*3+i)
                if steps == 0:
                    self.grid[j].append(Space(lower_id, Rect(x + i*width/3, y+j*height/3, width/3, height/3), 0))
                else:
                    self.grid[j].append(NonagonTree(lower_id, Rect(x + i*width/3, y+j*height/3, width/3, height/3), steps - 1))

        self.winner = 0

    def access_by_id(self, id:list[int]):
        if len(id) == 0:
            return None
        assert len(id) <= self.steps + 1
        id_copy = id.copy()
        token = id_copy.pop(0)
        j = token // 3
        i = token % 3
        g = self.grid[j][i]
        if len(id_copy) == 0 or isinstance(g, Space):
            return g
        elif isinstance(g, self.__class__):
            return g.access_by_id(id_copy)
        

    def query(self, dx, dy):
        if self.rect.contains(dx, dy):
            for j in range(len(self.grid)):
                for i in range(len(self.grid[j])):
                    grid_slot = self.grid[j][i].query(dx, dy)
                    if grid_slot != None:
                        return grid_slot
        else:
            return None
        
    def to_list(self):
        temp_list = []
        for j in range(len(self.grid)):
            for i in range(len(self.grid[j])):
                grid_slot = self.grid[j][i]
                if isinstance(grid_slot, Space):
                    temp_list.append(grid_slot)
                else:
                    temp_list += grid_slot.to_list()
        return temp_list
    
    def draw(self):
        # Draw tictactoe grid
        for j in range(len(self.grid)):
            for i in range(len(self.grid[j])):
                self.grid[j][i].draw()
        # if self.winner = 0: no winner, 1: x wins, 2: o wins

class Space:
    def __init__(self, id:list[int], rect:Rect, fill:int = 0) -> None:
        assert fill == 0 or fill == 1 or fill == 2, f"fill: {fill} not a valid input"
        self.value: int = fill
        self.rect = rect

    def query(self, dx, dy):
        if self.rect.contains(dx, dy):
            return self
        else:
            return None
        
    def draw(self):
        # 0 = blank
        # 1 = x
        # 2 = o
        pass


