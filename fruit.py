import math, pygame


LVL_TO_SIZE_MULTIPLIER = 50
GRAVITY_ACCELERATION = 200
DENCITY = 4000


class Vec3:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    
    def length(self):
        return math.sqrt(self.x^2 + self.y^2)
    
    
    def normalize(self):
        l = self.length()
        self.x = self.x / l
        self.y = self.y / l
        return self


    def distance(vec1, vec2):
        dx = vec1.x - vec2.x
        dy = vec1.y - vec2.y
        return math.sqrt(dx * dx + dy * dy)



class Fruit:
    def __init__(self, possition_x, possition_y, level=1, is_held=True):
        self.pos = Vec3(possition_x, possition_y)
        self.vel = Vec3(0, 0)
        self.level = level

        self.radius = self.level * LVL_TO_SIZE_MULTIPLIER
        self.mass = 4/3 * math.pi * math.pow(self.radius/1000, 3) * DENCITY
        
        self.is_held = is_held
        
        self.touching_left = False
        self.touching_right = False
        self.touching_floor = False
        
    
    def draw(self, screen):
        pygame.draw.circle(screen, (255,255,255), [int(self.pos.x), int(self.pos.y)], self.radius)
        
    
    def update_box_collision(self, screen_width, screen_height):
        self.touching_left = self.update_left_wall_collision(screen_width)
        self.touching_right = self.update_right_wall_collision(screen_width)
        self.touching_floor = self.update_floor_collision(screen_height)
        
        
    def update_left_wall_collision(self, screen_width):
        if self.pos.x < self.radius:
            self.pos.x = self.radius
            self.vel.x = 0
            return True
        return False
    
    
    def update_right_wall_collision(self, screen_width):
        if self.pos.x > screen_width - self.radius:
            self.pos.x = screen_width - self.radius
            self.vel.x = 0
            return True
        return False
    
    
    def update_floor_collision(self, screen_height):
        if self.pos.y > screen_height - self.radius:
            self.pos.y = screen_height - self.radius
            self.vel.y = 0
            return True
        return False

    
    def update_free_fall(self, frame_time):
        if not self.touching_floor:
            a_y = GRAVITY_ACCELERATION
            self.vel.y += a_y * frame_time
            self.pos.y += a_y * frame_time
    

    def update_fruit_fruit_collision(self, fruit):
        dist = Vec3.distance(self.pos, fruit.pos)
        dist_target = self.radius + fruit.radius
        if dist < dist_target:
            if self.level != fruit.level:
                angle = math.atan2((fruit.pos.y - self.pos.y), (fruit.pos.x - self.pos.x))
                d_dist = dist_target - dist
                dx = d_dist * math.cos(angle)
                dy = d_dist * math.sin(angle)
                
                
                if not (self.touching_left or self.touching_right or fruit.touching_left or fruit.touching_right):
                    self.pos.x -= dx/2
                    fruit.pos.x += dx/2
                
                elif (self.touching_left and not fruit.touching_right) or (self.touching_right and not fruit.touching_left):
                    fruit.pos.x += dx
                    
                elif (not self.touching_left and fruit.touching_right) or (not self.touching_right and fruit.touching_left):
                    self.pos.x -= dx
                    
                
                if self.touching_floor and not fruit.touching_floor:
                    fruit.pos.y += dy
                
                elif not self.touching_floor and fruit.touching_floor:
                    self.pos.y -= dy
                
                elif not self.touching_floor and not fruit.touching_floor:
                    self.pos.y -= dy / 2
                    fruit.pos.y += dy / 2
            
                return None
            
            else:
                new_pos = Vec3((self.pos.x + fruit.pos.x) / 2, (self.pos.y + fruit.pos.y) / 2)
                return Fruit(new_pos.x, new_pos.y, self.level + 1, False)