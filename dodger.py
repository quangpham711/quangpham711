import pygame, random, sys, os
from pygame.locals import *
from background_effects import background_with_stars

WINDOWWIDTH = 1200
WINDOWHEIGHT = 800
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 20
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 30
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 3
ADDNEWBADDIERATE = 5
PLAYERMOVERATE = 20
GRAVITY_FACTOR = 0.0005  # Điều chỉnh mức độ hút
HIGH_SCORES_FILE = "high_scores.txt"  # File lưu điểm cao

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Thêm hàm lưu và tải điểm cao
def save_high_score(score):
    if not os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, "w") as f:
            f.write(str(score))
    else:
        with open(HIGH_SCORES_FILE, "r") as f:
            current_high_score = int(f.read().strip())
        if score > current_high_score:
            with open(HIGH_SCORES_FILE, "w") as f:
                f.write(str(score))

def load_high_score():
    if os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, "r") as f:
            return int(f.read().strip())
    return 0

# Thêm hàm menu chính

def main_menu(windowSurface, font):
    
    while True:
        background_with_stars(windowSurface, num_stars=100)
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText("Dodger", font, windowSurface, WINDOWWIDTH // 2 - 100, 150)
        drawText("1. Start Game", font, windowSurface, WINDOWWIDTH // 2 - 150, 300)
        drawText("2. High Scores", font, windowSurface, WINDOWWIDTH // 2 - 150, 400)
        drawText("3. Quit Game", font, windowSurface, WINDOWWIDTH // 2 - 150, 500)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_1:
                    return "start"
                elif event.key == K_2:
                    return "high_scores"
                elif event.key == K_3:
                    terminate()


# Thêm hàm hiển thị điểm cao
def show_high_scores(windowSurface, font):
    high_score = load_high_score()
    while True:
        windowSurface.fill(BACKGROUNDCOLOR)
        drawText("High Scores", font, windowSurface, WINDOWWIDTH // 2 - 100, 150)
        drawText(f"Highest Score: {high_score}", font, windowSurface, WINDOWWIDTH // 2 - 150, 300)
        drawText("Press ESC to return", font, windowSurface, WINDOWWIDTH // 2 - 150, 400)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Dodger')

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.WAV')
pygame.mixer.music.load('background.WAV')

# set up images
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')
backgroundImage = pygame.image.load('background.png')

# resize the background to fit the window size
backgroundImage = pygame.transform.scale(backgroundImage, (WINDOWWIDTH, WINDOWHEIGHT))
# Hiển thị hiệu ứng nền và menu bắt đầu
background_with_stars(windowSurface, num_stars=100)

# Hiển thị menu chính
while True:
    choice = main_menu(windowSurface, font)
    if choice == "start":
        topScore = load_high_score()  # Tải điểm cao nhất
        break
    elif choice == "high_scores":
        show_high_scores(windowSurface, font)

#Set up chuột tàn hình
pygame.mouse.set_visible(False)

# Game loop chính

while True:
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True:  # game loop
        score += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key in (K_LEFT, ord('a')):
                    moveRight = False
                    moveLeft = True
                if event.key in (K_RIGHT, ord('d')):
                    moveLeft = False
                    moveRight = True
                if event.key in (K_UP, ord('w')):
                    moveDown = False
                    moveUp = True
                if event.key in (K_DOWN, ord('s')):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()
                if event.key in (K_LEFT, ord('a')):
                    moveLeft = False
                if event.key in (K_RIGHT, ord('d')):
                    moveRight = False
                if event.key in (K_UP, ord('w')):
                    moveUp = False
                if event.key in (K_DOWN, ord('s')):
                    moveDown = False
            if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
                playerRect.move_ip(event.pos[0] - playerRect.centerx, event.pos[1] - playerRect.centery)
         # Cập nhật vị trí của nhân vật dựa trên các phím di chuyển
          

        if moveLeft:
            playerRect.x -= PLAYERMOVERATE
        if moveRight:
            playerRect.x += PLAYERMOVERATE
        if moveUp:
            playerRect.y -= PLAYERMOVERATE
        if moveDown:
            playerRect.y += PLAYERMOVERATE

        # Giới hạn di chuyển nhân vật trong cửa sổ
        if playerRect.left < 0:
            playerRect.left = 0
        if playerRect.right > WINDOWWIDTH:
            playerRect.right = WINDOWWIDTH
        if playerRect.top < 0:
            playerRect.top = 0
        if playerRect.bottom > WINDOWHEIGHT:
            playerRect.bottom = WINDOWHEIGHT

         # Add new baddies at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)

            # Random góc xuất hiện
            startCorner = random.choice(['top_left', 'top_right', 'bottom_left', 'bottom_right'])

            if startCorner == 'top_left':
                startX, startY = 0, 0
                speedX, speedY = random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
            elif startCorner == 'top_right':
                startX, startY = WINDOWWIDTH, 0
                speedX, speedY = -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
            elif startCorner == 'bottom_left':
                startX, startY = 0, WINDOWHEIGHT
                speedX, speedY = random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)
            elif startCorner == 'bottom_right':
                startX, startY = WINDOWWIDTH, WINDOWHEIGHT
                speedX, speedY = -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED), -random.randint(BADDIEMINSPEED, BADDIEMAXSPEED)

            # Tạo baddie mới
            newBaddie = {
                'rect': pygame.Rect(startX, startY, baddieSize, baddieSize),
                'speedX': speedX,
                'speedY': speedY,
                'surface': pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
            }
            baddies.append(newBaddie)

        # Cập nhật vị trí baddies với lực hút
        for b in baddies:
            # Tính toán lực hút hướng về player
            if not reverseCheat and not slowCheat:
                dx = playerRect.centerx - b['rect'].centerx  # Khoảng cách x đến player
                dy = playerRect.centery - b['rect'].centery  # Khoảng cách y đến player

                # Điều chỉnh tốc độ theo hướng player
                b['speedX'] += dx * GRAVITY_FACTOR
                b['speedY'] += dy * GRAVITY_FACTOR

                # Di chuyển baddie
                b['rect'].move_ip(b['speedX'], b['speedY'])

            elif reverseCheat:
                b['rect'].move_ip(-b['speedX'], -b['speedY'])

            elif slowCheat:
                b['rect'].move_ip(b['speedX'] * 0.5, b['speedY'] * 0.5)


        # Xóa các baddie nếu ra ngoài cửa sổ
        for b in baddies[:]:
            if (b['rect'].top > WINDOWHEIGHT or b['rect'].bottom < 0 or
                b['rect'].left > WINDOWWIDTH or b['rect'].right < 0):
                baddies.remove(b)


        # Draw the game world on the window.
        windowSurface.blit(backgroundImage, (0, 0))  # Sử dụng ảnh nền

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the player's rectangle
        windowSurface.blit(playerImage, playerRect)

        # Draw each baddie
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                topScore = score
                save_high_score(topScore)  # Lưu điểm cao
            break

        mainClock.tick(FPS)

    # Game over logic
    pygame.mixer.music.stop()
    gameOverSound.play()
    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
    gameOverSound.stop()