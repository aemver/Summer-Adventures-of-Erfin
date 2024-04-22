import pygame # import the modules
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init() # initialize pygame

clock = pygame.time.Clock() # to keep track of the time and adjust the fps
fps = 40
# create the game window
screen_width = 900
screen_height = 900

screen = pygame.display.set_mode((screen_width, screen_height)) # displays the window
pygame.display.set_caption('Summer Adventures of Erfin') # puts the name of the game


#define font
font = pygame.font.SysFont('Times New Roman', 70)
font_score = pygame.font.SysFont('Times New Roman', 30)


#define game variables
tile_size = 45
game_over = 0
main_menu = True
level = 1
max_levels = 7
score = 0


#define colours
white = (255, 255, 255)
red = (255, 0, 0)


# loads the images
sun_img = pygame.image.load('Platformer-files/img/sun.png')
bg_img = pygame.image.load('Platformer-files/img/sky.png')
restart_img = pygame.image.load('Platformer-files/img/restart_btn.png')
start_img = pygame.image.load('Platformer-files/img/start_btn.png')
exit_img = pygame.image.load('Platformer-files/img/exit_btn.png')

# loads the sounds
pygame.mixer.music.load('Platformer-files/img/music.wav') # a background music that will constantly play
pygame.mixer.music.play(-1, 0.0, 5000) # it will set a delay that will make the bg music fade in
coin_fx = pygame.mixer.Sound('Platformer-files/img/coin.wav')
coin_fx.set_volume(0.5) # decreases the volume
jump_fx = pygame.mixer.Sound('Platformer-files/img/jump.wav')
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound('Platformer-files/img/game_over.wav')
game_over_fx.set_volume(0.5)


def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


# function to reset level
def reset_level(level):
	player.reset(100, screen_height - 130)
	blob_group.empty()
	platform_group.empty()
	coin_group.empty()
	lava_group.empty()
	exit_group.empty()

	# load in level data and create world
	if path.exists(f'Platformer-files/level{level}_data'):
		pickle_in = open(f'Platformer-files/level{level}_data', 'rb')
		world_data = pickle.load(pickle_in)
	world = World(world_data)
	#create dummy coin for showing the score
	score_coin = Coin(tile_size // 2, tile_size // 2)
	coin_group.add(score_coin)
	return world # loads the new level/s


class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.clicked = False

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		#draw button
		screen.blit(self.image, self.rect)

		return action
		
# create the player
class Player():
	def __init__(self, x, y):
		self.reset(x, y)

	def update(self, game_over):
		dx = 0 # define the variables
		dy = 0
		walk_cooldown = 2.5 # the duration needed to pass to update the index
		col_thresh = 20
        
		if game_over == 0:
			# get keypresses (adds control to the player)
			key = pygame.key.get_pressed()
			if key[pygame.K_SPACE] and self.jumped == False: # allows the character to jump
				jump_fx.play() # plays a sound when character jumps
				self.vel_y = -15 # it jumps off with -15 pixels and moves the character up
				self.jumped = True
			if key[pygame.K_SPACE] == False: # only when the player press 'space', the character jumps again
				self.jumped = False
			if key[pygame.K_LEFT]:
				dx -= 5 # the x coordinate decreases to move to the left
				self.counter += 1 # increases counter when the player press the key/s so when the character is actually moving, it is able to walk
				self.direction = -1
			if key[pygame.K_RIGHT]:
				dx += 5 # the y coordinate increases to move to the right
				self.counter += 1
				self.direction = 1
			if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False: # it resets the counter when the key/s is/are released
				self.counter = 0
				self.index = 0
				if self.direction == 1: # makes sure the direction or image is the same when the player release the key/s
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			# handles the animation
			if self.counter > walk_cooldown: # slows down the animation
				self.counter = 0	
				self.index += 1
				if self.index >= len(self.images_right): # starts at the beginning to avoid an error
					self.index = 0
				if self.direction == 1: # makes sure that it picks the right image depending on the direction
					self.image = self.images_right[self.index]
				if self.direction == -1:
					self.image = self.images_left[self.index]


			# adds gravity
			self.vel_y += 1 # controls the speed of the gravity
			if self.vel_y > 10: # sets the limit
				self.vel_y = 10
			dy += self.vel_y # the dy is constantly increasing by this number when the character jumps

			# check for collision
			self.in_air = True
			for tile in world.tile_list: # a loop to go through each tile on the map
				# checks for collision in the x direction
				if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): # creates a barrier before overlapping happens
					dx = 0 # stops the character from moving when collided in the left or right direction
				# checks for collision in the y direction
				if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): 
					# checks if the character hits his head while jumping/falling, checks whether the player is below or above the block 
					if self.vel_y < 0:
						dy = tile[1].bottom - self.rect.top
						self.vel_y = 0
					# checks if above the ground i.e. falling
					elif self.vel_y >= 0:
						dy = tile[1].top - self.rect.bottom
						self.vel_y = 0
						self.in_air = False


			# checks for collision with the enemies
			if pygame.sprite.spritecollide(self, blob_group, False):
				game_over = -1 # ends the game when the character died
				game_over_fx.play() # plays a sound when character dies

			# checks for collision with the lava
			if pygame.sprite.spritecollide(self, lava_group, False):
				game_over = -1
				game_over_fx.play()

			#check for collision with exit
			if pygame.sprite.spritecollide(self, exit_group, False):
				game_over = 1


			#check for collision with platforms
			for platform in platform_group:
				#collision in the x direction
				if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
					dx = 0
				#collision in the y direction
				if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
					#check if below platform
					if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
						self.vel_y = 0
						dy = platform.rect.bottom - self.rect.top
					#check if above platform
					elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
						self.rect.bottom = platform.rect.top - 1
						self.in_air = False
						dy = 0
					#move sideways with the platform
					if platform.move_x != 0:
						self.rect.x += platform.move_direction


			# updates the player coordinates
			self.rect.x += dx
			self.rect.y += dy


		elif game_over == -1:
			self.image = self.dead_image # changes the image when character dies
			draw_text('GAME OVER!', font, red, (screen_width // 2) - 200, screen_height // 2)
			if self.rect.y > 200: # puts a limit on where the ghost floats away
				self.rect.y -= 5

		# draws the player onto the screen
		screen.blit(self.image, self.rect)

		return game_over
	

	def reset(self, x, y):
		self.images_right = [] # creates a list for the images (animation)
		self.images_left = []
		self.index = 0 # corresponds to the items on the list (access)
		self.counter = 0 # controls the speed of the animation
		for num in range(1, 5): # create a loop to load in the images not individually
			img_right = pygame.image.load(f'Platformer-files/img/guy{num}.png') # the string loads in the images
			img_right = pygame.transform.scale(img_right, (40, 80)) # scales the image
			img_left = pygame.transform.flip(img_right, True, False) # takes the image and flip it on the axis (x, y)
			self.images_right.append(img_right) # whatever puts in here gets added on the list
			self.images_left.append(img_left)
		self.dead_image = pygame.image.load('Platformer-files/img/ghost.png') # it loads an image of a ghost when the character dies
		self.image = self.images_right[self.index] # accesses the images from the list
		self.rect = self.image.get_rect() # it takes the size of the image and creates a rectangle from it
		self.rect.x = x # sets the placement of where its going to show
		self.rect.y = y
		self.width = self.image.get_width() # sets the width and height
		self.height = self.image.get_height()
		self.vel_y = 0 # the velocity when the character jumps is increasing by 0 at the top to the maximum bottom of the screen
		self.jumped = False
		self.direction = 0 # sets the direction
		self.in_air = True


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
					img_rect = img.get_rect()
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
				if tile == 3:
					blob = Enemy(col_count * tile_size, row_count * tile_size + 15) # it places and drops down the enemy on its assigned place or tile
					blob_group.add(blob)
				if tile == 4:
					platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
					platform_group.add(platform)
				if tile == 5:
					platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
					platform_group.add(platform)
				if tile == 6:
					lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2)) # it will place the lava on its designated place
					lava_group.add(lava)
				if tile == 7:
					coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
					coin_group.add(coin)
				if tile == 8:
					exit = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
					exit_group.add(exit)
				col_count += 1 # increases the variable by one
			row_count += 1 # it also increases with the column count

    # iterates through the list and draw them on the screen
	def draw(self):
		for tile in self.tile_list: # saves the tile as a tuple
			screen.blit(tile[0], tile[1]) # takes the picture and put it on the location of the rectangle coordinate


# create a class for the enemy
class Enemy(pygame.sprite.Sprite): 
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load('Platformer-files/img/blob.png')
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_direction = 1
		self.move_counter = 0
    # makes the enemy move from right to left and vice versa
	def update(self):
		self.rect.x += self.move_direction
		self.move_counter += 1
		if abs(self.move_counter) > 50: # counts or limits how many pixels the enemy moves
			self.move_direction *= -1
			self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, move_x, move_y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Platformer-files/img/platform.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.move_counter = 0
		self.move_direction = 1
		self.move_x = move_x
		self.move_y = move_y


	def update(self):
		self.rect.x += self.move_direction * self.move_x
		self.rect.y += self.move_direction * self.move_y
		self.move_counter += 1
		if abs(self.move_counter) > 50:
			self.move_direction *= -1
			self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Platformer-files/img/lava.png')
		self.image = pygame.transform.scale(img, (tile_size, tile_size // 2)) # it will take up half of the block height
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


class Coin(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Platformer-files/img/coin.png')
		self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) # sets the position in the middle


class Exit(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		img = pygame.image.load('Platformer-files/img/exit.png')
		self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


player = Player(100, screen_height - 125)

blob_group = pygame.sprite.Group() # creates a new group or like a list
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# create dummy coin for showing the score
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

#load in level data and create world
if path.exists(f'Platformer-files/level{level}_data'):
    pickle_in = open(f'Platformer-files/level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)

#create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + -30, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

# loop to keep the window running
run = True
while run:

	clock.tick(fps) # limits how quickly it works on the computer or it fixes the fps
    # constantly draws them on the screen
	screen.blit(bg_img, (0, 0))
	screen.blit(sun_img, (100, 100)) # keep in mind the order so that the sun won't be covered by the sky or clouds 

	if main_menu == True:
		if exit_button.draw():
			run = False
		if start_button.draw():
			main_menu = False
	else:
		world.draw()

		if game_over == 0:
			blob_group.update()
			platform_group.update()
			# update score
			# check if a coin has been collected
			if pygame.sprite.spritecollide(player, coin_group, True): # whenever the character collides with the coin, it disappears on the screen
				score += 1
				coin_fx.play() # plays a sound when player collects coins
			draw_text('X' + str(score), font_score, white, tile_size - 10, 10)
		
		blob_group.draw(screen)
		platform_group.draw(screen)
		lava_group.draw(screen)
		coin_group.draw(screen)
		exit_group.draw(screen)

		game_over = player.update(game_over)

		#if player has died
		if game_over == -1:
			if restart_button.draw():
				world_data = []
				world = reset_level(level)
				game_over = 0
				score = 0

		#if player has completed the level
		if game_over == 1:
			# reset game and go to next level
			level += 1
			if level <= max_levels:
				# reset level
				world_data = []
				world = reset_level(level)
				game_over = 0
			else:
				draw_text('YOU WIN!', font, red, (screen_width // 2) - 140, screen_height // 2)
				if restart_button.draw():
					level = 1
					#reset level
					world_data = []
					world = reset_level(level)
					game_over = 0


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False # exits the game

	pygame.display.update() # it updates the window with all the instructions

pygame.quit()