import pygame

class Texture:
    def __init__(self, background:pygame.Surface, x_texture:pygame.Surface, o_texture:pygame.Surface) -> None:
        self.x_texture = x_texture
        self.o_texture = o_texture
        self.background = background
        pass

class Rect:
    def __init__(self, x, y, width, height) -> None:
        self.x, self.y, self.width, self.height = x, y, width, height
        pass

    def get_values(self):
        return self.x, self.y, self.width, self.height
    
    def contains(self, dx, dy):
        return self.x < dx <= self.x + self.width and self.y < dy <= self.y + self.height
    
class NonagonTree:
    def __init__(self, id:list[int], rect:Rect, steps:int, texture:Texture) -> None:
        self.rect = rect
        self.steps = steps
        x, y, width, height = self.rect.get_values()
        self.grid:list[list["Space | NonagonTree"]] = [[] for _ in range(3)]
        for j in range(3):
            for i in range(3):
                lower_id = id.copy()
                lower_id.append(j*3+i)
                if steps == 0:
                    self.grid[j].append(Space(lower_id, Rect(x + i*width/3, y+j*height/3, width/3, height/3), 0, texture))
                else:
                    self.grid[j].append(NonagonTree(lower_id, Rect(x + i*width/3, y+j*height/3, width/3, height/3), steps - 1, texture))
        self.highlighted:bool = False
        self.value = 0 # The winner of the grid.

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
        
    def set_highlight_by_id(self, id:list[int]) -> bool:
        obj = self.access_by_id(id)
        if obj != None:
            if isinstance(obj, self.__class__):
                obj.highlighted = True
                return True
        return False
            
    def mark_space(self, id:list[int], winner:int) -> bool:
        space = self.access_by_id(id)
        if isinstance(space, Space) and (winner == 1 or winner == 2):
            space.value = winner
            return True
        elif isinstance(space, self.__class__):
            pass
        return False

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

    def _tictactoe_board(self, surface, weight = 1):
        x, y, w, h = self.rect.get_values()
        for i in range(1, 3, 1):
            line_v = ((x+(w*i)/3, y), (x+(w*i)/3, y+h))
            line_h = ((x, y+(h*i)/3), (x+w, y+(h*i)/3))
            for j in (line_v, line_h):
                pygame.draw.line(surface, "black", *j, width = weight)
        pass

    def _determine_winner(self):
        def _add(l1:list[int], l2:list[int])->list[int]:
            return [a + b for a, b in zip(l1, l2)]
        
        def _mult(l1:list[int], mag:int):
            return [a*mag for a in l1]
        
        def _access(id:list[int]):
            return self.grid[id[1]][id[0]]
        
        topleft, down, right, down_right, down_left = ([0, 0], [1, 0], [1, 0], [1, 1], [-1, 1])

        top = [_add(topleft, _mult(right, i)) for i in range(3)]
        mid = [_add(x, down) for x in top]
        bottom = [_add(x, down) for x in mid]
        horizontal = [top, mid, bottom]
        vertical = [[i[j] for i in (top, mid, bottom)] for j in range(3)]
        diag = [_add(topleft, _mult(down_right, i)) for i in range(3)]
        diag_inv = [_add(top[2], _mult(down_left, i)) for i in range(3)]

        awl:list[list[list[int]]] = []
        for i in (horizontal, vertical):
            awl += i
        awl.append(diag)
        awl.append(diag_inv)
        #awl is a list of all potential winning lines on the board

    def check_highlight(self, main_surface):
        # execute every frame
        #If self.highlighted: highlight else: unhighlight
        pass
    
    def draw(self, surface:pygame.Surface):
        # Draw tictactoe grid
        for j in range(len(self.grid)):
            for i in range(len(self.grid[j])):
                self.grid[j][i].draw(surface)
        # if self.winner = 0: no winner, 1: x wins, 2: o wins

class Space:
    def __init__(self, id:list[int], rect:Rect, fill:int, texture:Texture) -> None:
        assert fill == 0 or fill == 1 or fill == 2, f"fill: {fill} not a valid input"
        self.id = id
        self.value: int = fill
        self.changed = False
        self.rect = rect
        self.texture = texture

    def query(self, dx, dy):
        if self.rect.contains(dx, dy):
            return self
        else:
            return None
        
    def draw(self, surface:pygame.Surface):
        
        if self.changed:
            return
        
        def _scale_draw(surface:pygame.Surface, texture:pygame.Surface):
            t = texture.copy()
            pygame.transform.scale(t, (self.rect.width, self.rect.height))
            surface.blit(t, (self.rect.x, self.rect.y))
        
        if self.value == 0:
            pass
        elif self.value == 1:
            self.changed = True
            _scale_draw(surface, self.texture.x_texture)
        elif self.value == 2:
            self.changed = True
            _scale_draw(surface, self.texture.o_texture)

        # 0 = blank
        # 1 = x
        # 2 = o
        pass


