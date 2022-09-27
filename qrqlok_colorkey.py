"""
Clock Mathy bits lifted from somewhere;
Dig out and attribute later
"""

import qrcode,pygame,time,math
from datetime import datetime

pygame.init()

BLACK   = (0,0,0)
RED     = (255,0,0)
GREEN   = (0,128,0)
LIME    = (0,255,0)
BLUE    = (0,0,255)
GREY    = (128,128,128)
WHITE   = (255,255,255)
FUCHSIA = (255,0,255)

BG = WHITE

BOX = 8
EDGE  = 51
BORDER = 1
SLEEP = 1

WIDTH = EDGE * BOX
HEIGHT = EDGE * BOX

screen = pygame.display.set_mode((WIDTH,HEIGHT))
hands = screen.copy()
hands.set_colorkey(FUCHSIA)
hands = pygame.transform.scale(hands,(EDGE,EDGE))

pygame.display.set_caption('QRQLOK')
screen.fill(BG)
hands.fill(FUCHSIA)

clock = pygame.time.Clock()

#CLOCK_R  = int(WIDTH / 2) # clock radius
CLOCK_R  = int(EDGE / 2) # clock radius
HOUR_R   = int(CLOCK_R * 7 / 10) # hour hand length
MINUTE_R = int(CLOCK_R * 9 / 10) # minute hand length
SECOND_R = int(CLOCK_R * 95 / 100) # second hand length
#HOUR_STROKE = BOX*3
#MINUTE_STROKE = BOX*2
#SECOND_STROKE = BOX
HOUR_STROKE = 3
MINUTE_STROKE = 2
SECOND_STROKE = 1

HOURS_IN_CLOCK = 12
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60

CENTER = (int(EDGE/2),int(EDGE/2))
HourX = WIDTH-(EDGE*2)
HourY = HEIGHT-(EDGE*2)
MinX = WIDTH-EDGE/2
MinY = int(HEIGHT/2)

def circle_point(center, radius, theta):
    """Calculates the location of a point of a circle given the circle's
       center and radius as well as the point's angle from the xx' axis"""

    return (center[0] + radius * math.cos(theta),
            center[1] + radius * math.sin(theta))

## ht Rabbid76 @ https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame
def draw_line_round_corners_polygon(surf, p1, p2, c, w):
    p1v = pygame.math.Vector2(p1)
    p2v = pygame.math.Vector2(p2)
    lv = (p2v - p1v).normalize()
    lnv = pygame.math.Vector2(-lv.y, lv.x) * w // 2
    pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
    pygame.draw.polygon(surf, c, pts)
    pygame.draw.circle(surf, c, p1, round(w / 2))
    pygame.draw.circle(surf, c, p2, round(w / 2))

def line_at_angle(screen, center, radius, theta, color, width):
    """Draws a line from a center towards an angle. The angle is given in
       radians."""
    point = circle_point(center, radius, theta)
    #pygame.draw.line(screen, color, center, point, width)
    draw_line_round_corners_polygon(hands,center,point,color,width)

def get_angle(unit, total):
    """Calculates the angle, in radians, corresponding to a portion of the clock
       counting using the given units up to a given total and starting from 12
       o'clock and moving clock-wise."""
    return 2 * math.pi * unit / total - math.pi / 2

running = True

timeInit = datetime.now()

# Spin until the second flips, hopefully better sync
while datetime.now().second == timeInit.second:
    pass

while running:
    
    timeNow = datetime.now()
    timeFormatted = timeNow.strftime("%H:%M:%S")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # print("Time = ", timeHour,":",timeMin,":",timeSec)
    qr = qrcode.QRCode(version=8,
                       box_size=BOX,
                       error_correction=qrcode.constants.ERROR_CORRECT_H,
                       border=BORDER)
    qr.add_data(timeFormatted)
    qr.make(fit=True)

    if int(timeNow.hour) == 10 and int(timeNow.minute <= 15):
        FILL = LIME
    else:
        FILL = BLACK
    
    img = qr.make_image(fill_color=FILL, back_color='white')

    # saving the QR Code every tick is a bad hack. FIX THIS
    img.save('time.png')

    # Draw the QR Code
    QRImg = pygame.image.load('time.png')
    screen.blit(QRImg,(0,0))
    
    ### TRIGONOMETRY GOES HERE
        # draw hands
    hour_theta = get_angle(timeNow.hour + 1.0 * timeNow.minute / MINUTES_IN_HOUR, HOURS_IN_CLOCK)
    minute_theta = get_angle(timeNow.minute, MINUTES_IN_HOUR)
    second_theta = get_angle(timeNow.second, SECONDS_IN_MINUTE)

    for (radius, theta, color, stroke) in (
        (HOUR_R, hour_theta, RED, HOUR_STROKE),
        (MINUTE_R, minute_theta, GREEN, MINUTE_STROKE),
        (SECOND_R, second_theta, BLUE, SECOND_STROKE),
        ):
        line_at_angle(hands,CENTER,radius,theta,color,stroke)

    hands = pygame.transform.scale(hands,(WIDTH,HEIGHT))
    screen.blit(hands,(0,0))

    pygame.display.flip()

    time.sleep(SLEEP)

