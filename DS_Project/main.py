import pygame
from sys import exit
from random import*


class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def insert_at_front(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.length += 1

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.length += 1

    def get(self, index):
        if index < 0 or index >= self.length:
            return None
        current = self.head
        for i in range(index):
            current = current.next
        return current.data

    def delete_at_front(self):
        if self.head:
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.head = self.head.next
                self.head.prev = None
            self.length -= 1

    def delete_at_end(self):
        if self.tail:
            if self.head == self.tail:
                self.head = self.tail = None
            else:
                self.tail = self.tail.prev
                self.tail.next = None
            self.length -= 1

    def search(self, value):
        current = self.head
        while current:
            if current.data == value:
                return current
            current = current.next
        return None

    def size(self):
        return self.length

    def print_forward(self):
        current = self.head
        while current:
            print(current.data, end=" ")
            current = current.next

    def print_backward(self):
        current = self.tail
        while current:
            print(current.data, end=" ")
            current = current.prev

    def clear(self):
        self.head = self.tail = None
        self.length = 0

class Stack:
    def __init__(self):
        self._stack = DoublyLinkedList()

    def length(self):
        return self._stack.size()

    def clear(self):
        self._stack.clear()

    def push(self, value):
        self._stack.insert_at_end(value)

    def pop(self):
        if self._stack.size() == 0:
            return None
        else:
            value = self._stack.get(self._stack.size()-1)
            self._stack.delete_at_end()
            return value

class Queue:
    queue = DoublyLinkedList()

    def enqueue(self, value):
        self.queue.insert_at_front(value)

    def dequeue(self):
        if self.queue.length != 0:
            x = self.queue.get(self.queue.length-1)
            self.queue.delete_at_end()
            return x

    def size(self):
        return self.queue.length

    def clear(self):
        self.queue.clear()

class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class TreeDictionary:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        if not self.root:
            self.root = TreeNode(key, value)
        else:
            current = self.root
            while True:
                if key < current.key:
                    if current.left is None:
                        current.left = TreeNode(key, value)
                        break
                    else:
                        current = current.left
                elif key > current.key:
                    if current.right is None:
                        current.right = TreeNode(key, value)
                        break
                    else:
                        current = current.right
                else:  # If the key already exists, update the value
                    current.value = value
                    break

    def search(self, key):
        current = self.root
        while current is not None and current.key != key:
            if key < current.key:
                current = current.left
            else:
                current = current.right

        if not current:  # Key not found in the tree
            return None

        return current.value

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 5
        self.counter = 0  # To control unwanted inputs
        self.counter_start = False
        self.heart = pygame.image.load("files/graphics/player/heart.png").convert_alpha()
        self.heart = pygame.transform.scale(self.heart, (25, 25))
        self.player_off = pygame.image.load("files/graphics/player/playeroff.png").convert_alpha()
        self.player_off = pygame.transform.scale(self.player_off, (96, 102))
        self.player_on = pygame.image.load("files/graphics/player/playeron.png").convert_alpha()
        self.player_on = pygame.transform.scale(self.player_on, (96, 102))
        self.player_images = [self.player_off, self.player_on]
        self.player_index = 0
        self.image = self.player_images[self.player_index].convert_alpha()
        self.rect = self.image.get_rect(midbottom=(width/2, 0.95*height))
        self.machinegun = pygame.image.load("files/graphics/player/machinegun.png").convert_alpha()
        self.shotgun = pygame.image.load("files/graphics/player/shotgun.png").convert_alpha()
        self.laser = pygame.image.load("files/graphics/player/laser.png").convert_alpha()
        self.guns = Queue()
        self.guns.enqueue({"name": "shotgun", "ammo": 8, "image": self.shotgun})
        self.guns.enqueue({"name": "laser", "ammo": 5, "image": self.laser})
        self.current_gun = {"name": "machinegun", "ammo": 30, "image": self.machinegun}

    def player_input(self):
        # Moving
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.right += 8
            if self.rect.right > width:
                self.rect.right = width
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.left -= 8
            if self.rect.left < 0:
                self.rect.left = 0
        # Change Ammo & Shoot
        if self.counter == 0:
            if keys[pygame.K_c]:
                self.guns.enqueue(self.current_gun)
                self.current_gun = self.guns.dequeue()
                self.counter_start = True
            if keys[pygame.K_SPACE]:
                self.shoot()
                self.counter_start = True
        if self.counter_start:
            self.counter += 1
            if self.counter >= 10:
                self.counter = 0
                self.counter_start = False

    def shoot(self):
        if self.current_gun["ammo"] > 0:
            self.current_gun["ammo"] = self.current_gun["ammo"] - 1
            info = {"health": self.health, "gun": self.current_gun.copy(), "player_rect": self.rect.__copy__()}
            if info["gun"]["name"] == "shotgun":
                info["player_rect"].left -= 40
                for j in range(-2, 3):
                    info = info.copy()  # To avoid passing by reference
                    info["orientation"] = j
                    bullets.add(Bullet(info))
                    info["player_rect"].left += 20
            else:
                bullets.add(Bullet(info))
        else:
            print("Out of Ammo!")

    def animation_state(self):
        self.player_index += 0.3
        if self.player_index >= len(self.player_images):
            self.player_index = 0
        self.image = self.player_images[int(self.player_index)]

    def hud(self):
        gun = pygame.transform.scale(self.current_gun["image"], (25, 50))
        font = pygame.font.Font("files/font/Pixeltype.ttf", 50)
        ammonum = font.render(str(self.current_gun["ammo"]), False, "White")
        screen.blit(gun, (width*0.96, height*0.88))
        screen.blit(ammonum, (width*0.92, height*0.91))
        for j in range(self.health):
            screen.blit(self.heart, (width*0.9+j*20, height*0.95))

    def reload(self):
        self.guns.clear()
        self.guns.enqueue({"name": "shotgun", "ammo": 8, "image": self.shotgun})
        self.guns.enqueue({"name": "laser", "ammo": 5, "image": self.laser})
        self.current_gun = {"name": "machinegun", "ammo": 30, "image": self.machinegun}
        self.health = 5
        self.counter = 0
        self.counter_start = False

    def update(self):
        self.player_input()
        self.animation_state()
        self.hud()
        if pygame.sprite.spritecollide(self, asteroids, False):
            self.health -= 1
        if self.health == 0:
            global current_state
            current_state = "lose"

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_info):
        super().__init__()
        self.player_info = player_info
        self.image = player_info["gun"]["image"]
        self.image = pygame.transform.scale(self.image, (20, 50))
        self.rect = self.image.get_rect(midbottom=self.player_info["player_rect"].midtop)
        if self.player_info["gun"]["name"] == "laser":
            self.damage = 5
        else:
            self.damage = 1

    def movement_n_collision(self):
        if pygame.sprite.spritecollide(self, asteroids, False):
            self.damage -= 1
        if self.rect.bottom < -5 or self.damage == 0:
            self.kill()
        if self.player_info["gun"]["name"] == "laser":
            self.rect.bottom -= 15
        else:
            self.rect.bottom -= 10
        if self.player_info["gun"]["name"] == "shotgun":
            self.rect.left += self.player_info["orientation"]

    def update(self):
        self.movement_n_collision()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, orient):
        super().__init__()
        if current_state == "level1":
            self.image = pygame.image.load("files/graphics/asteroids/asteroid1.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (65, 65))
            self.rect = self.image.get_rect(midbottom=pos)
            self.speed = 10
            self.hp = 1
        elif current_state == "level2":
            if orient == 0:
                self.image = pygame.image.load("files/graphics/asteroids/asteroid21.png")
                self.image = pygame.transform.scale(self.image, (65, 65))
                self.rect = self.image.get_rect(midbottom=pos)
                self.hp = 2
            else:
                self.image = pygame.image.load("files/graphics/asteroids/asteroid22.png")
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.rect = self.image.get_rect(midbottom=pos)
                self.hp = 1
            self.speed = 8
        self.orientation = orient

    def update(self):
        if self.rect.top > height+1:
            self.kill()
        if self.hp == 0:
            if current_state == "level2" and self.orientation == 0:
                asteroids.add(Asteroid(self.rect.midbottom, -2))
                asteroids.add(Asteroid(self.rect.midbottom, 2))
            self.kill()
        self.rect.bottom += self.speed
        self.rect.left += self.orientation
        if pygame.sprite.spritecollide(self, bullets, False) or pygame.sprite.spritecollide(self, player, False):
            self.hp -= 1


def load_game_states():
    states = Stack()
    states.push("level3")
    states.push("level2")
    states.push("level1")
    return states

def load_menu():
    menu_backrground = pygame.image.load("files/graphics/backgrounds/menu.png").convert_alpha()
    menu_backrground = pygame.transform.scale(menu_backrground, (width, height))
    story_background = pygame.image.load("files/graphics/backgrounds/story.jpg").convert_alpha()
    story_background = pygame.transform.scale(story_background, (width, height))
    lose_background = pygame.image.load("files/graphics/backgrounds/losebackground.jpg").convert_alpha()
    lose_background = pygame.transform.scale(lose_background, (width, height))
    text_font = pygame.font.Font("files/font/Pixeltype.ttf", 50)
    menu_start_txt = text_font.render("START", False, "White").convert()
    menu_start_txt_rect = menu_start_txt.get_rect(topleft=(width-180, height-120))
    menu_story_txt = text_font.render("STORY", False, "White").convert()
    menu_story_txt_rect = menu_story_txt.get_rect(topleft=(width-180, height-80))
    menu_exit_txt = text_font.render("EXIT", False, "White").convert()
    menu_exit_txt_rect = menu_exit_txt.get_rect(topleft=(width-180, height-40))
    text_font2 = pygame.font.Font("files/font/Pixeltype.ttf", 30)
    story_text = []
    with open("files/text/Text.txt") as File:
        for _line in File.readlines():
            story_text.append(_line[0:-1])
    back_txt = text_font.render("BACK", False, "White").convert()
    back_txt_rect = back_txt.get_rect(topleft=(50, 650))
    quit_txt = text_font.render("QUIT", False,"White").convert()
    quit_txt_rect = quit_txt.get_rect(topright=(1230, 650))
    menu_dict = TreeDictionary()
    menu_dict.insert("menu_background", menu_backrground)
    menu_dict.insert("story_background", story_background)
    menu_dict.insert("lose_background", lose_background)
    menu_dict.insert("text_font", text_font)
    menu_dict.insert("text_font2", text_font2)
    menu_dict.insert("menu_start_txt", menu_start_txt)
    menu_dict.insert("menu_start_txt_rect", menu_start_txt_rect)
    menu_dict.insert("menu_story_txt", menu_story_txt)
    menu_dict.insert("menu_story_txt_rect", menu_story_txt_rect)
    menu_dict.insert("menu_exit_txt", menu_exit_txt)
    menu_dict.insert("menu_exit_txt_rect", menu_exit_txt_rect)
    menu_dict.insert("story_text", story_text)
    menu_dict.insert("back_txt", back_txt)
    menu_dict.insert("back_txt_rect", back_txt_rect)
    menu_dict.insert("quit_txt", quit_txt)
    menu_dict.insert("quit_txt_rect", quit_txt_rect)
    return menu_dict

def load_levels():
    lvl_background = pygame.image.load("files/graphics/backgrounds/levelbackground.jpg").convert_alpha()
    lvl_background = pygame.transform.scale(lvl_background, (width, height))
    level_dict = TreeDictionary()
    level_dict.insert("lvl_background", lvl_background)
    return level_dict

def reset(reason):
    global level_timer, game_states, current_state
    level_timer = 0
    bullets.empty()
    asteroids.empty()
    print(Player.current_gun)
    Player.reload()
    if reason == "losing":
        game_states = load_game_states()
        current_state = "menu"
    elif reason == "level won":
        current_state = game_states.pop()

def draw_level():
    screen.blit(lvl_dict.search("lvl_background"), (0, 0))
    player.draw(screen)
    player.update()
    bullets.draw(screen)
    bullets.update()
    asteroids.draw(screen)
    asteroids.update()
    if level_timer == 60:
        reset("level won")


# Program Start
pygame.init()

# Screen Setup
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Saving the Stranded")
clock = pygame.time.Clock()

# Game Setup
menu_Dict = load_menu()
lvl_dict = load_levels()
game_states = load_game_states()
current_state = "menu"

# Loading Sprite Groups
player = pygame.sprite.GroupSingle()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
Player = Player()
player.add(Player)

# Timer Objects
asteroid_timer = pygame.USEREVENT + 1
pygame.time.set_timer(asteroid_timer, 1000)
level_timer = 0


while True:
    for event in pygame.event.get():
        # Checking for Quit input from the player
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Spawning Level 1 Asteroids
        if event.type == asteroid_timer and current_state[0:5] == "level":
            level_timer += 1
            spawn_number = choice([5, 6, 7, 8])
            for i in range(spawn_number):
                x_pos = randint(0, width-50)
                y_pos = randint(-200,0)
                asteroids.add(Asteroid((x_pos, y_pos), 0))

    if current_state == "menu":
        screen.blit(menu_Dict.search("menu_background"), (0, 0))
        screen.blit(menu_Dict.search("menu_start_txt"), menu_Dict.search("menu_start_txt_rect"))
        screen.blit(menu_Dict.search("menu_story_txt"), menu_Dict.search("menu_story_txt_rect"))
        screen.blit(menu_Dict.search("menu_exit_txt"), menu_Dict.search("menu_exit_txt_rect"))

        if pygame.mouse.get_pressed() == (1, 0, 0):
            if menu_Dict.search("menu_exit_txt_rect").collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                pygame.quit()
                exit()
            if menu_Dict.search("menu_start_txt_rect").collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                current_state = game_states.pop()
            if menu_Dict.search("menu_story_txt_rect").collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                current_state = "story"

    if current_state == "story":
        screen.blit(menu_Dict.search("story_background"), (0, 0))

        for line in range(len(menu_Dict.search("story_text"))):
            story_text_surface = menu_Dict.search("text_font2").render(menu_Dict.search("story_text")[line],
                                                                       True, "#FFFFFF", "#929292")
            screen.blit(story_text_surface, (50, line*30+30))

        screen.blit(menu_Dict.search("back_txt"), menu_Dict.search("back_txt_rect"))
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if menu_Dict.search("back_txt_rect").collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                print("click")
                current_state = "menu"

    if current_state == "level1":
        draw_level()
        # Asteroids being generated in the event for loop at the same time

    if current_state == "level2":
        draw_level()
        # Asteroids being generated in the event for loop at the same time

    if current_state == "lose":
        screen.blit(menu_Dict.search("lose_background"), (0, 0))
        screen.blit(menu_Dict.search("back_txt"), menu_Dict.search("back_txt_rect"))
        screen.blit(menu_Dict.search("quit_txt"), menu_Dict.search("quit_txt_rect"))
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if menu_Dict.search("back_txt_rect").collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                reset("losing")
            if menu_Dict.search("quit_txt_rect").collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                pygame.quit()
                exit()

    pygame.display.update()
    clock.tick(60)
