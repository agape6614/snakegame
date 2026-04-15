import pygame
import os
import sys
import random
from time import sleep

SCREEN_WIDTH=800
SCREEN_HEIGHT=600

#그리드
GRID_SIZE=20
GRID_WIDTH=SCREEN_WIDTH/GRID_SIZE
GRID_HEIGHT=SCREEN_HEIGHT/GRID_SIZE

#방향
UP=(0,-1)
DOWN=(0,1)
LEFT=(-1,0)
RIGHT=(1,0)

#색상
WHITE=(255,255,255)
ORANGE=(250,150,0)
GRAY=(100,100,100)

class Snake():
    def __init__(self):
        self.create()

    def create(self):
        self.length=2
        self.positions=[(int(SCREEN_WIDTH/2),int(SCREEN_HEIGHT/2))]
        self.direction=random.choice([UP,DOWN,LEFT,RIGHT])
        

    def control(self, xy):
        if (xy[0]*-1, xy[1]*-1)==self.direction:
            return
        else:
            self.direction=xy

    def move(self):
        cur=self.positions[0]
        x,y=self.direction
        new=(cur[0]+(x*GRID_SIZE)), (cur[1]+(y*GRID_SIZE))

        if new in self.positions[2:]:
            if(self.length > 2):
                 print(self.length)
            sleep(1)
            self.create()
        elif new[0] < 0 or new[0] >= SCREEN_WIDTH or \
                new[1] < 0 or new[1] >= SCREEN_HEIGHT:
            if(self.length > 2):
                print(self.length)
            sleep(1)
            self.create()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def eat(self):
        self.length += 1

    def draw(self, screen):
        red,green,blue = 50 / (self.length-1), 150, 150 / (self.length-1)
        for i,p in enumerate(self.positions):
            color=(100+red*i, green, blue*i)
            rect=pygame.Rect((p[0],p[1]),(GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen,color,rect)

class Feed():
    def __init__(self):
        self.position=(0,0)
        self.color=ORANGE
        self.create()

    def create(self):
        x = random.randint(0,GRID_WIDTH-1)
        y = random.randint(0,GRID_HEIGHT-1)
        self.position = x*GRID_SIZE, y*GRID_SIZE

    def draw(self, screen):
        rect=pygame.Rect((self.position[0], self.position[1]),\
                         (GRID_SIZE,GRID_SIZE))
        pygame.draw.rect(screen,self.color,rect)

class Game():
    def __init__(self):
        self.snake = Snake()
        self.feed = Feed()
        self.speed = 5
        self.frame_delay = 100

        # 이전 프레임에서의 키 입력
        self.prev_keys = pygame.key.get_pressed()

    def process_events(self):
        pygame.event.pump()  # 입력 이벤트 업데이트

        keys = pygame.key.get_pressed()  # 현재 프레임에서의 키 입력

        # 방향 전환 처리
        if keys[pygame.K_KP8] and not self.prev_keys[pygame.K_KP8]:
            self.snake.control(UP)
        elif keys[pygame.K_KP5] and not self.prev_keys[pygame.K_KP5]:
            self.snake.control(DOWN)
        elif keys[pygame.K_KP4] and not self.prev_keys[pygame.K_KP4]:
            self.snake.control(LEFT)
        elif keys[pygame.K_KP6] and not self.prev_keys[pygame.K_KP6]:
            self.snake.control(RIGHT)

        self.prev_keys = keys  # 이전 프레임의 키 입력 업데이트

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # 'q' 키를 눌렀을 때 게임을 초기화
                    self.snake.create()
                    self.feed.create()
                    self.frame_delay = 100
        return False


    def run_logic(self):
        self.snake.move()
        self.check_eat(self.snake, self.feed)
        if self.snake.positions[0][0] < 0 or self.snake.positions[0][0] >= SCREEN_WIDTH or \
        self.snake.positions[0][1] < 0 or self.snake.positions[0][1] >= SCREEN_HEIGHT:
            self.frame_delay = 100  # frame_delay를 100으로 재설정
        else:
            pygame.time.delay(self.frame_delay)

    def check_eat(self,snake,feed):
        if snake.positions[0] == feed.position:
            snake.eat()
            feed.create()
            self.frame_delay -= 5

    def draw_info(self,length,speed,screen):
        info="score: "+str(length)
        font=pygame.font.SysFont('함초롱바탕',35,False,False)
        text_obj=font.render(info,True,GRAY)
        text_rect=text_obj.get_rect()
        text_rect.x, text_rect.y = 340, 10
        screen.blit(text_obj,text_rect)


    def draw_info_t(self,length,speed,screen):
        info="speed initialization = 'q' "
        font=pygame.font.SysFont('함초롱바탕',35,False,False)
        text_obj=font.render(info,True,GRAY)
        text_rect=text_obj.get_rect()
        text_rect.x, text_rect.y = 10, 10
        screen.blit(text_obj,text_rect)

    def display_frame(self,screen):
        screen.fill(WHITE)
        self.draw_info(self.snake.length,self.speed,screen)
        self.draw_info_t(self.snake.length,self.speed,screen)
        self.snake.draw(screen)
        self.feed.draw(screen)
        screen.blit(screen,(0,0))

def main():
    pygame.init()
    pygame.display.set_caption('Snake Game')
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    done = False
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        pygame.display.flip()
        # pygame.time.delay(50)  # 프레임 간격을 50ms로 설정

    pygame.quit()

if __name__=='__main__':
    main()

# +" "+"speed: "+str(round(speed,2))print