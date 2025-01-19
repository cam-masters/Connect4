import pygame

# Setup
pygame.init()
HEIGHT = 700
WIDTH = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Connect 4')
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()
fps = 60

# Game variables
red_positions = []
yellow_positions = []
# 0 - red turn 1- yellow turn
winner = ''
turn_step = 0
selection = -1


def draw_board():
    for i in range(8):
        pygame.draw.line(screen, 'blue',  [100 * i, 0], [100 * i, 600], 8)
    for i in range(7):
        pygame.draw.line(screen, 'blue', [0, 600 - 100 * i], [700, 600 - 100 * i], 8)

    status_text = ['Red to play, choose a column!', 'Yellow to play, choose a column!']
    screen.blit(font.render(status_text[turn_step], True, 'black'), (50, 640))


def draw_counters():
    for red_counter in red_positions:
        x_coord = red_counter[0] * 100 + 50
        y_coord = red_counter[1] * 100 + 50
        pygame.draw.circle(screen, 'red',[x_coord, y_coord], 40, 40)
    for yellow_counter in yellow_positions:
        x_coord = yellow_counter[0] * 100 + 50
        y_coord = yellow_counter[1] * 100 + 50
        pygame.draw.circle(screen, 'yellow',[x_coord, y_coord], 40, 40)


def add_counter(click_coords, color):
    num_in_col = len([x for x in red_positions if x[0] == click_coords[0]]) + len([x for x in yellow_positions if x[0] == click_coords[0]])
    if num_in_col == 6:
        return False
    if color == 'red':
        red_positions.append((click_coords[0], 5 - num_in_col))
    else:
        yellow_positions.append((click_coords[0], 5 - num_in_col))
    return True


def check_winner(positions, color):
    scales = [(1, 0), (0, 1), (1, 1), (-1, 1)] # Scales which way to look i.e. horizontal, vertical, diagonal, other diagonal
    for scale in scales:
        for counter in positions:
            for i in range(1, 4):
                if (counter[0] + scale[0] * i, counter[1] + scale[1] * i) in positions:
                    if i == 3:
                        return color
                else:
                    break

    return ''


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))

run = True
game_over = False
while run:
    timer.tick(fps)
    screen.fill('light gray')
    draw_board()
    draw_counters()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step == 0: # red turn
                if add_counter(click_coords, 'red'):
                    turn_step = 1
                    winner = check_winner(red_positions, 'red')
            elif turn_step == 1: # yellow turn
                if add_counter(click_coords, 'yellow'):
                    turn_step = 0
                    winner = check_winner(yellow_positions, 'yellow')
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                red_positions = []
                yellow_positions = []
                turn_step = 0


    if winner != '':
        game_over = True
        draw_game_over()

    
    pygame.display.flip()
pygame.quit()
