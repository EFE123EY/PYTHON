import pygame
import random
import cv2
import mediapipe
import numpy

pygame.init()

#WEBCAM
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

#font
text_font = pygame.font.Font("IndieFlower-Regular.ttf", 48)


#SCREEN
width,height = 1280,720
screen = pygame.display.set_mode((width,height))

#müzik
pygame.mixer.music.load("Juhani Junkala [Chiptune Adventures] 4. Stage Select.wav")
pygame.mixer.music.play(-1,0,0)
beat=pygame.mixer.Sound("dead.wav")

#fps
fps=30
clock=pygame.time.Clock()

#Karakterler
character = pygame.image.load("roket.png")
character = pygame.transform.scale(character,(50,50))
character_coor = character.get_rect()

meteor=pygame.image.load("meteor.png")
meteor = pygame.transform.scale(meteor,(50,60))
meteor_coor = meteor.get_rect()
meteor_coor.center = (250, 150)

x,y = 500,300
score=90
game_time = 0
game_time_text = None

#hand
hand_model = mediapipe.solutions.hands

open= True
with hand_model.Hands (min_tracking_confidence=0.5,min_detection_confidence=0.5) as hand:

    while open:
        for activity in pygame.event.get():
            if activity.type == pygame.QUIT:
                open = False
        game_time += 1
        game_time_text = "Süre: {}".format(str(game_time // 15).rjust(2))


        control, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hand.process(rgb)
        if result.multi_hand_landmarks:
            for hand_landmark in result.multi_hand_landmarks:
                for coor in hand_landmark.landmark:
                    mark = hand_landmark.landmark[8]
                    x = int(mark.x * width)
                    y = int(mark.y * height)
        character_coor.center = (x, y)
        rgb = numpy.rot90(rgb)
        video_screen = pygame.surfarray.make_surface(rgb).convert()
        video_screen = pygame.transform.flip(video_screen, True, False)
        screen.blit(video_screen, (0, 0))
        screen.blit(meteor, meteor_coor)
        screen.blit(character, character_coor)
        text = text_font.render(f"Skor {score}", True, (255, 255, 255))
        text_coor = text.get_rect()
        text_coor.topleft = (20, 20)
        pygame.draw.line(screen, (0, 0, 255), (0, 120), (width, 120), 3)
        screen.blit(text, text_coor)
        screen.blit(text_font.render(game_time_text, True, (255, 255, 255)), (1000, 20))
        if character_coor.colliderect(meteor_coor):
            beat.play()
            meteor_coor.x = random.randint(0, width - 50)
            meteor_coor.y = random.randint(121, height - 32)
            score += 5

        if score >= 100:
            game_win_text = text_font.render("Kazandın!", True, (0, 255, 0))
            screen.blit(game_win_text, (width // 2 - 100, height // 2))
            pygame.display.update()
            pygame.time.wait(5000)
            open = False

        if game_time >= 900:
            game_lose_text = text_font.render("Kaybettin!", True, (255, 0, 0))
            screen.blit(game_lose_text, (width // 2 - 100, height // 2))
            pygame.display.update()
            pygame.time.wait(5000)
            open = False

        pygame.display.update()
        clock.tick(fps)

pygame.quit()








