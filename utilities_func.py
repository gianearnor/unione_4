import pygame
import sys
import random
import pandas as pd
from block import Block
from parameters import *
import smtplib
from email.mime.text import MIMEText


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def render_text(screen, screen_width, screen_height, tempo_scritte, text):
    screen.fill(WHITE)
    myfont = pygame.font.SysFont("monospace", 40)
    if type(text) != list:
        text = [text]
    for i in range(len(text)):
        label = myfont.render(text[i], 1, (0, 0, 0))
        text_rect = label.get_rect(center=(screen_width / 2, screen_height / 2 - 40 + i*40))
        screen.blit(label, text_rect)
    pygame.display.flip()
    pygame.time.wait(tempo_scritte)


def wait_func(clock):
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


def tutorial_game(screen, screen_dim, object_sizes, clock):
    block_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    screen_width, screen_height = screen_dim
    myfont = pygame.font.SysFont("monospace", 40)
    myfont2 = pygame.font.SysFont("monospace", 30)
    b0 = Block(screen_width, screen_height, object_sizes)
    xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
    b0.reset(speed=0, decrease=xc, side=0)
    block_list.add(b0)
    all_sprites_list.add(b0)
    sec00 = b0.decrease * DIFF_FACT / 60
    htime00 = round(sec00)
    scoreTOT = 0
    done = False
    results = pd.DataFrame({'NN': [], 'SIDE0': [], 'scelta0': [], 'dim_iniz0': [], 'handling_time0': []})
    frame_count = 0

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        conta_speed = 0

        if b0.c == 0:
            if b0.chosen:
                b0.c = 0
                b0.update()

            elif b0.results[2] == 1:
                results = results.append(pd.DataFrame(
                    {'NN': [b0.NN], 'SIDE0': [b0.results[1]], 'scelta0': [b0.results[2]],
                     'dim_iniz0': [b0.results[3]], 'handling_time0': [htime00]}))
                b0.speed = random.choice(SPEED_VALUES)
                xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
                b0.reset(speed=b0.speed, decrease=xc, side=0)
                b0.c += 1

            else:
                b0.NN += 1
                b0.results = [b0.NN, b0.side, 0, b0.dim_ini, b0.decrease]
                results = results.append(pd.DataFrame(
                    {'NN': [b0.NN], 'SIDE0': [b0.results[1]], 'scelta0': [b0.results[2]],
                     'dim_iniz0': [b0.results[3]], 'handling_time0': [htime00]}))
                b0.speed = random.choice(SPEED_VALUES)
                xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
                b0.reset(speed=b0.speed, decrease=xc, side=0)
                b0.c += 1

        elif b0.NN < N_elementi_da_ispezionare[0] or b0.c < 100:
            conta_speed += 1
            b0.update()
        elif b0.NN >= N_elementi_da_ispezionare[0] and b0.c == 100:
            b0.chosen = [b0.rect.x, b0.rect.y]
            conta_speed += 1
            score = b0.dim * .75
            scoreTOT = scoreTOT + score

            b0.update()

        if b0.NN == sum(N_elementi_da_ispezionare):
            done = True

        screen.fill(WHITE)

        all_sprites_list.draw(screen)
        if scoreTOT < screen_width // 2:
            pygame.draw.rect(screen, RED, pygame.Rect((0, screen_height - 100), (scoreTOT, 100)))
        else:
            pygame.draw.rect(screen, GREEN, pygame.Rect((0, screen_height - 100), (scoreTOT, 100)))
        if scoreTOT > 1:
            scoreTOT -= 0.02
        sy = str(round(scoreTOT))
        text_score = myfont2.render('PUNTEGGIO: %s' % sy, False, (0, 0, 0))

        screen.blit(text_score, (screen_width // 2 - 100, screen_height - 100))

        timer_string = "Tempo rimanente: 05:00"

        text_time = myfont2.render(timer_string, True, BLACK)

        screen.blit(text_time, (screen_width // 2 - 200, 50))

        frame_count += 1

        sec00 = b0.decrease * DIFF_FACT / 60
        text_xc = myfont.render(str(round(sec00)), False, (0, 0, 0))
        screen.blit(text_xc, (screen_width // 2 - 800, screen_height - 700))

        pygame.display.flip()

        clock.tick(60)

    return results


def game(screen, screen_dim, object_sizes, clock, num_block, lista=None, stimuli=None):
    done = False
    myfont = pygame.font.SysFont("monospace", 40)
    myfont2 = pygame.font.SysFont("monospace", 30)
    # results = pd.DataFrame({'NN': [], 'SIDE0': [], 'scelta0': [], 'dim_iniz0': [], 'handling_time0': [],
    #                         'SIDE1': [], 'scelta1': [], 'dim_iniz1': [], 'handling_time1': []})
    results = pd.DataFrame()
    screen_width, screen_height = screen_dim
    # block_list = pygame.sprite.Group()
    block_list = []

    scoreTOT = 0
    all_sprites_list = pygame.sprite.Group()
    frame_count = 0
    frame_rate = 60
    start_time = 30  # 300
    htime = []
    conta = 0
    for i in range(num_block):
        tmp_b = Block(screen_width, screen_height, object_sizes)
        xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
        tmp_b.reset(speed=0, decrease=xc, side=i)
        block_list.append(tmp_b)
        all_sprites_list.add(tmp_b)
        sec = tmp_b.decrease * DIFF_FACT / 60
        htime.append(round(sec))

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
            if event.type == pygame.KEYDOWN:
                check_chosen = False
                for b in block_list:
                    if b.chosen:
                        check_chosen = True
                if event.key == pygame.K_LEFT and not check_chosen:
                    for b in block_list:
                        if b.side == 0:
                            b.chosen = [b.rect.x, b.rect.y]
                            score = b.dim * .75
                            scoreTOT = scoreTOT + score
                        else:
                            b.rejected = [b.rect.x, b.rect.y]
                if event.key == pygame.K_RIGHT and not check_chosen:
                    for b in block_list:
                        if b.side == 1:
                            b.chosen = [b.rect.x, b.rect.y]
                            score = b.dim * .75
                            scoreTOT = scoreTOT + score
                        else:
                            b.rejected = [b.rect.x, b.rect.y]
                if event.key == pygame.K_UP and not check_chosen:
                    for b in block_list:
                        if b.side == 2:
                            b.chosen = [b.rect.x, b.rect.y]
                            score = b.dim * .75
                            scoreTOT = scoreTOT + score
                        else:
                            b.rejected = [b.rect.x, b.rect.y]
        check_c_zero = True
        for b in block_list:
            if b.c != 0:
                check_c_zero = False
        if check_c_zero:
            check_side_chosen = False
            side_chosen = 0
            for i, b in enumerate(block_list):
                if b.chosen:
                    check_side_chosen = True
                    side_chosen = i
            if check_side_chosen:
                for b in block_list:
                    if b.side == side_chosen:
                        if side_chosen == 0 or side_chosen == 1:
                            b.update_circle()
                        else:
                            b.update_line()
                    else:
                        b.c = 0
            else:
                check_results = False
                for b in block_list:
                    if b.results[2] == 1:
                        check_results = True
                if check_results:
                    tmp_results = pd.DataFrame({'NN': [block_list[0].NN]})
                    for i, b in enumerate(block_list):
                        if i < 2:
                            tmp_results = pd.concat(
                                [tmp_results, pd.DataFrame({'SIDE' + str(i): [b.results[1]], 'scelta' + str(i): [b.results[2]],
                                                            'dim_iniz' + str(i): [b.results[3]], 'handling_time' + str(i): [htime[i]]})], axis=1)
                        if i == 2:
                            tmp_results = pd.concat(
                                [tmp_results, pd.DataFrame({'SIDED': [b.results[1]], 'sceltaD': [b.results[2]],
                                                            'dim_inizD': [b.results[3]], 'handling_timeD': [htime[i]]})], axis=1)
                    results = results.append(tmp_results)
                    speed = random.choice(SPEED_VALUES)
                    if num_block > 1:
                        case = lista[conta]
                        exp_stim = stimuli.loc[[case[0]]]
                        num_stim = case[1]
                        image0 = exp_stim.Size1.values.tolist()[0]
                        image1 = exp_stim.Size2.values.tolist()[0]
                        xc0 = exp_stim.decrease1.values.tolist()[0]
                        xc1 = exp_stim.decrease2.values.tolist()[0]
                        if random.choice([1, 2]) == 1:
                            image0D = max(image0, image1) * 0.8
                            xcD = max(xc0, xc1)
                        else:
                            image0D = min(image0, image1)
                            xcD = min(xc0, xc1) * 1.2
                        for b in block_list:
                            if b.side == 0:
                                b.reset_circle(speed=speed, decrease=xc0, side=0, image=int(image0))
                            elif b.side == 1:
                                b.reset_circle(speed=speed, decrease=xc1, side=1, image=int(image1))
                            elif b.side == 2:
                                b.reset_line(speed0=speed, decrease=xcD, side=2, image=int(image0D))
                            b.c += 1
                        conta += 1
                    elif num_block == 1:
                        b = block_list[0]
                        b.speed = speed
                        xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
                        b.reset(speed=b.speed, decrease=xc, side=0)
                        b.c += 1
                else:
                    speed = random.choice(SPEED_VALUES)
                    if num_block > 1:
                        case = lista[conta]
                        exp_stim = stimuli.loc[[case[0]]]
                        num_stim = case[1]
                        image0 = exp_stim.Size1.values.tolist()[0]
                        image1 = exp_stim.Size2.values.tolist()[0]
                        xc0 = exp_stim.decrease1.values.tolist()[0]
                        xc1 = exp_stim.decrease2.values.tolist()[0]
                        if random.choice([1, 2]) == 1:
                            image0D = max(image0, image1) * 0.8
                            xcD = max(xc0, xc1)
                        else:
                            image0D = min(image0, image1)
                            xcD = min(xc0, xc1) * 1.2

                        for b in block_list:
                            b.NN += 1
                            b.results = [b.NN, b.side, 0, b.dim_ini, b.decrease, 0]
                            b.speed = speed
                            if b.side == 0:
                                b.reset_circle(speed=speed, decrease=xc0, side=0, image=int(image0))
                            elif b.side == 1:
                                b.reset_circle(speed=speed, decrease=xc1, side=1, image=int(image1))
                            elif b.side == 2:
                                b.reset_line(speed0=speed, decrease=xcD, side=2, image=int(image0D))
                            b.c += 1
                        conta += 1
                    elif num_block == 1:
                        b = block_list[0]
                        b.results = [b.NN, b.side, 0, b.dim_ini, b.decrease, 0]
                        b.NN += 1
                        b.speed = speed
                        xc = random.randrange(OBJ_COL_min, OBJ_COL_max, OBJ_COL_stp)
                        b.reset(speed=b.speed, decrease=xc, side=0)
                        b.c += 1

                    tmp_results = pd.DataFrame({'NN': [block_list[0].NN]})
                    for i, b in enumerate(block_list):
                        if i < 2:
                            tmp_results = pd.concat(
                                [tmp_results,
                                 pd.DataFrame({'SIDE' + str(i): [b.results[1]], 'scelta' + str(i): [b.results[2]],
                                               'dim_iniz' + str(i): [b.results[3]],
                                               'handling_time' + str(i): [htime[i]]})], axis=1)
                        if i == 2:
                            tmp_results = pd.concat(
                                [tmp_results, pd.DataFrame({'SIDED': [b.results[1]], 'sceltaD': [b.results[2]],
                                                            'dim_inizD': [b.results[3]],
                                                            'handling_timeD': [htime[i]]})], axis=1)
                    results = results.append(tmp_results)
        else:
            for b in block_list:
                if b.side == 0 or b.side == 1:
                    b.update_circle()
                else:
                    b.update_line()

        for b in block_list:
            if b.done:
                done = True

        screen.fill(WHITE)

        all_sprites_list.draw(screen)
        if scoreTOT < screen_width // 2:
            pygame.draw.rect(screen, RED, pygame.Rect((0, screen_height - 100), (scoreTOT, 100)))
        else:
            pygame.draw.rect(screen, GREEN, pygame.Rect((0, screen_height - 100), (scoreTOT, 100)))
        # pygame.draw.rect(screen, RED, pygame.Rect([0, SCREEN_HEIGHT-100], [scoreTOT, 100]))
        if scoreTOT > 1:
            scoreTOT -= 0.02

        sy = str(round(scoreTOT))

        text_score = myfont2.render('PUNTEGGIO: %s' % sy, False, (0, 0, 0))

        screen.blit(text_score, (screen_width // 2 - 100, screen_height - 100))

        total_seconds = start_time - (frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0

        minutes = total_seconds // 60

        seconds = total_seconds % 60

        timer_string = "Tempo rimanente: {0:02}:{1:02}".format(minutes, seconds)

        text_time = myfont2.render(timer_string, True, BLACK)

        screen.blit(text_time, (screen_width // 2 - 200, 50))

        frame_count += 1

        if minutes == 0 and seconds == 0:
            done = True
        for b in block_list:
            sec = b.decrease * DIFF_FACT / 60
            text_xc = myfont.render(str(round(sec)), False, (0, 0, 0))
            if b.side == 0:
                screen.blit(text_xc, (screen_width // 2 - 800, screen_height - 700))
            elif b.side == 1:
                screen.blit(text_xc, (screen_width // 2 + 800, screen_height - 700))
            elif b.side == 2:
                screen.blit(text_xc, (screen_width // 2 - 100, screen_height - 700))

        pygame.display.flip()

        clock.tick(FPS)

    return results


server = '127.0.0.1'


def send_email(text, subj, FROM=FROM, TO=TO):
    msg = MIMEText(text)
    msg['Subject'] = subj
    msg['From'] = FROM
    msg['To'] = ", ".join(TO)
    s = smtplib.SMTP(server)
    s.sendmail(FROM, TO, msg.as_string())
    s.quit()
