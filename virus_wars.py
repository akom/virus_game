import pygame, random, sys, time

#Initialize pygame
pygame.init()

#Set display window
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Vírus Wars")

#Set FPS and Clock
FPS = 60
clock = pygame.time.Clock()

#Define Classes
class Game():
    """A class to control gameplay"""
    def __init__(self, player, virus_group, life_group):
        """Initilize the game object"""
        #Set game values
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.virus_group = virus_group
        self.life_group = life_group

        #Set sounds and music
        self.kill_virus_sound = pygame.mixer.Sound("Sounds/kill_virus.wav")
        self.wrong_virus_sound = pygame.mixer.Sound("Sounds/wrong_virus.wav")
        self.level_sound = pygame.mixer.Sound("Sounds//Piano_In_The_Dark.wav")
        
        #Set font
        self.font = pygame.font.Font("Fonts/AtlantisText-Regular.ttf", 20)
        self.font_title = pygame.font.Font("Fonts/AtlantisText-Regular.ttf", 50)
        self.font_subtext = pygame.font.Font("Fonts/AtlantisText-Regular.ttf", 25)

        #Set images
        blue_image = pygame.image.load("Images/blue_virus.png")
        green_image = pygame.image.load("Images/green_virus.png")
        purple_image = pygame.image.load("Images/purple_virus.png")
        red_image = pygame.image.load("Images/red_virus.png")

        #This list cooresponds to the virus_type attribute int 0 -> blue, 1 -> green, 2 -> purple, 3 -> red
        self.target_virus_images = [blue_image, green_image, purple_image, red_image]

        self.target_virus_type = random.randint(0,3)
        self.target_virus_image = self.target_virus_images[self.target_virus_type]

        self.target_virus_rect = self.target_virus_image.get_rect()
        self.target_virus_rect.centerx = WINDOW_WIDTH//2
        self.target_virus_rect.top = 30

    def update(self):
        """Update our game object"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        #Check for collisions
        self.check_collisions()

    def draw(self):
        """Draw the HUD and other to the display"""
        #Set colors
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)

        #Add the virus colors to a list where the index of the color matches target_virus_images
        colors = [BLUE, GREEN, PURPLE, RED]

        #Set Background
        

        #Set text
        catch_text = self.font.render("Atacar o Virus", True, BLACK)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH//2
        catch_rect.top = 5

        score_text = self.font.render("Pontos: " + str(self.score), True, BLACK)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Vida: ", True, BLACK)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Rodada Atual: " + str(self.round_number), True, BLACK)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Tempo da Ronda: " + str(self.round_time), True, BLACK)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warp_text = self.font.render("Fugir: " + str(self.player.warps), True, BLACK)
        warp_rect = warp_text.get_rect()
        warp_rect.topright = (WINDOW_WIDTH - 10, 35)

        #Blit the HUD
        
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warp_text, warp_rect)
        
        display_surface.blit(self.target_virus_image, self.target_virus_rect)


        pygame.draw.rect(display_surface, colors[self.target_virus_type], (WINDOW_WIDTH//2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.target_virus_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT-210), 4)
        
        
    def check_collisions(self):
        """Check for collisions between player and virus"""
        #Check for collision between a player and an indiviaual virus
        #We must test the type of the virus to see if it matches the type of our target virus
        collided_virus = pygame.sprite.spritecollideany(self.player, self.virus_group)

        #We collided with a virus
        if collided_virus:
            #Caught the correct virus
            if collided_virus.type == self.target_virus_type:
                self.kill_virus_sound.play()
                self.score += 10*self.round_number
                #Remove caught virus
                collided_virus.remove(self.virus_group)
                if (self.virus_group):
                    #There are more viruss to catch
                    self.choose_new_target()
                else:
                    #The round is complete
                    self.player.reset()
                    self.start_new_round()
            #Caught the wrong virus
            else:
                self.wrong_virus_sound.play()            
                self.player.lives -= 1
                
                for i, life in enumerate(self.life_group):
                    if  i == self.player.lives:
                     self.life_group.remove(life)
                     display_surface.fill((0, 0, 0))
                    
             
                #Check for game over
                if self.player.lives <= 0:
                    self.pause_game("Total de Pontos: " + str(self.score), "Pressione 'Enter' para começar de novo")
                    self.reset_game()
                self.player.reset()


    def start_new_round(self):
        """Populate board with new virus"""
        #Provide a score bonus based on how quickly the round was finished
        self.score += int(100*self.round_number/(1 + self.round_time))
        #Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1

        #Remove any remaining viruss from a game reset
        for virus in self.virus_group:
            self.virus_group.remove(virus)

        #Add viruss to the virus group
        for i in range(self.round_number):
            self.virus_group.add(Virus(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-210), self.target_virus_images[0], 0))
            self.virus_group.add(Virus(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-210), self.target_virus_images[1], 1))
            self.virus_group.add(Virus(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-210), self.target_virus_images[2], 2))
            self.virus_group.add(Virus(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT-210), self.target_virus_images[3], 3))


        #Choose a new target virus
        self.choose_new_target()

        

    def choose_new_target(self):
        """Choose a new target virus for the player"""
        target_virus = random.choice(self.virus_group.sprites())
        self.target_virus_type = target_virus.type
        self.target_virus_image = target_virus.image

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        #Set color
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        #Create the main pause text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        #Create the sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 64)

        #Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        #Pause level sound
        self.level_sound.stop()


        #Pause the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    def reset_game(self):
        """Reset the game"""
        self.score = 0
        self.round_number = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()
        self.level_sound.play(-1)
        x = 70
        for i in range(0, 5):
            life = Life(x,45)
            self.life_group.add(life)
            x += 35
        self.start_new_round()

    def credit(self):
        WHITE= (255, 255, 255)
        BLACK = (0, 0, 0)

        global running

        credit_font = pygame.font.Font("Fonts/AtlantisText-Regular.ttf", 20)
        is_credit = True

        credits = ["Adolfo Kurt Olguin Mostajo - Game Programmer", "Caroline Messias Aloca - Game Art Design", "Melissa Miho Suzaki Morimoto - Game Art Design", "Pedro Henrique Pradela - Game Art Design"]
        text_rects = []
        while is_credit:
            display_surface.fill(WHITE)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_credit = False
                if event.type == pygame.QUIT:
                    is_credit = False
                    running = False

            for i, credit in enumerate(credits):
                text_rect = self.draw_text(credit, credit_font, BLACK, (400), (250 + i * 50 + 10))
                text_rects.append(text_rect)

            self.draw_text("      Pressione 'Enter' para voltar",credit_font, BLACK, (400), (600))

            pygame.display.update()


    def main_menu(self):
        WHITE= (255, 255, 255)
        BLACK = (0, 0, 0)
        YELLOW = (255, 255, 0)
        
        option_font = pygame.font.Font("Fonts/AtlantisText-Regular.ttf", 20)

        options = ["Iniciar Jogo", "Creditos", "Sair"]

        self.image_background = pygame.image.load("Images/background.png")
        self.menu_select_sound = pygame.mixer.Sound("Sounds/menu_selection.wav")
        self.menu_sound = pygame.mixer_music.load("Sounds/Dark Harmony.wav")
        pygame.display.update()
        pygame.mixer_music.play()


        is_menu = True
        while is_menu:                       
            display_surface.fill(WHITE)
            display_surface.blit(self.image_background, (0, 100, 0, 0))
            text_rects = []
            for i, option in enumerate(options):
                text_rect = self.draw_text(option, option_font, BLACK, (WINDOW_HEIGHT//2+200 +i * 15), (WINDOW_HEIGHT//2+150 + i * 50 + 10))
                text_rects.append(text_rect)
                if self.is_mouse_over_text(text_rect):
                    #self.menu_select_sound.play()
                    pygame.draw.line(display_surface, BLACK, (text_rect.left, text_rect.bottom + 5), (text_rect.right, text_rect.bottom + 5), 2)  # Highlight the text with a line when hovered

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, text_rect in enumerate(text_rects):
                    if self.is_mouse_over_text(text_rect):
                        print("Opcao :", options[i])
                        # Add your logic here for the clicked option
                        if options[i] == "Iniciar Jogo":
                            # Start the game
                            pygame.mixer_music.stop()
                            self.level_sound.play(-1)
                            is_menu = False
                            
                        elif options[i] == "Creditos":
                            # Go to the Cretits
                            self.credit()
                        elif options[i] == "Sair":
                            pygame.quit()
                            sys.exit()
            
            pygame.display.update()
            clock.tick(FPS)

    def is_mouse_over_text(self, text_rect):
        mouse_pos = pygame.mouse.get_pos()
        if text_rect.collidepoint(mouse_pos):
            return True
        return False
    
    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        display_surface.blit(text_surface, text_rect)
        return text_rect

class Player(pygame.sprite.Sprite):
    """A player class that the user can control"""
    def __init__(self):
        """Initialize the player"""
        super().__init__()
        self.image = pygame.image.load("Images/player_down.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

        self.lives = 5
        self.warps = 2
        self.velocity = 8

        
        #self.die_sound = pygame.mixer.Sound("Sounds/die.wav")
        #self.warp_sound = pygame.mixer.Sound("Sounds/warp.wav")


    def update(self):
        """Update the player"""
        keys = pygame.key.get_pressed()

        #Move the player within the bounds of the screen
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.image = pygame.image.load("Images/player_left.png")
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.image = pygame.image.load("Images/player_right.png")
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.top > 100:
            self.image = pygame.image.load("Images/player_up.png")
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.bottom < WINDOW_HEIGHT - 127:
            self.image = pygame.image.load("Images/player_down.png")
            self.rect.y += self.velocity


    def warp(self):
        """Warp the player to the bottom 'safe zone'"""
        if self.warps > 0:
            self.warps -= 1
            #self.warp_sound.play()
            self.rect.bottom = WINDOW_HEIGHT


    def reset(self):
        """Resets the players position"""
        self.rect.centerx = WINDOW_WIDTH//2
        self.rect.bottom = WINDOW_HEIGHT

class Virus(pygame.sprite.Sprite):
    """A class to create enemy virus objects"""
    def __init__(self, x, y, image, virus_type):
        """Initialize the virus"""
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #virus type is an int 0 -> blue, 1 -> green, 2 -> purple, 3 -> red
        self.type = virus_type

        #Set random motion
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        self.velocity = random.randint(1, 5)


    def update(self):
        """Update the virus"""
        self.rect.x += self.dx*self.velocity
        self.rect.y += self.dy*self.velocity

        #Bounce the virus off the edges of the display
        if self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1*self.dx
        if self.rect.top <= 100 or self.rect.bottom >= WINDOW_HEIGHT - 120:
            self.dy = -1*self.dy

class Life(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("Images/life.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
       
        
#Create a player group and Player object
my_player_group = pygame.sprite.Group()
my_player = Player()
my_player_group.add(my_player)

#Create a virus group.
my_virus_group = pygame.sprite.Group()

#Create a life group.
my_life_group = pygame.sprite.Group()

x = 70
for i in range(0, 5):
    life = Life(x,45)
    my_life_group.add(life)
    x += 35

#Create a game object
my_game = Game(my_player, my_virus_group, my_life_group)
my_game.main_menu()
#my_game.pause_game("VIRUS WARS", "Pressione 'Enter' para começar")
my_game.start_new_round()

#The main game loop
image_level_background = pygame.image.load("Images/background_level2.png")

running = True
while running:
    #Check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Player wants to warp
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                my_player.warp()

    #Fill the display
    display_surface.fill((255, 255, 255))
    display_surface.blit(image_level_background, (0,0))

    #Update and draw sprite groups
    my_player_group.update()
    my_player_group.draw(display_surface)

    my_virus_group.update()
    my_virus_group.draw(display_surface)

    my_life_group.update()
    my_life_group.draw(display_surface)

    #Update and draw the Game
    my_game.update()
    my_game.draw()

    #Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

#End the game
pygame.quit()