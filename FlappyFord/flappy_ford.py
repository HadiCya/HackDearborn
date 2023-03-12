import pygame
import neat
import time
import os
import random
pygame.font.init()

WIDTH = 500
HEIGHT = 800

CAR_IMAGE = pygame.image.load(os.path.join("imgs", "fordraptor.png"))
building_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "building.png")))
BASE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BACKGROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
GROUND_LEVEL = 730

GAME_FONT = pygame.font.SysFont("roboto", 50)
generation = 0

class Car:
    IMG = CAR_IMAGE
    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    ANIMATION_TIME = 5

    def __init__(self,x, y) -> None:
        self.x = x
        self.y = y
        self.tilt = 0
        self.frame_cnt = 0
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, self.IMG.get_width(), self.IMG.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.height = self.y
        self.img = self.IMG

    def jump(self): 
        self.velocity = -10.5
        self.frame_cnt = 0
        self.height = self.y

    def move(self):
        self.frame_cnt += 1
        displacement = (self.velocity * self.frame_cnt) + (1.5*self.frame_cnt**2)
        if displacement >= 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY
    
    def draw(self, window, building):
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        pygame.draw.rect(window, self.color, (new_rect.x, new_rect.y, new_rect.width, new_rect.height), 2)
        window.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Building:
    GAP = 200
    VELOCITY = 5

    def __init__(self, x) -> None:
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.building_top = pygame.transform.flip(building_IMAGE, False, True)
        self.building_bottom = building_IMAGE
        self.rect = pygame.Rect(self.x, 0, building_IMAGE.get_width(), building_IMAGE.get_height())

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.building_top.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def draw(self, window):
        window.blit(self.building_top, (self.x, self.top))
        window.blit(self.building_bottom, (self.x, self.bottom))

    def collide(self, car):
        car_mask = car.get_mask()
        top_mask = pygame.mask.from_surface(self.building_top)
        bottom_mask = pygame.mask.from_surface(self.building_bottom)

        top_offset = (self.x-car.x, self.top-round(car.y))
        bottom_offset = (self.x-car.x, self.bottom-round(car.y))

        t_point = car_mask.overlap(top_mask, top_offset)
        b_point = car_mask.overlap(bottom_mask, bottom_offset)

        if t_point or b_point:
            return True
        return False

class Base:
    VELOCITY = 5
    Base_WIDTH = BASE_IMAGE.get_width()
    IMG = BASE_IMAGE

    def __init__(self, y) -> None:
        self.y = y
        self.x1 = 0
        self.x2 = self.Base_WIDTH

    def move(self):
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        if self.x1 + self.Base_WIDTH < 0:
            self.x1 = self.x2 + self.Base_WIDTH
        if self.x2 + self.Base_WIDTH < 0:
            self.x2 = self.x1 + self.Base_WIDTH

    def draw(self, window):
        window.blit(self.IMG, (self.x1, self.y)) 
        window.blit(self.IMG, (self.x2, self.y))



def draw_window(window, cars, buildings, base, score, gen):
    window.blit(BACKGROUND_IMAGE, (0, 0))
    for building in buildings:
        building.draw(window)
    
    text = GAME_FONT.render(str(score), 1, (255, 255, 255))
    window.blit(text, (WIDTH/2 + text.get_width(), 10))
 
    text = GAME_FONT.render(str(gen), 1, (255, 255, 255))
    window.blit(text, (10, 10))

    base.draw(window)
    for car in cars:
        car.draw(window, buildings[0])
    pygame.display.update()

def main():
    car = Car(230, 350)
    base = Base(GROUND_LEVEL)
    buildings = [Building(GROUND_LEVEL)]
    score = 0

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #car.move()
        new_building = False
        garbage = []
        for building in buildings:
            if building.collide(car):
                pass
                #run = False

            if building.x + building.building_top.get_width() < 0:
                garbage.append(building)
            if not building.passed and building.x < car.x:
                building.passed = True
                new_building = True
            building.move()
        
        if new_building:
            score += 1
            buildings.append(building(GROUND_LEVEL))

        for trash in garbage:
            buildings.remove(trash)

        if car.y + car.img.get_height() >= GROUND_LEVEL:
            pass
        
             
        base.move()
        draw_window(window, car, buildings, base, score)
    pygame.quit()
    quit()

def eval_genomes(genomes, config):
    
    nets = []
    ge = []
    cars = []
    global generation
    generation += 1
    for i, gene in genomes:
         net = neat.nn.FeedForwardNetwork.create(gene, config)
         nets.append(net)
         cars.append(Car(230, 350))
         gene.fitness = 0
         ge.append(gene)

    
    base = Base(GROUND_LEVEL)
    buildings = [Building(GROUND_LEVEL)]
    score = 0

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        index_building = 0
        if len(cars) > 0:
            if len(buildings) > 1 and cars[0].x > buildings[0].x + buildings[0].building_top.get_width():
                index_building = 1
        else:
            run = False
            break
        
        for x, car in enumerate(cars):
            car.move()
            ge[x].fitness += 0.10

            output = nets[x].activate((car.y, abs(car.y - buildings[index_building].height), abs(car.y - buildings[index_building].bottom)))

            if output[0] > 0.5:
                car.jump()

        new_building = False
        garbage = []
        for building in buildings:
            for x, car in enumerate(cars):
                if building.collide(car):
                    ge[x].fitness -= 1
                    cars.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                if not building.passed and building.x < car.x:
                    building.passed = True
                    new_building = True

            if building.x + building.building_top.get_width() < 0:
                garbage.append(building)
            building.move()
        
        if new_building:
            score += 1
            for gene in ge:
                gene.fitness += 5
            buildings.append(Building(GROUND_LEVEL-100))

        for trash in garbage:
            buildings.remove(trash)

        for x, car in enumerate(cars):
            if car.y + car.img.get_height() >= GROUND_LEVEL: #or car.y < 0: # ADD EXPLOIT HERE
                cars.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        
             
        base.move()
        draw_window(window, cars, buildings, base, score, generation)
    

                
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    best = population.run(eval_genomes, 50)

# if __name__ == "main":
#     print("hi")
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config-feedforward.txt")
    
run(config_path)

