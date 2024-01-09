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
        self.player_off = pygame.image.load("files/graphics/player/playeroff.png").convert_alpha()
        self.player_off = pygame.transform.scale(self.player_off,(96,102))
        self.player_on = pygame.image.load("files/graphics/player/playeron.png").convert_alpha()
        self.player_on = pygame.transform.scale(self.player_on,(96,102))
        self.player_images = [self.player_off, self.player_on]
        self.player_index = 0
        self.image = self.player_images[self.player_index].convert_alpha()
        self.rect = self.image.get_rect(midbottom=(width/2,0.95*height))

        self.bullet = pygame.image.load("files/graphics/player/bullet.png").convert_alpha()
        self.shotgun = pygame.image.load("files/graphics/player/shotgun.png").convert_alpha()
        self.laser = pygame.image.load("files/graphics/player/laser.png").convert_alpha()

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.rect.right < width:
            self.rect.right += 8
            if self.rect.right > width:
                self.rect.right = width
            print("m_right")
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.left -= 8
            if self.rect.left < 0:
                self.rect.left = 0
            print("m_left")

    def animation_state(self):
        self.player_index += 0.3
        if self.player_index >= len(self.player_images):
            self.player_index = 0
        self.image = self.player_images[int(self.player_index)]

    def update(self):
        self.animation_state()
        self.player_input()

def load_game_states():
    states = Stack()
    states.push("level4")
    states.push("level3")
    states.push("level2")
    states.push("level1")
    return states

def load_menu():
    menu_backrground = pygame.image.load("files/graphics/backgrounds/menu.jpg").convert_alpha()
    menu_backrground = pygame.transform.scale(menu_backrground, (width, height))
    story_background = pygame.image.load("files/graphics/backgrounds/story.jpg").convert_alpha()
    story_background = pygame.transform.scale(story_background, (width,height))
    text_font = pygame.font.Font("files/font/Pixeltype.ttf",50)
    menu_start_txt = text_font.render("START",False,"White").convert()
    menu_start_txt_rect = menu_start_txt.get_rect(topleft=(width-180,height-120))
    menu_story_txt = text_font.render("STORY",False,"White").convert()
    menu_story_txt_rect = menu_story_txt.get_rect(topleft=(width-180,height-80))
    menu_exit_txt = text_font.render("EXIT",False,"White").convert()
    menu_exit_txt_rect = menu_exit_txt.get_rect(topleft=(width-180,height-40))
    text_font2 = pygame.font.Font("files/font/Pixeltype.ttf",30)
    story_text = []
    with open("files/text/Text.txt") as File:
        for _line in File.readlines():
            story_text.append(_line[0:-2])
    story_back_txt = text_font.render("BACK",False,"White").convert()
    story_back_txt_rect = story_back_txt.get_rect(topleft=(50,650))
    menu_dict = TreeDictionary()
    menu_dict.insert("menu_background",menu_backrground)
    menu_dict.insert("story_background",story_background)
    menu_dict.insert("text_font",text_font)
    menu_dict.insert("text_font2",text_font2)
    menu_dict.insert("menu_start_txt",menu_start_txt)
    menu_dict.insert("menu_start_txt_rect",menu_start_txt_rect)
    menu_dict.insert("menu_story_txt",menu_story_txt)
    menu_dict.insert("menu_story_txt_rect",menu_story_txt_rect)
    menu_dict.insert("menu_exit_txt",menu_exit_txt)
    menu_dict.insert("menu_exit_txt_rect",menu_exit_txt_rect)
    menu_dict.insert("story_text",story_text)
    menu_dict.insert("story_back_txt",story_back_txt)
    menu_dict.insert("story_back_txt_rect",story_back_txt_rect)
    return menu_dict

def load_levels():
    lvl_background = pygame.image.load("files/graphics/backgrounds/levelBackground.jpg").convert_alpha()
    lvl_background = pygame.transform.scale(lvl_background,(width,height))

    level_dict = TreeDictionary()
    level_dict.insert("lvl_background",lvl_background)

    return level_dict


# Program Start
pygame.init()

# Screen Setup
width = 1280
height = 720
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Saving the Stranded")
clock = pygame.time.Clock()

# Game Setup
menu_Dict = load_menu()
lvl_dict = load_levels()
game_states = load_game_states()
current_state = "menu"


# Loading Sprite Groups
player = pygame.sprite.GroupSingle()
player.add(Player())


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if current_state == "menu":

        screen.blit(menu_Dict.search("menu_background"),(0,0))
        screen.blit(menu_Dict.search("menu_start_txt"),menu_Dict.search("menu_start_txt_rect"))
        screen.blit(menu_Dict.search("menu_story_txt"),menu_Dict.search("menu_story_txt_rect"))
        screen.blit(menu_Dict.search("menu_exit_txt"),menu_Dict.search("menu_exit_txt_rect"))

        if pygame.mouse.get_pressed() == (1, 0, 0):
            if menu_Dict.search("menu_exit_txt_rect").collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                pygame.quit()
                exit()
            if menu_Dict.search("menu_start_txt_rect").collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                current_state = game_states.pop()
            if menu_Dict.search("menu_story_txt_rect").collidepoint(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                current_state = "story"

    if current_state == "story":

        screen.blit(menu_Dict.search("story_background"),(0,0))

        for line in range(len(menu_Dict.search("story_text"))):
            story_text_surface = menu_Dict.search("text_font2").render(menu_Dict.search("story_text")[line],True,"#FFFFFF","#929292")
            screen.blit(story_text_surface,(50,line*30+30))

        screen.blit(menu_Dict.search("story_back_txt"),menu_Dict.search("story_back_txt_rect"))

        if pygame.mouse.get_pressed() == (1, 0, 0):
            if menu_Dict.search("story_back_txt_rect").collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                print("click")
                current_state = "menu"

    if current_state == "level1":
        screen.blit(lvl_dict.search("lvl_background"),(0,0))
        player.draw(screen)
        player.update()

    pygame.display.update()
    clock.tick(60)