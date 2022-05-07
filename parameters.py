import os
import random

# PARAMETERS
N_elementi_da_ispezionare = [4, 2]
DIFF_FACT = 4
CUTOFF = 400
OBJ_SIZE_min = 30
OBJ_SIZE_max = 100
OBJ_SIZE_stp = 1
OBJ_SIZE_mean = (OBJ_SIZE_min + OBJ_SIZE_max) // 2
OBJ_SIZE_num = (OBJ_SIZE_max - OBJ_SIZE_min)/OBJ_SIZE_stp
OBJ_COL_min = 20
OBJ_COL_max = 60
OBJ_COL_stp = 1
OBJ_COL_mean = (OBJ_COL_min + OBJ_COL_max) // 2
OBJ_COL_num = (OBJ_COL_max - OBJ_COL_min)/OBJ_COL_stp
SPEED_VALUES = [0.008, 0.008]
Tempo_scritte = 1000
FPS = 60
ID_NUMBER = random.randrange(1000, 9999, 1)
FROM = str(ID_NUMBER) + '@prova.prova'
TO = 'gianearnor@gmail.com'
userhome = os.path.expanduser('~')
user = os.path.split(userhome)[-1]
