import pygame, sys, random

# until 0:54:29 - Collisions (with rects)
# https://www.youtube.com/watch?v=UZg49z76cLw&t=33s
# https://www.youtube.com/watch?v=XRw1FUEsSv4&feature=youtu.be 

# constants
WINDOW_WIDTH = 288
WINDOW_HEIGHT = 512
FPS = 60

DIRECTORY = os.path.dirname(__file__)
HS_FILE = 'highscore.txt'

def load_data(DIRECTORY, HS_FILE):
    with open(os.path.join(DIRECTORY, HS_FILE), 'r') as f:
        try:
            highscore = float(f.read())
        except:
            highscore = 0
    return highscore


def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,430))
	screen.blit(floor_surface,(floor_x_pos+265,430))


def create_pipe():
	random_pipe_pos = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop = (WINDOW_WIDTH + 150, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (WINDOW_WIDTH + 150, random_pipe_pos - 100))
	return bottom_pipe, top_pipe


def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	# only copying the elements that are on the screen
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return visible_pipes


def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= WINDOW_HEIGHT:
			screen.blit(pipe_surface, pipe)
		else:
			# 2nd arg - flip in X direction
			# 3rd arg - flip in Y direction
			flip_pipe = pygame.transform.flip(pipe_surface,False, True)
			screen.blit(flip_pipe, pipe)


def check_collision(pipes):
	global can_score 

	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			can_score = True
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 430:
		can_score = True
		return False

	return True


def rotate_bird(bird):
	# surface, angle, scale
	new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
	return new_bird


def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (50, bird_rect.centery))
	return new_bird, new_bird_rect


def score_display(game_state):
	if game_state == 'main_game':
		# score is float -> conv to integer -> conv to a string
		score_surface = game_font.render(str(int(score)), True, (255,255,255))
		score_rect = score_surface.get_rect(center = (WINDOW_WIDTH/2, 50))
		screen.blit(score_surface, score_rect)

	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)} ', True, (255,255,255))
		score_rect = score_surface.get_rect(center = (WINDOW_WIDTH/2, 50))
		screen.blit(score_surface, score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}' , True, (255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (WINDOW_WIDTH/2, 410))
		screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score


def pipe_score_check():
	global score, can_score
	
	if pipe_list:
		for pipe in pipe_list:
			if 50 < pipe.centerx < 55 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True


# tells the init() method how to initiate the mixer
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

# surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0


bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (50, WINDOW_HEIGHT/2))


BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
# bird_rect = bird_surface.get_rect(center = (50, WINDOW_HEIGHT/2))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

pipe_height = [200, 300, 400]

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 6
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (50, WINDOW_HEIGHT/2)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface, bird_rect = bird_animation()


	screen.blit(bg_surface,(0,0))


	if game_active:
		# Bird
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird, bird_rect)
		game_active = check_collision(pipe_list)

		# Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)
		
		# Score
		pipe_score_check()
		score_display('main_game')
		
	else:
		screen.blit(game_over_surface, game_over_rect)
		high_score = update_score(score, high_score)
		score_display('game_over')

	# floor
	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -288:
		floor_x_pos = 0



	pygame.display.update()	
	clock.tick(FPS)

 