import pygame
import random
import math
import ctypes
import sys
import os
from block import Block
from utilities_func import render_text, game, tutorial_game, wait_func, send_email
from parameters import *
from zipfile import ZipFile
import shutil
import csv

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

clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

infoScreen = pygame.display.Info()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH = infoScreen.current_w
SCREEN_HEIGHT = infoScreen.current_h

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

myfont = pygame.font.SysFont("monospace", 40)
myfont2 = pygame.font.SysFont("monospace", 30)

Qm = OBJ_SIZE_mean
Hm = (OBJ_COL_mean * DIFF_FACT)/60
Sm = (math.pi/2 + math.asin((SCREEN_HEIGHT*0.1)/(SCREEN_HEIGHT * 0.5))) / (SPEED_VALUES[0] * 60)

# PREPARO STIMOLI
# stimuli = pd.DataFrame({'Size1': [], 'decrease1': [], 'Size2': [], 'decrease2': [], 'Size_decoy': [], 'decrease_decoy': []})
BF = 0.0
size1 = []
decrease1 = []
size2 = []
decrease2 = []
size_decoy = []
decrease_decoy = []
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
            size1.append(image00)
            decrease1.append(xc0)
            size2.append(image01)
            decrease2.append(xc1)
            size_decoy.append(image00 * 0.9)
            decrease_decoy.append(xc0)

stimuli = {'Size1': size1, 'decrease1': decrease1, 'Size2': size2, 'decrease2': decrease2, 'Size_decoy': size_decoy, 'decrease_decoy': decrease_decoy}
# stimuli = stimuli.append(stimuli, ignore_index=True)
TOT_STIMULI = len(size1)

lista = []
for i in range(TOT_STIMULI):
    if i <= TOT_STIMULI/2:
        lista.append([i, 2])
    else:
        lista.append([i, 3])
random.shuffle(lista)

# render text
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Benvenuto all'esperimento comportamentale di Daniel Migliori"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            [f"Il tuo codice identificativo e' {ID_NUMBER}"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Ora osserverai una serie di quadrati", "rappresentanti delle risorse"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Ad ogni quadrato è associato un numero che indica ", "il tempo necessario per ottenere la risorsa"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Le dimensioni del quadrato rappresentano", "il valore della risorsa"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Mentre il numero a lato dello schermo indica il numero", "di secondi che servono per assorbire il quadrato"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra)"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Ora osserverai un esempio automatico"])
wait_func(clock)

# Tutorial Game
results_tutorial = tutorial_game(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), OBJECT_SIZES, clock)

# render text
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Durante questo primo gioco di allenamento sarà presente", "un solo quadrato alla volta"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["La durata di questo gioco è di 5 minuti"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Per iniziare il gioco premi la barra spaziatrice"])

# wait
wait_func(clock)

#  game
results_column1, results1 = game(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), OBJECT_SIZES, clock, 1)

# render text
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Nel prossimo esperimento saranno presenti", "2 quadrati contemporaneamente"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra, destra)"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Potrai scegliere solo uno dei due quadrati", "quindi scegli con attenzione"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["La durata di questo gioco è di 5 minuti"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Per iniziare il gioco premi la barra spaziatrice"])

# wait
wait_func(clock)

#game2

results_column2, results2 = game(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), OBJECT_SIZES, clock, 2, stimuli=stimuli, lista=lista)

# results.to_excel("C:/Users/%s/Desktop/%s_2.xlsx" %(user, ID_NUMBER), index=False)
# results2.to_excel("%s_2.xlsx" %ID_NUMBER, index=False)

#render text 3
render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Nel prossimo esperimento saranno presenti", "3 quadrati contemporaneamente"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Lo scopo del gioco è ottenere la maggior quantità", "possibile di punti prima dello scadere del tempo"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Per ottenere la risorsa premi sulla tastiera la frecca direzionale", "corrispondente alla posizione del quadrato (sinistra, destra o su)"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Potrai scegliere solo uno dei tre quadrati", "quindi scegli con attenzione"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Il tuo punteggio totale sarà visibile nella parte bassa", "dello schermo mediante una barra rossa"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Inoltre il tuo punteggio diminuirà ogni secondo", "quindi cerca di essere rapido nelle tue scelte"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["La durata di questo gioco è di 5 minuti"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Per iniziare il gioco premi la barra spaziatrice"])

# wait
wait_func(clock)

# game 3
results_column3, results3 = game(screen, (SCREEN_WIDTH, SCREEN_HEIGHT), OBJECT_SIZES, clock, 3, stimuli=stimuli, lista=lista)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["L'esperimento e' concluso.", "Grazie della tua partecipazione"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            [f"Il tuo codice identificativo e' {ID_NUMBER}"])
wait_func(clock)

render_text(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            ["Premere la Barra Spaziatrice per chiudere il programma"])
wait_func(clock)

pygame.quit()

# results.to_excel("C:/Users/%s/Desktop/%s.xls" %(user, ID_NUMBER), index=False)
# results3.to_excel("%s.xls" %ID_NUMBER, index=False)

# Genera l'output
output_path = os.path.join(os.getcwd(), f"output_{ID_NUMBER}")
output_archive = os.path.join(os.getcwd(), f"output_archive_{ID_NUMBER}")
if not os.path.isdir(output_path):
    os.mkdir(output_path)
output_file1 = os.path.join(output_path, f"game1_{ID_NUMBER}.csv")
output_file2 = os.path.join(output_path, f"game2_{ID_NUMBER}.csv")
output_file3 = os.path.join(output_path, f"game3_{ID_NUMBER}.csv")
with open(output_file1, 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(results_column1)
    write.writerows(results1)
with open(output_file2, 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(results_column2)
    write.writerows(results2)
with open(output_file3, 'w', newline='') as f:
    write = csv.writer(f)
    write.writerow(results_column3)
    write.writerows(results3)
shutil.make_archive(output_archive, 'zip', output_path)
shutil.rmtree(output_path)

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
