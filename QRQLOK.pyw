"""
Clock Mathy bits lifted from somewhere;
Dig out and attribute later
"""

import qrcode,pygame,time,math
from datetime import datetime

pygame.init()

BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (0,128,0)
BLUE  = (0,0,255)
GREY  = (128,128,128)
WHITE = (255,255,255)

BG = WHITE

BOX = 15
EDGE  = 51
BORDER = 1
SLEEP = 1

WIDTH = EDGE * BOX
HEIGHT = EDGE * BOX

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('QRQLOK')
screen.fill(BG)

clock = pygame.time.Clock()

CLOCK_R  = int(WIDTH / 2) # clock radius
HOUR_R   = int(CLOCK_R * 7 / 10) # hour hand length
MINUTE_R = int(CLOCK_R * 9 / 10) # minute hand length
SECOND_R = CLOCK_R # second hand length
HOUR_STROKE = BOX*3
MINUTE_STROKE = BOX*2
SECOND_STROKE = BOX*1

HOURS_IN_CLOCK = 12
MINUTES_IN_HOUR = 60
SECONDS_IN_MINUTE = 60

CENTER = (int(WIDTH/2),int(HEIGHT/2))
HourX = WIDTH-(EDGE*2)
HourY = HEIGHT-(EDGE*2)
MinX = WIDTH-EDGE/2
MinY = int(HEIGHT/2)

def circle_point(center, radius, theta):
    """Calculates the location of a point of a circle given the circle's
       center and radius as well as the point's angle from the xx' axis"""

    return (center[0] + radius * math.cos(theta),
            center[1] + radius * math.sin(theta))

def line_at_angle(screen, center, radius, theta, color, width):
    """Draws a line from a center towards an angle. The angle is given in
       radians."""
    point = circle_point(center, radius, theta)
    pygame.draw.line(screen, color, center, point, width)

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
    img = qr.make_image(fill_color=GREY, back_color='white')

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
        (HOUR_R, hour_theta, BLUE, HOUR_STROKE),
        (MINUTE_R, minute_theta, GREEN, MINUTE_STROKE),
        (SECOND_R, second_theta, RED, SECOND_STROKE),
    ):
        line_at_angle(screen, CENTER, radius, theta, color, stroke)

    pygame.display.flip()

    time.sleep(SLEEP)

