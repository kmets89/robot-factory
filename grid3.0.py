import random
import pygame
from pygame.locals import *


class Monster:
    """ A class for the enemy npcs."""
    def __init__(self,name,stats,damage,text,location,color,bounds,speed):
        self.name = name
        self.stats = stats
        self.damage = damage
        self.text = text
        self.loc = location
        self.color = color
        self.bounds = bounds
        self.speed = speed
    def get_text(self):
        """ Creates a text object for the text at the start of a fight."""
        return font.render(self.text,True,red)
    def move_down(self):
        """ Moves the monster up and down on the grid between its
    lower and upper bounds."""
        self.loc.top += self.speed
        if self.loc.top < self.bounds[0] or self.loc.top > self.bounds[1]:
            self.speed = self.speed * -1
    def move_right(self):
        """ Moves the monster left and right on the grid between its
    lower and upper bounds."""
        self.loc.left += self.speed
        if self.loc.left < self.bounds[0] or self.loc.left > self.bounds[1]:
            self.speed = self.speed * -1

class Upgrades:
    """ A class for the items in the game."""
    def __init__(self,name,stat_index,stat_change,desc):
        self.name = name
        self.stat_index = stat_index
        self.stat_change = stat_change
        self.desc = desc
    def get_desc(self):
        """ Creates a text object for the description of an item."""
        return font.render(self.desc,True,white)
    def get_summary(self):
        """ Returns the description for the stat an item changes."""
        return stat_desc[self.stat_index]
    def update_stats(self,stat_set):
        """ Changes the player's stats for an item."""
        stat_set[self.stat_index] = stat_set[self.stat_index] + self.stat_change
        return stat_set

def encounter(monster,stat_set,skill_set):
    """ Switches between the player's and monster's turn until one dies."""
    global game_over, winner
    skillbox = pygame.Rect(0,650,450,170)
    resultbox = pygame.Rect(470,650,330,170)
    numkey = 0
    player = [s for s in stat_set]
    baddie = monster.stats
    
    pygame.draw.rect(screen,black,textbox)
    screen.blit(monster.get_text(),(100,630))

    #Determines turn order based on speed
    if player[3] >= baddie[3]:
        turn = player
    else:
        turn = baddie

    while player[0] > 0 and baddie[0] > 0:

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_1 or event.key == K_KP1:
                    numkey = 1
                if event.key == K_2 or event.key == K_KP2:
                    numkey = 2
                if event.key == K_3 or event.key == K_KP3:
                    numkey = 3

        #Displays player's skill options
        if turn == player:
            pygame.draw.rect(screen,black,skillbox)
            screen.blit(font.render("What sequence do you want to run?",True,
                                    white),(20,670))
            screen.blit(skill_set[1][0],(20,690))
            screen.blit(skill_set[1][1],(20,710))
            screen.blit(skill_set[1][2],(20,730))
            screen.blit(skill_set[1][3],(50,750))
            pygame.display.update()
            
            if numkey != 0:
                pygame.draw.rect(screen,black,resultbox)
                #Checks to see if an attack hit, based on hit chance against
                #block chance
                if (player[1] + random.randrange(1,21)) >= baddie[2]:
                    if numkey == 1:
                        baddie[0] = baddie[0] - skill_set[0][0]
                    elif numkey == 2:
                        player[0] = player[0] - 20
                        baddie[0] = baddie[0] - skill_set[0][1]
                    elif numkey == 3:
                        player[2] = player[2] + 3
                        baddie[0] = baddie[0] - skill_set[0][2]
                else:
                    screen.blit(font.render(monster.name+" blocked your attack!",
                                            True,red),(470,670))
                #Adjusts monster's health by damage taken
                screen.blit(font.render(monster.name+"'s health is "
                                        +str(baddie[0]),True,white),(470,690))
                turn = baddie
        elif turn == baddie:
            #Checks to see if the monster's attack hit
            if (baddie[1] + random.randrange(1,21)) >= player[2]:
                player[0] = player[0] - monster.damage
            else:
                screen.blit(font.render("You blocked the attack!",True,red),
                            (470,730))
            #Adjusts player's health
            screen.blit(font.render("Your health is "+str(player[0]),True,
                                    white),(470,750))
            numkey = 0
            turn = player
        pygame.display.update()
        clock.tick(20)

    #The game ends if the player's health reaches 0
    if player[0] <= 0:
        winner = False
        game_over = True
        return winner, game_over

def loot(items,stat_set,count):
    """ Randomly chooses two elements from items and displays their text."""
    choice = 0
    scroll = False
    roll = random.sample(items,2)
    
    while choice == 0:
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_1 or event.key == K_KP1:
                    choice = 1
                if event.key == K_2 or event.key == K_KP2:
                    choice = 2
                if event.key == K_RETURN:
                    scroll = True

        #Displays the text after an encounter
        if not scroll and count == 0:
            pygame.draw.rect(screen,black,textbox)
            screen.blit(upgrade_prompts[0],(20,650))
            screen.blit(upgrade_prompts[1],(20,670))
            screen.blit(key_prompts[1],(20,750))
        elif not scroll:
            pygame.draw.rect(screen,black,textbox)
            screen.blit(upgrade_prompts[(count + 1)],(20,650))
            screen.blit(key_prompts[1],(20,750))
        #Displays the item name, description, and description
        #of the stat it affects
        if scroll:
            pygame.draw.rect(screen,black,textbox)       
            screen.blit(font.render("1. "+str(roll[0].name),True,white),(20,650))
            screen.blit(roll[0].get_desc(),(20,670))
            screen.blit(roll[0].get_summary(),(20,710))
            screen.blit(font.render("2. "+str(roll[1].name),True,white),(400,650))
            screen.blit(roll[1].get_desc(),(400,670))
            screen.blit(roll[1].get_summary(),(400,710))

        pygame.display.flip()
        clock.tick(20)

    #Updates the player's stats for their chosen item and removes
    #both from the items list   
        if choice == 1:
            roll[0].update_stats(stat_set)
        elif choice == 2:
            roll[1].update_stats(stat_set)
    items.pop(items.index(roll[0]))
    items.pop(items.index(roll[1]))
    return stat_set, items

def main():
    """ The main game loop."""
    global game_over,winner
    
    done = False
    game_over = False
    winner = True
    encounter_count = 0
    scroll = False

    #Assigns player's hp, hit chance, block chance, and speed
    player_stats = [500,50,50,35]
    #Assigns the damage values for the player's skills and creates text objects
    #for the skill descriptions
    player_skills = [[50,70,20],
    [font.render("1. A basic attack.",True,white),
    font.render("2. A strong attack that causes recoil.",True,white),
    font.render("3. A low power move that increases",True,white),
    font.render("chance to block each time.",True,white)]]
    player = pygame.Rect(373,57,54,54)

    bots = []
    tom = Monster("Tom",[200,40,50,30],50,"Tom has a bone to pick with you!",
                  pygame.Rect(255,57,54,54),yellow,[57,411],5)
    bots.append(tom)
    jerry = Monster("Jerry",[300,45,53,30],50,"Jerry's looking for a fight!",
                    pygame.Rect(491,175,54,54),orange,[491,609],5)
    bots.append(jerry)
    cletus = Monster("Cletus",[500,50,55,35],70,"Cletus takes a swing at you!",
                     pygame.Rect(137,293,54,54),red,[137,373],5)
    bots.append(cletus)
    herman = Monster("Herman",[600,50,60,45],75,"Herman looks at you with fire\
 in his eyes!",
                     pygame.Rect(491,293,54,54),darkred,[293,529],5)
    bots.append(herman)
    marjory = Monster("Marjory",[700,60,65,55],80,"Marjory is on a rampage!",
                      pygame.Rect(137,529,54,54),purple,[137,609],5)
    bots.append(marjory)

    items = [
    Upgrades("Autonomous Galvanizer",0,100,"Galvanizes autonomously."),
    Upgrades("Blaster",1,10,"This one doesn't go to stun."),
    Upgrades("Boots of Swiftness",3,10,"These do not stack."),
    Upgrades("Flamethrower",1,10,"It's good you're not combustible."),
    Upgrades("Internal Steam Boiler",0,100,"Can also be used to brew tea."),
    Upgrades("Liquid Nitrogen Cooling System",3,10,"Overclock your feet!"),
    Upgrades("Titanium Alloy Spine",2,10,"That's about it."),
    Upgrades("Unobtanium Plating",2,10,"Don't ask how we got this.")]

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT:
                    if player.left >= 255:
                        player.left -= 118
                if event.key == K_RIGHT:
                    if player.left <= 491:
                        player.left += 118
                if event.key == K_UP:
                    if player.top >= 148:
                        player.top -= 118
                if event.key == K_DOWN:
                    if player.top <= 502:
                        player.top += 118
                if event.key == K_RETURN:
                    scroll = True

        screen.fill(black)

        #Draws the grid background
        pygame.draw.rect(screen,white,[100,20,600,600])

        #Draws the tiles on the grid
        for t in tiles:
            pygame.draw.rect(screen,navy,t)

        #Draws T-081
        pygame.draw.rect(screen,gray,player)

        #Draws the roguebots
        for b in bots:
            pygame.draw.rect(screen,b.color,b.loc)

        #Moves the roguebots
        tom.move_down()
        jerry.move_right()      
        cletus.move_right()       
        herman.move_down()       
        marjory.move_right()
                         
        #Displays the intro text at the start of the game
        if encounter_count == 0:
            pygame.draw.rect(screen,black,textbox)
            screen.blit(intro[0],(20,650))
            screen.blit(intro[1],(20,670))
            screen.blit(key_prompts[1],(20,770))
            if scroll:
                pygame.draw.rect(screen,black,textbox)
                screen.blit(intro[2],(20,650))
                screen.blit(intro[3],(20,670))
                screen.blit(intro[4],(20,690))
                screen.blit(intro[5],(20,710))
                screen.blit(key_prompts[0],(20,770))

        #If the player hits a roguebot, initiates a fight
        for b in bots:
            if player.colliderect(b.loc):
                encounter(b,player_stats,player_skills)
                if not winner:
                    done = True
                bots.pop(bots.index(b))
                if winner and encounter_count < 4:
                    loot(items,player_stats,encounter_count)
                encounter_count += 1

        #The game ends once the board is cleared
        if encounter_count == 5:
            game_over = True
            return winner

        pygame.display.flip()
        clock.tick(20)


white = (255,255,255)
black = (0,0,0)
navy = (27,8,135)
gray = (209,203,205)
red = (204,10,10)
purple = (102,0,51)
green = (0,255,0)
yellow = (220,220,0)
orange = (244,102,0)
darkred = (102,0,0)

pygame.init()

pygame.font.init()
font = pygame.font.SysFont("consolas",20)
bigfont = pygame.font.SysFont("consolas",40,True)

size = (800,800)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("The Factory")

clock = pygame.time.Clock()

textbox = pygame.Rect(0,630,800,160)

#Creates and populates a list for the tiles on the grid    
tiles = []
for y_co in range(30,591,118):
    for x_co in range(110,691,118):
        tiles.append(pygame.Rect(x_co,y_co,108,108))

intro = [
font.render("Good morning T-081, congratulations on being born!",True,white),
font.render("We have brought you to the test facility to try out your\
 programming.",True,white),
font.render("You can walk up to any of these Roguebots to test",True,white),
font.render("your combat functions.",True,white),
font.render("Unfortunately, none of the other T-series can be here with us,",
            True,white),
font.render("but we have high hopes for you!",True,white)]

upgrade_prompts = [
font.render("Well you didn't have to blow it to pieces.",True,white),
font.render("But you can pick up one of those parts and use it to upgrade\
 yourself.",True,white),
font.render("That was overkill.",True,white),
font.render("You're making a mess, you know.",True,white),
font.render("You're doing this on purpose, aren't you?",True,white)]

stat_desc = [
font.render("Increases max health",True,white),
font.render("Increases attack",True,white),
font.render("Increases chance to block",True,white),
font.render("Increases speed",True,white)]

key_prompts = [
font.render("Use the arrow keys to move",True,white),
font.render("Press enter to continue",True,white),
font.render("Press R to restart",True,white),
font.render("Press Q to quit",True,white)]

#Runs the game loop for the first time
main()

#Game over screen
while game_over:

    screen.fill(black)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
        if event.type == pygame.KEYDOWN:
            if event.key == ord('r'):
                #Runs the game loop again
                main()
            if event.key == ord('q'):
                game_over = False
    
    pygame.draw.rect(screen,navy,[100,100,600,600])
    if winner:
        #Displays the text for a won game
        screen.blit(font.render("Oh, you actually survived.",True,white),
                                (150,230))
        screen.blit(font.render("I mean...",True,white),(150,250))
        screen.blit(bigfont.render("Congratulations!",True,green),(200,330))
        screen.blit(font.render("Does this look like a watercooler?",True,
                                white),(150,430))
        screen.blit(font.render("Get back to work!",True,white),(210,450))
    else:
        #Displays the text for a lost game
        screen.blit(bigfont.render("You exploded!",True,red),(250,250))
        screen.blit(font.render("I guess this is what happens when you use",
                                True,white),(150,390))
        screen.blit(font.render("trial software.",True,white),(150,410))
        screen.blit(font.render("Someone boot up T-082.",True,white),(150,450))
    pygame.draw.rect(screen,white,[140,600,20,20])
    screen.blit(font.render("Press R to restart",True,white),(170,600))
    pygame.draw.rect(screen,white,[440,600,20,20])
    screen.blit(font.render("Press Q to quit",True,white),(470,600))
    pygame.display.flip()

pygame.quit()

