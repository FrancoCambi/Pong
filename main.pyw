import pygame, os, random
pygame.font.init()
pygame.display.init()

# Screen const

HEIGHT = 900
WIDTH = 1200
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60

# LOAD IMAGES

PALETA_IMAGE = pygame.image.load(os.path.join('Images', 'Paleta.png'))
BALL_IMAGE = pygame.image.load(os.path.join('Images', 'Ball.png'))

# Colors const

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Use Const

PALETA_WIDTH = 110
PALETA_HEIGHT = 120

PALETA_IZQ = pygame.transform.scale(PALETA_IMAGE, (PALETA_WIDTH, PALETA_HEIGHT))
PALETA_DER = pygame.transform.scale(PALETA_IMAGE, (PALETA_WIDTH, PALETA_HEIGHT))
PALETA_IZQ_DOWN = pygame.transform.rotate(pygame.transform.scale(PALETA_IMAGE, (PALETA_WIDTH, PALETA_HEIGHT)), 180)
PALETA_DER_DOWN = pygame.transform.rotate(pygame.transform.scale(PALETA_IMAGE, (PALETA_WIDTH, PALETA_HEIGHT)), 180)

BALL_WIDTH = 30
BALL_HEIGHT = 30

BALL = pygame.transform.scale(BALL_IMAGE, (BALL_WIDTH, BALL_HEIGHT))

# Functions

def draw_window(izq, der, PALETA_IZQ, PALETA_DER, saque, ball, izq_score, der_score):
    score_text_izq = SCORE_FONT.render("Score: " + str(izq_score // 7), 1, WHITE)
    score_text_der = SCORE_FONT.render("Score: " + str(der_score // 7) , 1, WHITE)
    if saque:
        WIN.fill(BLUE)
        WIN.blit(score_text_izq, (10, 10))
        WIN.blit(score_text_der, (WIDTH - score_text_der.get_width() - 10, 10))
        WIN.blit(PALETA_IZQ, (izq.x, izq.y))
        WIN.blit(PALETA_DER, (der.x, der.y))
        WIN.blit(BALL, (ball.x, ball.y))
    else:
        WIN.fill(BLUE)
        WIN.blit(score_text_izq, (10, 10))
        WIN.blit(score_text_der, (WIDTH - score_text_der.get_width() - 10, 10))
        WIN.blit(PALETA_IZQ, (izq.x, izq.y))
        WIN.blit(PALETA_DER, (der.x, der.y))
    pygame.display.update()

def handle_movement(keys_pressed, izq, der, vel):
    if keys_pressed[pygame.K_w] and izq.y - vel > 0:
        izq.y -= vel
    if keys_pressed[pygame.K_s] and izq.y + vel + PALETA_HEIGHT < HEIGHT:
        izq.y += vel
    if keys_pressed[pygame.K_UP] and der.y - vel > 0:
        der.y -= vel
    if keys_pressed[pygame.K_DOWN] and der.y + vel + PALETA_HEIGHT < HEIGHT:
        der.y += vel

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


# Main function

def main():

    izq = pygame.Rect(0, HEIGHT // 2 - PALETA_HEIGHT + 40, PALETA_WIDTH, PALETA_HEIGHT)
    der = pygame.Rect(WIDTH - PALETA_WIDTH, HEIGHT // 2 - PALETA_HEIGHT + 40, PALETA_WIDTH, PALETA_HEIGHT)
    ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_WIDTH, BALL_HEIGHT)


    saque = False
    run = True
    clock = pygame.time.Clock()

    ball_vel_x = 7 * random.choice((1, -1))
    ball_vel_y = 7 * random.choice((1, -1))
    vel = 5.5

    izq_score = 0
    der_score = 0

    winner_text = ""

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    saque = True

        if izq_score >= 70:
            winner_text = "Left Player Wins!"
            draw_winner(winner_text)
            break
        if der_score >= 70:
            winner_text = "Right Player Wins!"
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, izq, der, vel)
        if keys_pressed[pygame.K_DOWN] and keys_pressed[pygame.K_s]: # Ambas para abajo
            draw_window(izq, der, PALETA_IZQ_DOWN, PALETA_DER_DOWN, saque, ball, izq_score, der_score)
        elif keys_pressed[pygame.K_s]: # Izquierda para abajo
            draw_window(izq, der, PALETA_IZQ_DOWN, PALETA_DER, saque, ball, izq_score, der_score)
        elif keys_pressed[pygame.K_DOWN]: # Derecha para abajo
            draw_window(izq, der, PALETA_IZQ, PALETA_DER_DOWN, saque, ball, izq_score, der_score) 
        else: # Ninguna abajo
            draw_window(izq, der, PALETA_IZQ, PALETA_DER, saque, ball, izq_score, der_score)

        if saque: # Ball_Handle
            
            if ball_vel_x > 0:
                ball_vel_x += (1/500)
            if ball_vel_y > 0:
                ball_vel_y += (1/500)

            vel += (1/900)
            
            ball.x += ball_vel_x
            ball.y += ball_vel_y

            if ball.x + ball_vel_x + ball.width > WIDTH:
                izq_score += 1
            elif ball.x + ball_vel_x <= 0:
                der_score += 1

            if ball.y + ball_vel_y + ball.width > HEIGHT or ball.y + ball_vel_y <= 0: # Rebota pared
                ball_vel_y *= -1
            elif ball.x < 0 - ball.width: # Punto derecha
                der_score += 1
                ball.x = WIDTH // 2
                ball.y = HEIGHT // 2
                ball_vel_x *= random.choice((1, -1))
                ball_vel_y *= random.choice((1, -1))
                saque = False
            elif ball.x > WIDTH + ball.width: # Punto izquierda
                izq_score += 1
                ball.x = WIDTH // 2
                ball.y = HEIGHT // 2
                ball_vel_x *= random.choice((1, -1))
                ball_vel_y *= random.choice((1, -1))
                saque = False
            else:
                if ball.x + ball_vel_x > der.x and der.y + der.height // 2 < ball.y < der.y + der.height: # Rebota contra der abajo
                    ball_vel_y *= -1
                    ball_vel_x *= -1
                elif ball.x + ball_vel_x > der.x and der.y < ball.y < der.y + der.height: # Rebota contra der arriba
                    ball_vel_x *= -1
                elif ball.x + ball_vel_x < izq.x + izq.width - 30 and izq.y < ball.y < izq.y + izq.height: # Rebota contra izq arriba
                    ball_vel_x *= -1
                elif ball.x + ball_vel_x < izq.x + izq.width - 30 and izq.y + izq.height // 2 < ball.y < izq.y + izq.height: # Rebota contra izq abajo
                    ball_vel_y *= -1
                    ball_vel_x *= -1

    main()


if __name__ == "__main__":
    main()



