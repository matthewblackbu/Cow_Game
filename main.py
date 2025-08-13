import pygame
import random
import numpy as np
import math
import time
from pygame.constants import MOUSEBUTTONDOWN

file1 = open("how_many_times.txt",'r')
txt = int(file1.read())+1
file1.close()
file1 = open("how_many_times.txt",'w')
file1.write(str(txt))
file1.close()
print('------------------------Universal Test ' + str(txt) + '------------------------')

# initialize pygame
pygame.init()

# Create the screen
x_width = 1000
y_width = 1000
screen = pygame.display.set_mode((x_width, y_width))

# Title
pygame.display.set_caption("The Island")

# Icon 512x512
icon = pygame.image.load('assets/island.png')
pygame.display.set_icon(icon)

# WORLD SPEED (DONT TOUCH RETARD)
GLOBAL_TICK_MULT = 5
move_speed = .18 * GLOBAL_TICK_MULT
dev_mode = False

# Informational Variables
entity_size = 64

# Images 64x64
playerImg = pygame.image.load('assets/player.png')
pointerImg = pygame.image.load('assets/pointer.png')
cowImg = pygame.image.load('assets/cow.png')
coinImg = pygame.image.load('assets/coin.png')
grassImg1 = pygame.image.load('assets/grass1.png')
grassImg2 = pygame.image.load('assets/grass2.png')
grassImg3 = pygame.image.load('assets/grass3.png')
grassUImg = pygame.image.load('assets/grass_upgrade.png')
coinUImg = pygame.image.load('assets/coin_upgrade.png')
cowUImg = pygame.image.load('assets/cow_upgrade.png')
bigCoin = pygame.image.load('assets/big_coin.png')
shopIImg = pygame.image.load('assets/shop_icon.png')
stopImg = pygame.image.load('assets/stop.png')
goImg = pygame.image.load('assets/go.png')
shopImg = pygame.image.load('assets/shop.png')
playerUImg = pygame.image.load('assets/player_upgrade.png')

# Entity

class Entity():
    def __init__(self,x=0,y=0,type='Cow',show=False):
        self.x = x
        self.y = y
        self.type = type
        self.show = show
    def display(self):
        if self.type == 'Cow':
            screen.blit(cowImg,(self.x,self.y))
        elif self.type == 'Player':
            screen.blit(playerImg,(self.x,self.y))
            space = .18
            if self.direction != 0:
                rotated_image = pygame.transform.rotate(pointerImg, -45 * self.direction + 45)
                if self.x_change > 0:
                    x_temp = space
                elif self.x_change < 0:
                    x_temp = -space
                else:
                    x_temp = 0
                if self.y_change > 0:
                    y_temp = space
                elif self.y_change < 0:
                    y_temp = -space
                else:
                    y_temp = 0
                if self.direction == 2 or self.direction == 4:
                    x_temp -= .075
                if self.direction == 4 or self.direction == 6:
                    y_temp -= .05
                screen.blit(rotated_image,(self.x + (x_temp * 400-5),\
                                           self.y + (y_temp * 400)))
        elif self.type == 'Pointer':
            screen.blit(pointerImg,(self.x,self.y))
        elif self.type == 'Grass1':
            screen.blit(grassImg1,(self.x,self.y))
        elif self.type == 'Grass2':
            screen.blit(grassImg2,(self.x,self.y))
        elif self.type == 'Grass3':
            screen.blit(grassImg3,(self.x,self.y))
        elif self.type == 'Coin':
            screen.blit(coinImg,(self.x,self.y))
        elif self.type == 'Big_Coin':
            screen.blit(coinImg,(self.x,self.y))
        elif self.type == 'Coin_Upgrade':
            screen.blit(coin_upgrade_text,(self.x+20,self.y))
            screen.blit(coinUImg,(self.x,self.y))
        elif self.type == 'Cow_Upgrade':
            screen.blit(cow_upgrade_text,(self.x+20,self.y))
            screen.blit(cowUImg,(self.x,self.y))
        elif self.type == 'Grass_Upgrade':
            screen.blit(grassUImg,(self.x,self.y))
            screen.blit(grass_upgrade_text,(self.x+20,self.y))
        elif self.type == 'Player_Upgrade':
            screen.blit(playerUImg,(self.x,self.y))
            screen.blit(player_upgrade_text,(self.x+23,self.y+5))
        elif self.type == 'Shop_Icon':
            screen.blit(shopIImg,(self.x,self.y))
        elif self.type == 'Shop':
            screen.blit(shopImg,(self.x,self.y))
        elif self.type == 'Upgrade':
            global coins
            if coins >= self.cost:
                if self.hit_max():
                    screen.blit(stopImg,(self.x,self.y))
                    text = Font.render('Max',True,(0,0,0))
                    screen.blit(text,(self.x+10,self.y+19))
                    text = Font.render(self.text,True,(0,0,0))
                    screen.blit(text,(self.x-350,self.y+20))
                    return
                else:
                    screen.blit(goImg,(self.x,self.y))
            else:
                screen.blit(stopImg,(self.x,self.y))
            text = Font.render(self.text,True,(0,0,0))
            text2 = Font.render(str(math.floor(self.cost)),True,(0,0,0))
            screen.blit(text,(self.x-350,self.y+20))
            screen.blit(text2,(self.x+25,self.y+19))
            
    def move(self):
        pass
    def get_img(self):
        if self.type == 'Cow':
            return cowImg
        elif self.type == 'Player':
            return playerImg
        elif self.type == 'Grass1':
            return grassImg1
        elif self.type == 'Grass2':
            return grassImg1
        elif self.type == 'Grass3':
            return grassImg1
        elif self.type == 'Coin':
            return coinImg
        elif self.type == 'Shop_Icon':
            return shopIImg
        elif self.type == 'Shop':
            return shopImg
        elif self.type == 'Player_Upgrade':
            return playerUImg
        elif self.type == 'Coin_Upgrade':
            return coinUImg
        elif self.type == 'Cow_Upgrade':
            return cowUImg
        elif self.type == 'Grass_Upgrade':
            return grassUImg
        elif self.type == 'Upgrade':
            return goImg
        
    def get_pos(self):
        return (self.x,self.y)
    def show_on_screen(self):
        return self.show
    def revert_show(self):
        self.show = 1-self.show

# Player
class Player(Entity):
    def __init__(self,x = (x_width - 64) / 2,\
                      y = (y_width - 64) / 2):
        self.type = 'Player'
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 0
        self.direction = 0
    def move(self):
        shop_mod = player_speed.get_val()
        # Determine Direction
        if self.x_change > 0:
            if self.y_change > 0:
                self.direction = 4
            elif self.y_change < 0:
                self.direction = 2
            else:
                self.direction = 3
        elif self.x_change < 0:
            if self.y_change > 0:
                self.direction = 6
            elif self.y_change < 0:
                self.direction = 8
            else:
                self.direction = 7
        elif self.y_change > 0:
            self.direction = 5
        elif self.y_change < 0:
            self.direction = 1
        else:
            self.direction = 0
        # Test Boundaries to see if it can move
        x_temp = self.x_change*shop_mod
        y_temp = self.y_change*shop_mod
        if self.direction != 0:
            if self.direction % 2 == 0:
                x_temp = self.x_change * .707 * shop_mod
                y_temp = self.y_change * .707 * shop_mod
        if self.x + x_temp >= x_border:
            self.x = x_border
        elif self.x + x_temp <= 0:
            self.x = 0
        else:
            self.x += x_temp
        if self.y + y_temp >= y_border:
            self.y = y_border
        elif self.y + y_temp <= 0:
            self.y = 0
        else:
            self.y += y_temp

        # Collect Coins
        global Entities_coin
        global coins
        for i in Entities_coin:
            if touching(i,self):
                coins += i.get_value()
                Entities_coin.remove(i)
                global coin_text
                coin_text = Font.render(str(math.floor(coins)),True,(0,0,0))
    def calculate_player_movement(self,event):
        temp = move_speed*player_speed.get_val()
        temp = move_speed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.x_change -= temp
            if event.key == pygame.K_d:
                self.x_change += temp
            if event.key == pygame.K_w:
                self.y_change -= temp
            if event.key == pygame.K_s:
                self.y_change += temp
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.x_change += temp
            if event.key == pygame.K_d:
                self.x_change -= temp
            if event.key == pygame.K_w:
                self.y_change += temp
            if event.key == pygame.K_s:
                self.y_change -= temp
    def get_dir(self):
        return self.direction

# Cow
class Cow(Entity):
    def __init__(self,moving=False,):
        self.eating = False
        self.type = 'Cow'
        x_or_y = random.randint(0, 1)
        negitive_size_or_max = random.randint(0, 1)
        if x_or_y == 0:
            self.x = -entity_size * (1-negitive_size_or_max) + negitive_size_or_max * x_width
            self.y = random.randint(-entity_size,y_width)
        else:
            self.y = -entity_size * (1-negitive_size_or_max) + negitive_size_or_max * y_width
            self.x = random.randint(-entity_size,x_width)
        self.target_x = random.randint(0, x_border)
        self.target_y = random.randint(0, y_border)
        self.moving = moving
        self.cow_size = 64
        self.move_speed = .10 * GLOBAL_TICK_MULT
        self.ratio = .5
    def up_speed(self):
        self.move_speed = self.move_speed * 1.05
    def change_dir(self):
        self.target_x = random.randint(0, x_border-64)
        self.target_y = random.randint(0, y_border-64)
        x_dif = abs(self.target_x-self.x)
        y_dif = abs(self.target_y-self.y)
        self.ratio = x_dif/(y_dif+x_dif)
    def move(self):
        if random.randint(0,5000)==1:
            self.change_dir()
            self.moving = True
            self.eating = False
        global Entities_grass
        if not self.eating and not self.moving:
            # if random.randint(0, math.ceil(5000/GLOBAL_TICK_MULT)) <= 1:
            self.moving = True
            self.change_dir()
        elif self.moving:
            x_speed = self.move_speed*self.ratio*cow_speed.get_val()
            y_speed = self.move_speed*(1-self.ratio)*cow_speed.get_val()
            if abs(x_speed + self.x - self.target_x) <= x_speed:
                self.x = self.target_x
                x_speed = 0
            if abs(y_speed + self.y - self.target_y) <= y_speed:
                self.y = self.target_y
                y_speed = 0
            if x_speed == 0 and y_speed == 0:
                self.moving = False
            
            if self.target_x > self.x:
                self.x += x_speed
            else:
                self.x -= x_speed
            if self.target_y > self.y:
                self.y += y_speed
            else:
                self.y -= y_speed
                
            if not self.eating:
                closest = Cow()
                closest_dist = 150
                for i in Entities_grass:
                    tup = i.get_pos()
                    dist = np.hypot(self.x-tup[0],self.y-tup[1])
                    if dist <= closest_dist:
                        closest = i
                        closest_dist = dist

                if closest_dist <= 150 and not type(closest) == Cow and random.randint(0,100) == 1: 
                    self.target_x = closest.x-40
                    self.target_y = closest.y-30
                    x_dif = abs(self.target_x-self.x)
                    y_dif = abs(self.target_y-self.y)
                    if not (x_dif==0 and y_dif==0):
                        self.ratio = x_dif/(y_dif+x_dif)
                    self.eating = True
        elif self.eating and not self.moving:
            for i in Entities_grass:
                temp = i
                if touching(self,i):
                    break
            try:
                if touching(self,temp):
                    for i in Entities_grass:
                        if i == temp:
                            i.take_hit()
                else:
                    self.eating = False
            except:
                self.eating = False
        
    def __str__(self):
        return str(self.moving) + str(self.eating) + str(self.x) +" " +str(self.y)+" "+str(self.target_x) +" " +str(self.target_y)

# Grass
class Grass(Entity):
    def __init__(self,one=100,two=10,three=1):
        self.one = one
        self.two = two
        self.three = three
        self.rarity = self.set_rarity()
        self.x = random.randint(0,x_border)
        self.y = random.randint(0,y_border)
        self.health = 20
        self.being_eaten = False
        self.dead = False
        self.type = 'Grass' + str(self.rarity)
    def take_hit(self):
        if is_tenth:
            self.health -= 1
    def get_health(self):
        return self.health
    def set_rarity(self):
        num = random.randint(1,111)
        if num > self.one+self.two:
            array[2]+=1
            return 3
        elif num <= self.two:
            array[1]+=1
            return 2
        array[0]+=1
        return 1
    def get_rarity(self):
        return self.rarity
array = [0,0,0]
# Coin
class Coin(Entity):
    def __init__(self,x,y,val=1):
        self.val = val
        self.type = 'Coin'
        self.x = x
        self.y = y
        self.time = time.time()
    def is_viable(self,time):
        lifespan = 5 + coin_life_upgrade.get_val()
        if time - self.time > lifespan:
            return False
        return True
    def get_time(self):
        return self.time
    def get_value(self):
        return self.val

# Shop Upgrade
class Upgrade(Entity):
    def __init__(self,text="this is an upgrade",x=50,y=50,value=1,cost=1,cost_mod=2,cost_how='mult',max=1000000,val_how='add',val_mod = .1):
        self.text = text
        self.type = 'Upgrade'
        self.x = x
        self.y = y
        self.value = value
        self.cost = cost
        self.amount = 0
        self.val_how = val_how
        self.val_mod = val_mod
        self.cost_how = cost_how
        self.cost_mod = cost_mod
        self.max = max
    def buy(self):
        if not self.hit_max():
            global coins
            if coins >= self.cost:
                self.amount += 1
                coins -= self.cost
                if self.val_how == 'add':
                    self.value = round(self.value+self.val_mod,2)
                elif self.val_how == 'mult':
                    self.value = round(self.value*self.val_mod,2)
                if self.cost_how == 'add':
                    self.cost = round(self.cost+self.cost_mod,2)
                elif self.cost_how == 'mult':
                    self.cost = round(self.cost*self.cost_mod,2)
            global coin_text
            coin_text = Font.render(str(math.floor(coins)),True,(0,0,0))
    def get_val(self):
        return self.value
    def hit_max(self):
        return self.max <= self.amount

# Object collision
def touching(surface1,surface2):
    img1 = surface1.get_img()
    img2 = surface2.get_img()
    rect1 = img1.get_rect(topleft = (surface1.get_pos()))
    rect2 = img2.get_rect(topleft = (surface2.get_pos()))
    return(rect1.colliderect(rect2))

# Time detection
def second():
    global t_store
    if math.floor(time.time()) == t_store:
        return False
    t_store = math.floor(time.time())
    return True
def tenth():
    global tenth_store
    if round(time.time(),1) == tenth_store:
        return False
    tenth_store = round(time.time(),1)
    return True
# Border
x_border = x_width-entity_size
y_border = y_width-entity_size

# Starting Entities
Entities_grass = []
grass_max = 10
coin_chance = .2
Entities_cow = []
Entities_coin = []
Entities_player = []

for i in range(20):
    Entities_grass.append(Grass())
for i in range(2):
    Entities_cow.append(Cow())

Entities_player.append(Player())

# Shop code
shop_icon = Entity(x_width-80,y_width-80,'Shop_Icon')
shop_show = False

back_window = Entity(x_width/4,y_width/4,'Shop')
tab1 = pygame.Rect(254,252,90,33)
tab2 = pygame.Rect(348,252,90,33)
tab3 = pygame.Rect(442,252,83,33)
tab4 = pygame.Rect(527,252,82,33)
tab5 = pygame.Rect(613,252,78,33)
shop_list = [back_window,tab1,tab2,tab3,tab4,tab5,Entity(257,255,'Player_Upgrade'),Entity(355,260,'Coin_Upgrade'),Entity(450,260,'Cow_Upgrade'),Entity(535,260,'Grass_Upgrade')]


player_speed = Upgrade(text = "10% increased player speed",x=650,y=300,value=1,cost=5,val_how='add',val_mod=.2,cost_how='mult',cost_mod=2,max=10)
shop_tab_one = [player_speed]
coin_life_upgrade = Upgrade(text = "+1 second to coins",x=650,y=300,value=0,cost=5,val_how='add',val_mod=1,cost_how='mult',cost_mod=1.1,max=55)
shop_tab_two = [coin_life_upgrade]
cow_speed = Upgrade(text = "5% increased cow speed",x=650,y=300,value=1,cost=5,val_how='mult',val_mod=1.05,cost_how='mult',cost_mod=1.1,max=50)
cow_spawn = Upgrade(text = "Buy another cow",x=650,y=370,value=2,cost=100,val_how='add',val_mod=1,cost_how='mult',cost_mod=3.64,max=8)
shop_tab_three = [cow_spawn,cow_speed]
coin_upgrade = Upgrade(text = "grass upgrade",x=650,y=370,value=1,cost=20,val_how='add',val_mod=1,cost_how='mult',cost_mod=1.1,max=500)
grass_upgrade_speed = Upgrade(text = "20% increased grass spawn",x=650,y=300,value=0,cost=20,val_how='add',val_mod=1,cost_how='mult',cost_mod=1.1,max=500)
shop_tab_four = [grass_upgrade_speed,coin_upgrade]
shop_tab_five = []

# Coin
coins = 0
if dev_mode:
    coins = 100000000
Font = pygame.font.SysFont('Arial', 24)
Fonts = pygame.font.SysFont('Arial', 16)

# Game Loop
t_store = 0
tenth_store = 0
running = True
store_tab = 1

coin_text = Font.render(str(math.floor(coins)),True,(0,0,0))
player_price = Font.render(str(player_speed.cost),True,(0,0,0))
coin_upgrade_text = Fonts.render('Coins',True,(0,0,0))
player_upgrade_text = Fonts.render('Player',True,(0,0,0))
cow_upgrade_text = Fonts.render('Cow',True,(0,0,0))
grass_upgrade_text = Fonts.render('Grass',True,(0,0,0))
while running:
    clicked = []
    for event in pygame.event.get():
        # Quit first always
        if event.type == pygame.QUIT:
            running = False
        # Calculates the players net change over all keys
        for i in Entities_player:
            i.calculate_player_movement(event)
        
        if event.type == MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            if shop_show:
                for i in shop_list:
                    if type(i) == Entity:
                        if i.get_img().get_rect(topleft = (i.get_pos())).collidepoint(pos):
                            clicked.append(i)
                    else:
                        if i.collidepoint(pos):
                            clicked.append(i)
                if store_tab == 1:
                    for i in shop_tab_one:
                        if i.get_img().get_rect(topleft = (i.get_pos())).collidepoint(pos):
                            clicked.append(i)
                if store_tab == 2:
                    for i in shop_tab_two:
                        if i.get_img().get_rect(topleft = (i.get_pos())).collidepoint(pos):
                            clicked.append(i)
                if store_tab == 3:
                    for i in shop_tab_three:
                        if i.get_img().get_rect(topleft = (i.get_pos())).collidepoint(pos):
                            clicked.append(i)
                if store_tab == 4:
                    for i in shop_tab_four:
                        if i.get_img().get_rect(topleft = (i.get_pos())).collidepoint(pos):
                            clicked.append(i)
                if store_tab == 5:
                    for i in shop_tab_five:
                        if i.get_img().get_rect(topleft = (i.get_pos())).collidepoint(pos):
                            clicked.append(i)
                            
            else:
                if shop_icon.get_img().get_rect(topleft = (shop_icon.get_pos())).collidepoint(pos):
                    clicked.append(shop_icon)
            if back_window not in clicked:
                shop_show = False
            
            #print(clicked)
    # deal with clicked buttons

    for i in clicked:
        if i == shop_icon:
            shop_show = True
        elif i == tab1:
            store_tab = 1
        elif i == tab2:
            store_tab = 2
        elif i == tab3:
            store_tab = 3
        elif i == tab4:
            store_tab = 4
        elif i == tab5:
            store_tab = 5
        
# upgrades go here
        elif i == player_speed:
            player_speed.buy()
        elif i == cow_speed:
            cow_speed.buy()
        elif i == cow_spawn:
            cow_spawn.buy()
        elif i == grass_upgrade_speed:
            grass_upgrade_speed.buy()
        elif i == coin_life_upgrade:
            coin_life_upgrade.buy()
        elif i == coin_upgrade:
            coin_upgrade.buy()
        
        while cow_spawn.get_val() > len(Entities_cow):
            Entities_cow.append(Cow())
    # Bool once a second
    is_second = second()
    is_tenth = tenth()
    
    if is_second:
        # Grass Respawn
        if len(Entities_grass) < 200:
            for i in range(GLOBAL_TICK_MULT*(1+grass_upgrade_speed.get_val())):
                if random.randint(0,20) == 0:
                    Entities_grass.append(Grass())
        # Coin Timer
        for i in Entities_coin:
            if not i.is_viable(time.time()):
                Entities_coin.remove(i)

    # Background
    screen.fill((130, 230, 130))

    # Grass
    for i in Entities_grass:
        if i.get_health() <= 0:
            
            if i.get_rarity() == 1:
                Entities_coin.append(Coin(i.x,i.y,coin_upgrade.get_val()))
            elif i.get_rarity() == 2:
                Entities_coin.append(Coin(i.x,i.y,2*coin_upgrade.get_val()))
            else:
                Entities_coin.append(Coin(i.x,i.y,5*coin_upgrade.get_val()))
            Entities_grass.remove(i)
        i.move()
        i.display()

    # Cows
    for i in Entities_cow:
        i.move()
        i.display()

    # Coins
    for i in Entities_coin:
        i.move()
        i.display()

    # Players
    for i in Entities_player:
        i.move()
        i.display()

    # Coin picture and amount render
    if coins > 0:
        screen.blit(coin_text,(x_width-math.floor(np.log10(coins))*14-85,40))
    else:
        screen.blit(coin_text,(x_width-85,40))
    screen.blit(bigCoin,(x_width-62,30))
    screen.blit(coinImg,(x_width-50,45))
    screen.blit(coinUImg,(x_width-58,54))

    if shop_show:
        for i in shop_list:
            if type(i) == Entity:
                i.display()
        if store_tab == 1:
            for i in shop_tab_one:
                i.display()
        if store_tab == 2:
            for i in shop_tab_two:
                i.display()
        if store_tab == 3:
            for i in shop_tab_three:
                i.display()
        if store_tab == 4:
            for i in shop_tab_four:
                i.display()
        if store_tab == 5:
            for i in shop_tab_five:
                i.display()
    else:
        shop_icon.display()
    # Update screen
    pygame.display.update()
