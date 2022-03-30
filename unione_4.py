import pandas as pd
import pygame
import random
import math
import ctypes
import sys
import os
from block import Block
from utilities_func import render_text, game
from parameters import *

ctypes.windll.user32.SetProcessDPIAware()
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
b00.reset(speed=0, decrease=xc, side=0)
block_list.add(b00)
all_sprites_list.add(b00)
sec00 = b00.decrease*DIFF_FACT/60
htime00 = round(sec00)
clock = pygame.time.Clock()

# render text
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Ora osserverai una serie di quadrati", "rappresentanti delle risorse"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Ad ogni quadrato è associato un numero che indica ", "il tempo necessario per ottenere la risorsa"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Le dimensioni del quadrato rappresentano", "il valore della risorsa"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Mentre il numero a lato dello schermo indica il numero", "di secondi che servono per assorbire il quadrato"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra)"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Ora osserverai un esempio automatico"])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

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
           b00.speed = random.choice(SPEED_VALUES)
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
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Durante questo primo gioco di allenamento sarà presente", "un solo quadrato alla volta"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["La durata di questo gioco è di 5 minuti"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
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
results1 = game(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), OBJECT_SIZES, clock, 1)

# render text
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Nel prossimo esperimento saranno presenti", "2 quadrati contemporaneamente"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra, destra)"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Potrai scegliere solo uno dei due quadrati", "quindi scegli con attenzione"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["La durata di questo gioco è di 5 minuti"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
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
                done = True

if flag_quit:
    pygame.quit()
    sys.exit()

done = False

#game2

results2 = game(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), OBJECT_SIZES, clock, 2, stimuli=stimuli, lista=lista)

# results.to_excel("C:/Users/%s/Desktop/%s_2.xlsx" %(user, ID_NUMBER), index=False)
results2.to_excel("%s_2.xlsx" %ID_NUMBER, index=False)

#render text 3
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Nel prossimo esperimento saranno presenti", "3 quadrati contemporaneamente"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra, destra o su)"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Potrai scegliere solo uno dei tre quadrati", "quindi scegli con attenzione"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
            ["La durata di questo gioco è di 5 minuti"])

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT, Tempo_scritte,
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
                done = True
    
if flag_quit:
    pygame.quit()
    sys.exit()

done = False


# game 3
results3 = game(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), OBJECT_SIZES, clock, 3, stimuli=stimuli, lista=lista)

pygame.quit()

# results.to_excel("C:/Users/%s/Desktop/%s.xls" %(user, ID_NUMBER), index=False)
results3.to_excel("%s.xls" %ID_NUMBER, index=False)

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
