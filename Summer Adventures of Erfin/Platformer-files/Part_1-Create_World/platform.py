import pygame # import the modules
from pygame.locals import *

pygame.init() # initialize pygame
# create the game window
screen_width = 900
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height)) # displays the window
pygame.display.set_caption('Summer Adventures of Erfin') # puts the name of the game

#define game variables
tile_size = 45


#loads the images
sun_img = pygame.image.load('Platformer-files/img/sun.png')
bg_img = pygame.image.load('Platformer-files/img/sky.png')

def draw_grid(): # creates grid on the map
	for line in range(0, 20):
		pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_width, line * tile_size))
		pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


# create a class
class World():
	def __init__(self, data):
		self.tile_list = [] # stores the images and rectangle

		#loads the images
		dirt_img = pygame.image.load('Platformer-files/img/dirt.png')
		grass_img = pygame.image.load('Platformer-files/img/grass.png')
        # runs through each of the rows/columns and within the rows/columns, goes through the tiles one by one
		row_count = 0 
		for row in data:
			col_count = 0
			for tile in row:
				if tile == 1:
					img = pygame.transform.scale(dirt_img, (tile_size, tile_size)) # scales the dirt image
					img_rect = img.get_rect() # it takes the size of the image and creates a rectangle from it
					img_rect.x = col_count * tile_size # sets the placement of where its going to show
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile) # adds this on the list
				if tile == 2: # loads and scales the images
					img = pygame.transform.scale(grass_img, (tile_size, tile_size))
					img_rect = img.get_rect()
					img_rect.x = col_count * tile_size
					img_rect.y = row_count * tile_size
					tile = (img, img_rect)
					self.tile_list.append(tile)
				col_count += 1 # increases the variable by one
			row_count += 1 # it also increases with the column count
    # iterates through the list and draw them on the screen
	def draw(self):
		for tile in self.tile_list:
			screen.blit(tile[0], tile[1]) # takes the picture and put it on the location of the rectangle coordinate


# create the world map
world_data = [
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], # placement of bits of dirt
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], # creates a dirt outline
[1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1], # other numbers are put throughout the whole progress of the game
[1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1], # the tile 2 represents the placement of the grass
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1], 
[1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1], 
[1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1], 
[1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
[1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]




world = World(world_data)
# loop to keep the window running
run = True
while run:
    # constantly draws them on the screen
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (100, 100)) # keep in mind the order so that the sun won't be covered by the sky or clouds 

	world.draw()

	draw_grid()

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			run = False # exits the game

	pygame.display.update() # it updates the window with all the instructions

pygame.quit()