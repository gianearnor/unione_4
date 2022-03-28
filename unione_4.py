import pandas as pd
import pygame
import random
import math
import ctypes
import sys
import os
from block import Block
from utilities_func import render_text

ctypes.windll.user32.SetProcessDPIAware()
# PARAMETERS
N_elementi_da_ispezionare = [4, 2]
DIFF_FACT = 4
CUTOFF = 400
OBJ_SIZE_min = 30
OBJ_SIZE_max = 100
OBJ_SIZE_stp = 1
OBJ_SIZE_mean = (OBJ_SIZE_min + OBJ_SIZE_max) // 2
OBJ_SIZE_num = (OBJ_SIZE_max - OBJ_SIZE_min)/OBJ_SIZE_stp
OBJ_COL_min = 30
OBJ_COL_max = 200
OBJ_COL_stp = 1
OBJ_COL_mean = (OBJ_COL_min + OBJ_COL_max) // 2
OBJ_COL_num = (OBJ_COL_max - OBJ_COL_min)/OBJ_COL_stp
Tempo_scritte = 1000
FPS = 60
ID_NUMBER = random.randrange(1000, 9999, 1)
userhome = os.path.expanduser('~')
user = os.path.split(userhome)[-1]
'''
results = pd.DataFrame({'N': [], 'x0': [], 'scelta': [],'dim_iniz': [],'handling_time': [],
                                'time_0': [], 'click_time': [], 'exit_time': []})

if len(sys.argv) < 2:
    print("Indicare il nome del file dei risultati")
    sys.exit()
'''

OBJECT_SIZES = []
for i in range(OBJ_SIZE_min, OBJ_SIZE_max, OBJ_SIZE_stp):
    OBJECT_SIZES.append((i, i))

pygame.init()

infoScreen = pygame.display.Info()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SPEED_VALUES = [0.008, 0.008]
SCREEN_WIDTH = infoScreen.current_w
SCREEN_HEIGHT = infoScreen.current_h

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

NN = 0
#results = tablib.Dataset()     
#results.headers = ['N', 'scelta', 'dim_iniz', 'handling_time', 'time_0', 'click_time', 'exit_time']

myfont = pygame.font.SysFont("monospace", 40)
myfont2 = pygame.font.SysFont("monospace", 30)

Qm = OBJ_SIZE_mean
Hm = (OBJ_COL_mean * DIFF_FACT)/60
Sm = (math.pi/2 + math.asin((SCREEN_HEIGHT*0.1)/(SCREEN_HEIGHT * 0.5))) / (SPEED_VALUES[0] * 60)

# PREPARO STIMOLI
stimuli = pd.DataFrame({'Size1': [], 'decrease1': [], 'Size2': [], 'decrease2': [], 'Size_decoy': [], 'decrease_decoy': []})
BF = 0.0

for i in range(OBJ_SIZE_min, OBJ_SIZE_max, OBJ_SIZE_stp):
    image00 = i
    B0 = (image00 - Qm)/Qm
    F0 = BF - B0
    xc0 = (60 * (Hm + Sm) * (1 - F0))/DIFF_FACT
    if xc0 > 0:
        F00 = (Hm + Sm - DIFF_FACT * xc0 * FPS / (60*60))/(Hm + Sm)
        image01 = F0 * Qm + Qm
        if image01 > 1:
            B1 = (image01 - Qm) / Qm
            F1 = B0 + F0 - B1
            xc1 = (60 * (Hm + Sm) * (1 - F1))/DIFF_FACT
            stimuli = stimuli.append(pd.DataFrame({'Size1': [image00], 'decrease1': [xc0],
                                                   'Size2': [image01], 'decrease2': [xc1],
                                                   'Size_decoy': [image00 * 0.9], 'decrease_decoy': [xc0]}), ignore_index=True)

stimuli = stimuli.append(stimuli, ignore_index=True)
TOT_STIMULI = len(stimuli)

lista = []
for i in range(TOT_STIMULI):
    if i <= TOT_STIMULI/2:
        lista.append([i, 2])
    else:
        lista.append([i, 3])
random.shuffle(lista)

count_TOT = 0

block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

xc = 0
xc1 = 0
xc2 = 0
frame_count = 0
frame_rate = 60
start_time = 10

score = 0
score1 = 0
score2 = 0
scoreTOT = 0
scoreTOT1 = 0
scoreTOT2 = 0
done = False
results = pd.DataFrame({'NN': [], 'SIDE0': [], 'scelta0': [], 'dim_iniz0': [], 'handling_time0': [],
                        'SIDE1': [], 'scelta1': [], 'dim_iniz1': [], 'handling_time1': []})

# game
b00 = Block(SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZES)
xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
b00.reset(speed=0, decrease=(xc), side=0)
block_list.add(b00)
all_sprites_list.add(b00)
sec00 = b00.decrease*DIFF_FACT/60
htime00 = round(sec00)
clock = pygame.time.Clock()

# render text
render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Ora osserverai una serie di quadrati", "rappresentanti delle risorse"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Ad ogni quadrato è associato un numero che indica ", "il tempo necessario per ottenere la risorsa"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Le dimensioni del quadrato rappresentano", "il valore della risorsa"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Mentre il numero a lato dello schermo indica il numero", "di secondi che servono per assorbire il quadrato"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra)"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Ora osserverai un esempio automatico"])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done=True

    conta_speed = 0

    if b00.c == 0:
        if b00.chosen:
            b00.c = 0
            b00.update()

        elif b00.results[2] == 1:
            results = results.append(pd.DataFrame({'NN': [b00.NN], 'SIDE0': [b00.results[1]], 'scelta0': [b00.results[2]],'dim_iniz0': [b00.results[3]], 'handling_time0': [htime00]}))
            b00.speed = random.choice(SPEED_VALUES)
            xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
            b00.reset(speed=b00.speed, decrease=xc, side=0)
            b00.c += 1
                   
        else:    
           b00.NN += 1
           b00.results = [b00.NN, b00.side, 0, b00.dim_ini, b00.decrease]
           results = results.append(pd.DataFrame({'NN': [b00.NN], 'SIDE0': [b00.results[1]], 'scelta0': [b00.results[2]],'dim_iniz0': [b00.results[3]], 'handling_time0': [htime00]}))
           b00.speed =  random.choice(SPEED_VALUES)
           xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
           b00.reset(speed=b00.speed, decrease=xc, side=0)
           b00.c += 1

    elif b00.NN < N_elementi_da_ispezionare[0] or b00.c < 100:
        conta_speed += 1
        b00.update()            
    elif b00.NN >= N_elementi_da_ispezionare[0] and b00.c == 100:
        b00.chosen = [b00.rect.x, b00.rect.y]
        conta_speed += 1
        score = b00.dim * .75
        scoreTOT = scoreTOT + score
        
        b00.update()

    if b00.NN == sum(N_elementi_da_ispezionare): 
        done = True

    screen.fill(WHITE)

    all_sprites_list.draw(screen)
    if scoreTOT < SCREEN_WIDTH//2: 
        pygame.draw.rect(screen, RED, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT, 100)))
    else:
        pygame.draw.rect(screen, GREEN, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT, 100)))
    if scoreTOT > 1:
        scoreTOT -= 0.02
    sy = str(round(scoreTOT))
    text_score = myfont2.render('PUNTEGGIO: %s' % sy, False, (0, 0, 0))
    
    screen.blit(text_score, (SCREEN_WIDTH//2-100, SCREEN_HEIGHT-100))

    timer_string = "Tempo rimanente: 05:00"
 
    text_time = myfont2.render(timer_string, True, BLACK)
 
    screen.blit(text_time, (SCREEN_WIDTH//2-200, 50))

    frame_count += 1
    
    sec00 = b00.decrease*DIFF_FACT/60
    text_xc = myfont.render(str(round(sec00)), False, (0, 0, 0))
    screen.blit(text_xc, (SCREEN_WIDTH//2-800, SCREEN_HEIGHT-700))
    
    pygame.display.flip()
    
    clock.tick(60)

# render text
render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Durante questo primo gioco di allenamento sarà presente", "un solo quadrato alla volta"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["La durata di questo gioco è di 5 minuti"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per iniziare il gioco premi la barra spaziatrice"])
clock.tick(60)

# wait
done = False
flag_quit = False
while not done and not flag_quit:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            done = True
        if event.type == pygame.QUIT:
            flag_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    
if flag_quit:
    pygame.quit()
    sys.exit()

done = False
           
#  game         

block_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()           
frame_count = 0
frame_rate = 60
start_time = 30 #300
b01 = Block(SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZES)
xc1 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
b01.reset(speed=0, decrease=(xc1), side=0)
block_list.add(b01)
all_sprites_list.add(b01)
sec01 = b01.decrease*DIFF_FACT/60
htime01 = round(sec01)

while not done:
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                for b01 in block_list:
                    if b01.speed:
                        b01.chosen = [b01.rect.x, b01.rect.y]
                        score1 = b01.dim * .75
                        scoreTOT1 = scoreTOT1 + score1

    if b01.c == 0:
        if b01.chosen:
            b01.c = 0
            b01.update()
           
        elif b01.results[2] == 1:

            results = results.append(pd.DataFrame({'NN': [b01.NN], 'SIDE0': [b01.results[1]], 'scelta0': [b01.results[2]], 'dim_iniz0': [b01.results[3]],'handling_time0': [htime01]}))

            b01.speed = random.choice(SPEED_VALUES)
               
            xc1 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
            b01.reset(speed=b01.speed, decrease=xc1, side=0)
               
            b01.c += 1
                    
        else:    
            b01.NN += 1
             
            b01.results = [b01.NN, b01.side, 0, b01.dim_ini, b01.decrease]

            results = results.append(pd.DataFrame({'NN': [b01.NN], 'SIDE0': [b01.results[1]], 'scelta0': [b01.results[2]], 'dim_iniz0': [b01.results[3]],'handling_time0': [htime01]}))
           
            b01.speed = random.choice(SPEED_VALUES)
            xc1 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
            b01.reset(speed=b01.speed, decrease=xc1, side=0)
                
            b01.c += 1

    else:  
        b01.update()

    #print(conta_speed, b.speed, somma_passi)
    screen.fill(WHITE)

    all_sprites_list.draw(screen)
    if scoreTOT1 < SCREEN_WIDTH//2: 
        pygame.draw.rect(screen, RED, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT1, 100)))
    else:
        pygame.draw.rect(screen, GREEN, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT1, 100)))
    #pygame.draw.rect(screen, RED, pygame.Rect([0, SCREEN_HEIGHT-100], [scoreTOT, 100]))
    if scoreTOT1 > 1:
        scoreTOT1 -= 0.02

    sy = str(round(scoreTOT1))

    text_score = myfont2.render('PUNTEGGIO: %s' % (sy), False, (0, 0, 0))
    
    screen.blit(text_score, (SCREEN_WIDTH//2-100, SCREEN_HEIGHT-100))

    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0
 
    minutes = total_seconds // 60
 
    seconds = total_seconds % 60
 
    timer_string = "Tempo rimanente: {0:02}:{1:02}".format(minutes, seconds)
 
    text_time = myfont2.render(timer_string, True, BLACK)
 
    screen.blit(text_time,(SCREEN_WIDTH//2-200, 50))

    frame_count += 1
    
    if minutes == 0 and seconds == 0:
                done=True
    sec00 = b01.decrease*DIFF_FACT/60
    text_xc = myfont.render(str(round(sec00)), False, (0, 0, 0))
    screen.blit(text_xc, (SCREEN_WIDTH//2-800, SCREEN_HEIGHT-700))

    pygame.display.flip()

    clock.tick(60)

# render text
render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Nel prossimo esperimento saranno presenti", "2 quadrati contemporaneamente"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra, destra)"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Potrai scegliere solo uno dei due quadrati", "quindi scegli con attenzione"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["La durata di questo gioco è di 5 minuti"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per iniziare il gioco premi la barra spaziatrice"])
clock.tick(60)

done = False
flag_quit = False
while not done and not flag_quit:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            done = True
        if event.type == pygame.QUIT:
            flag_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done=True
    
if flag_quit:
    pygame.quit()
    sys.exit()

done = False

#game2
block_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

b02 = Block(SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZES)
xc2 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
b02.reset(speed=0, decrease=(xc2), side=0)
block_list.add(b02)
all_sprites_list.add(b02)


b03 = Block(SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZES)
xc03 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
b03.reset(speed=0, decrease=(xc03), side=1)
block_list.add(b03)
all_sprites_list.add(b03)

frame_count = 0
frame_rate = 60
start_time = 300
sec02 = b02.decrease*DIFF_FACT/60
htime02 = round(sec02)
sec03 = b03.decrease*DIFF_FACT/60
htime03 = round(sec03)
done = False

while not done:

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done=True
        elif event.type == pygame.QUIT:
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and (not b02.chosen and not b03.chosen):
               b02.chosen = [b02.rect.x, b02.rect.y] 
               b03.rejected = [b03.rect.x, b03.rect.y]
               score2 = b02.dim * 2.75                          
               scoreTOT2 = scoreTOT2 + score2
               
            if event.key == pygame.K_RIGHT and (not b02.chosen and not b03.chosen):
               b03.chosen = [b03.rect.x, b03.rect.y] 
               b02.rejected = [b02.rect.x, b02.rect.y]
               score2 = b03.dim * 2.75               
               scoreTOT2 = scoreTOT2 + score2

    if b02.c == 0 and b03.c == 0:
        if b03.chosen:
            b02.c = 0
            b03.update()
            
        elif b02.chosen:
            b03.c = 0
            b02.update()
            
        elif b02.results[2] == 1 or b03.results[2] == 1:

            results = results.append(pd.DataFrame({'NN': [b02.NN], 'SIDE0': [b02.results[1]], 'scelta0': [b02.results[2]], 'dim_iniz0': [b02.results[3]],'handling_time0': [htime02],
                                                 'SIDE1': [b03.results[1]], 'scelta1': [b03.results[2]], 'dim_iniz1': [b03.results[3]], 'handling_time1': [htime03]}))
                 
            b02.speed = random.choice(SPEED_VALUES)
            b03.speed = b02.speed
            xc2 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
            b02.reset(speed=b02.speed, decrease=(xc2), side=0)
            xc03 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
            b03.reset(speed=b03.speed, decrease=(xc03), side=1)
            b02.c += 1
            b03.c += 1            
        else:    
           b02.NN += 1
            
           b02.results = [b02.NN, b02.side, 0, b02.dim_ini, b02.decrease]
           b03.results = [b02.NN, b03.side, 0, b03.dim_ini, b03.decrease]

              
           results = results.append(pd.DataFrame({'NN': [b02.NN], 'SIDE0': [b02.results[1]], 'scelta0': [b02.results[2]], 'dim_iniz0': [b02.results[3]],'handling_time0': [htime02],
                                                 'SIDE1': [b03.results[1]], 'scelta1': [b03.results[2]], 'dim_iniz1': [b03.results[3]], 'handling_time1': [htime03]}))
           
           b02.speed =  random.choice(SPEED_VALUES)
           b03.speed =  b02.speed
           xc2 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
           b02.reset(speed=b02.speed, decrease=(xc2), side=0)
           xc03 = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
           b03.reset(speed=b03.speed, decrease=(xc03), side=1)
           b02.c += 1
           b03.c += 1 

    else:  
        b02.update()
        b03.update()
        
    if b02.done == True or b03.done == True: 
        done = True

    
    if scoreTOT2 >0 :
        scoreTOT2 -= 0.02

    screen.fill(WHITE)

    all_sprites_list.draw(screen)

    if scoreTOT2 < SCREEN_WIDTH//2: 
        pygame.draw.rect(screen, RED, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT2, 100)))
    else:
        pygame.draw.rect(screen, GREEN, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT2, 100)))

    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0
 
    minutes = total_seconds // 60
 
    seconds = total_seconds % 60
 
    timer_string = "Tempo rimanente: {0:02}:{1:02}".format(minutes, seconds)
 
    text_time = myfont.render(timer_string, True, BLACK)
 
    screen.blit(text_time,(SCREEN_WIDTH//2-200, 50))

    frame_count += 1
    
    if minutes == 0 and seconds == 0:
        done=True
                
    sy = str(round(scoreTOT2))
    
    text_score2 = myfont.render('PUNTEGGIO: %s' % (sy), False, (0, 0, 0))
    
    screen.blit(text_score2,(SCREEN_WIDTH//2-100, SCREEN_HEIGHT-100))
           
    sec02 = xc2*DIFF_FACT/60
    sec03 = xc03*DIFF_FACT/60
    
    text_xc2 = myfont.render(str(round(sec02)), False, (0, 0, 0))
    screen.blit(text_xc2, (SCREEN_WIDTH//2-800, SCREEN_HEIGHT-700))
    
    text_xc03 = myfont.render(str(round(sec03)), False, (0, 0, 0))
    screen.blit(text_xc03, (SCREEN_WIDTH//2+800, SCREEN_HEIGHT-700))
  
    pygame.display.flip()

    clock.tick(60)
    # results.to_excel("C:/Users/%s/Desktop/%s_2.xlsx" %(user, ID_NUMBER), index=False)
    results.to_excel("%s_2.xlsx" %ID_NUMBER, index=False)

#render text 3
render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Nel prossimo esperimento saranno presenti", "3 quadrati contemporaneamente"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra, destra o su)"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Potrai scegliere solo uno dei tre quadrati", "quindi scegli con attenzione"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["La durata di questo gioco è di 5 minuti"])

render_text(screen, myfont, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per iniziare il gioco premi la barra spaziatrice"])
clock.tick(60)

done = False
flag_quit = False
while not done and not flag_quit:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            done = True
        if event.type == pygame.QUIT:
            flag_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done=True
    
if flag_quit:
    pygame.quit()
    sys.exit()

done = False


# game 3

block_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()


clock = pygame.time.Clock()
scoreTOT3 = 0
score3 = 0
done = False
xc = 0
frame_count = 0
frame_rate = 60
start_time = 300


b04 = Block(SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZES)
xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
b04.reset_circle(speed=0, decrease=xc, side=0, image= 0)
block_list.add(b04)
all_sprites_list.add(b04)

b05 = Block(SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZES)
xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
b05.reset_circle(speed=0, decrease=xc, side=1, image= 0)
block_list.add(b05)
all_sprites_list.add(b05)

b0D = Block(SCREEN_WIDTH, SCREEN_HEIGHT, OBJECT_SIZES)
xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
b0D.reset_line(speed0=0, decrease=xc, side=2, image= 0)
block_list.add(b0D)
all_sprites_list.add(b0D)

sec04 = b04.decrease*DIFF_FACT/60
htime04 = round(sec04)
sec05 = b05.decrease*DIFF_FACT/60
htime05 = round(sec05)
sec0D = b0D.decrease*DIFF_FACT/60
htime0D = round(sec0D)
# render text
screen.fill(WHITE)

done = False
      
       

somma_passi = 0 

results = pd.DataFrame({'NN': [], 'SIDE0': [], 'scelta0': [],'dim_iniz0': [],'handling_time0': [],
                       'SIDE1': [], 'scelta1': [],'dim_iniz1': [],'handling_time1': [],
                       'SIDED': [], 'sceltaD': [],'dim_inizD': [],'handling_timeD': []})
conta = 0
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done=True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and (not b04.chosen and not b05.chosen and not b0D.chosen):
               b04.chosen = [b04.rect.x, b04.rect.y] 
               b05.rejected = [b05.rect.x, b05.rect.y]
               b0D.rejected = [b0D.rect.x, b0D.rect.y]
               score3 = b04.dim * .75
               scoreTOT3 = scoreTOT3 + score3 
               
            if event.key == pygame.K_RIGHT and (not b04.chosen and not b05.chosen and not b0D.chosen):
               b05.chosen = [b05.rect.x, b05.rect.y] 
               b04.rejected = [b04.rect.x, b04.rect.y]
               b0D.rejected = [b0D.rect.x, b0D.rect.y]
               score3 = b05.dim * .75
               scoreTOT3 = scoreTOT3 + score3 
               
            if event.key == pygame.K_UP and (not b04.chosen and not b05.chosen and not b0D.chosen):
               b0D.chosen = [b0D.rect.x, b0D.rect.y] 
               b04.rejected = [b04.rect.x, b04.rect.y]
               b05.rejected = [b05.rect.x, b05.rect.y]               
               score3 = b0D.dim * .75
               scoreTOT3 = scoreTOT3 + score3 

    
    if b04.c == 0 and b05.c == 0 and b0D.c == 0:
        if b05.chosen:
            b04.c = 0
            b05.update_circle()
            b0D.c = 0
            
        elif b04.chosen:
            b05.c = 0
            b04.update_circle()
            b0D.c = 0

        elif b0D.chosen:
            b04.c = 0
            b05.c = 0
            b0D.update_line()            
            
        elif b04.results[2] == 1 or b05.results[2] == 1 or b0D.results[2] == 1:

            #print(b04.NN[0],b05.NN[1], b04.results, b05.results, b0D.results)            
            results = results.append(pd.DataFrame({'NN': [b04.NN], 'SIDE0': [b04.results[1]], 'scelta0': [b04.results[2]],
                                  'dim_iniz0': [b04.results[3]], 'handling_time0': [htime04],
                                  'SIDE1': [b05.results[1]], 'scelta1': [b05.results[2]], 'dim_iniz1': [b05.results[3]],
                                  'handling_time1': [htime05],
                                  'SIDED': [b0D.results[1]], 'sceltaD': [b0D.results[2]], 'dim_inizD': [b0D.results[3]],
                                  'handling_timeD': [htime0D]}))


            b04.speed =  random.choice(SPEED_VALUES)
            b05.speed = b04.speed
            b0D.speed = b04.speed

            case = lista[conta]
            exp_stim = stimuli.loc[[case[0]]]
            num_stim = case[1]
            
            image00 = exp_stim.Size1.values.tolist()[0]
            image01 = exp_stim.Size2.values.tolist()[0]
            xc0 = exp_stim.decrease1.values.tolist()[0]
            xc1 = exp_stim.decrease2.values.tolist()[0]
            
            if random.choice([1, 2]) == 1:
                    image0D = max(image00, image01) * 0.8
                    xcD = max(xc0, xc1)
            else:
                    image0D = min(image00, image01)
                    xcD = min(xc0, xc1) * 1.2
           
                #b0D.speed = 0

            b04.reset_circle(speed=b04.speed, decrease=xc0, side=0, image=int(image00))
            b05.reset_circle(speed=b05.speed, decrease=xc1, side=1, image=int(image01))
            b0D.reset_line(speed0=b0D.speed, decrease=xcD, side=2, image=int(image0D))
            b04.c += 1
            b05.c += 1            
            b0D.c += 1
            conta += 1
            #print([image00, xc0], [image01, xc1],[image0D, xcD])

        else:    
            b04.NN += 1
            b05.NN += 1
            b0D.NN += 1
            b04.results = [b04.NN, b04.side, 0, b04.dim_ini, b04.decrease, 0]
            b05.results = [b05.NN, b05.side, 0, b05.dim_ini, b05.decrease, 0]
            #print(b04.side, b05.side,b0D.side)
            b0D.results = [b0D.NN, b0D.side, 0, b0D.dim_ini, b0D.decrease, 0]           

            #print(b04.NN[0],b05.NN[1], b0D.NN[2], b04.results, b05.results) 

            results = results.append(pd.DataFrame({'NN': [b04.NN], 'SIDE0': [b04.results[1]], 'scelta0': [b04.results[2]],
                                   'dim_iniz0': [b04.results[3]], 'handling_time0': [htime04],
                                    
                                  'SIDE1': [b05.results[1]], 'scelta1': [b05.results[2]], 'dim_iniz1': [b05.results[3]],
                                  'handling_time1': [htime05], 
                                  'SIDED': [b0D.results[1]], 'sceltaD': [b0D.results[2]], 'dim_inizD': [b0D.results[3]],
                                  'handling_timeD': [htime0D]}))
           
            b04.speed = random.choice(SPEED_VALUES)
            b05.speed = b04.speed
            b0D.speed = b04.speed

            case = lista[conta]
            exp_stim = stimuli.loc[[case[0]]]
            num_stim = case[1]
            
            image00 = exp_stim.Size1.values.tolist()[0]
            image01 = exp_stim.Size2.values.tolist()[0]
            xc0 = exp_stim.decrease1.values.tolist()[0]
            xc1 = exp_stim.decrease2.values.tolist()[0]
            
            if random.choice([1, 2]) == 1:
                    image0D = max(image00, image01) * 0.8
                    xcD = max(xc0, xc1)
            else:
                    image0D = min(image00, image01)
                    xcD = min(xc0, xc1) * 1.2

            b04.reset_circle(speed=b04.speed, decrease=xc0, side=0, image=int(image00))
            b05.reset_circle(speed=b05.speed, decrease=xc1, side=1, image=int(image01))
            b0D.reset_line(speed0=b0D.speed, decrease=xcD, side=2, image=int(image0D))
            b04.c += 1
            b05.c += 1            
            b0D.c += 1
            conta += 1
    else:  
        b04.update_circle()
        b05.update_circle()
        b0D.update_line()

    if b04.done == True or b05.done == True or b0D.done == True: 
        done = True

    screen.fill(WHITE)

    all_sprites_list.draw(screen)
    if scoreTOT3 > 1:
        scoreTOT3 -= 0.02
    if scoreTOT3 < SCREEN_WIDTH//2: 
        pygame.draw.rect(screen, RED, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT3, 100)))
    else:
        pygame.draw.rect(screen, GREEN, pygame.Rect((0, SCREEN_HEIGHT-100), (scoreTOT3, 100)))
    #pygame.draw.rect(screen, RED, pygame.Rect([0, SCREEN_HEIGHT-100], [scoreTOT3, 100]))

    sy = str(round(scoreTOT3))
    
    text_score = myfont.render('PUNTEGGIO: %s' % (sy), False, (0, 0, 0))
    
    screen.blit(text_score,(SCREEN_WIDTH//2-100, SCREEN_HEIGHT-100))
   
    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0
 
    minutes = total_seconds // 60
 
    seconds = total_seconds % 60
 
    timer_string = "Tempo rimanente: {0:02}:{1:02}".format(minutes, seconds)
 
    text_time = myfont.render(timer_string, True, BLACK)
 
    screen.blit(text_time,(SCREEN_WIDTH//2-200, 50))

    frame_count += 1
    
    if minutes == 0 and seconds == 0:
                done=True
    
    sec00 = xc0*DIFF_FACT/60
    sec01 = xc1*DIFF_FACT/60
    sec0D = xcD*DIFF_FACT/60
    
    text_xc1 = myfont.render(str(round(sec00)), False, (0, 0, 0))
    screen.blit(text_xc1, (SCREEN_WIDTH//2-800, SCREEN_HEIGHT-700))
    
    text_xc2 = myfont.render(str(round(sec01)), False, (0, 0, 0))
    screen.blit(text_xc2, (SCREEN_WIDTH//2+800, SCREEN_HEIGHT-700))
      
    text_xcD = myfont.render(str(round(sec0D)), False, (0, 0, 0))
    screen.blit(text_xcD, (SCREEN_WIDTH//2-100, SCREEN_HEIGHT-700))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()

# results.to_excel("C:/Users/%s/Desktop/%s.xls" %(user, ID_NUMBER), index=False)
results.to_excel("%s.xls" %ID_NUMBER, index=False)

'''
Qm = np.mean(results.dim_iniz)
Sm = np.mean(results.click_time[results.scelta == 0] - results.time_0[results.scelta == 0])
handling = results.exit_time[results.scelta == 1] - results.click_time[results.scelta == 1]
Hm = np.mean(handling)
decision_time = results.click_time - results.time_0
decision_time[results.scelta == 0] = 0
Decision_m = np.mean(decision_time)
Threshold = Qm/(Sm + Hm)
Htime = Hm / np.mean(results.handling_time[results.scelta == 1]) * results.handling_time
Value = results.dim_iniz/Htime
Threshold = Qm/(Sm + Hm + Decision_m)
Expected_choice = (Value > Threshold) * 1
risu = pd.DataFrame({'N': results.N[sum(N_elementi_da_ispezionare):], 'Htime': Htime[sum(N_elementi_da_ispezionare):],
                    'Value': Value[sum(N_elementi_da_ispezionare):], 'Decision_time': 
                    decision_time[sum(N_elementi_da_ispezionare):],'Qm': Qm, 'Sm': Sm, 'Hm': Hm, 
                    'Threshold': Threshold, 'Expected_choice': Expected_choice[sum(N_elementi_da_ispezionare):]})

results = pd.merge(results, risu, on = 'N')
maxERR = results.Value[results.Value < Threshold]
valueERR = abs(results.Value[results.scelta != results.Expected_choice] - Threshold)
valuescore2 = 1 - np.sum(valueERR) / np.sum(maxERR)
n_ERR = np.size(valueERR)
n_CORRECT = np.size(results.Value) - n_ERR
cols = results.columns.tolist()
cols = cols[:5] + cols[6:] + [cols[5]]
results = results[cols]
results.to_csv('prova_OK.txt', sep="\t")
print('score2 results = ', valueSCORE)
print('TOTALE SCELTE NON OTTIMALI = ', n_ERR)
print('TOTALE SCELTE OTTIMALI     = ', n_CORRECT)
print('% SCELTE CORRETTE          = ', n_CORRECT/(n_CORRECT + n_ERR))
'''
