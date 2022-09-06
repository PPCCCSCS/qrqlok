import qrcode,pygame
from datetime import datetime

pygame.init()

BG = (255,255,255)
(WIDTH,HEIGHT) = (650,650)

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('QRCODE CLOCK')
screen.fill(BG)

clock = pygame.time.Clock()

pygame.display.flip()

CENTER = (int(WIDTH/2),int(HEIGHT/2))
HourX = WIDTH-150
HourY = HEIGHT-150
MinX = WIDTH-50
MinY = int(HEIGHT/2)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    timeNow = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    timeHour = datetime.now().strftime("%H")
    timeMin = datetime.now().strftime("%M")
    timeSec = datetime.now().strftime("%S")

    print("Time = ", timeHour,":",timeMin,":",timeSec)
    qr = qrcode.QRCode(version=10, box_size=10,error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(timeNow)
    qr.make(fit=True)
    img = qr.make_image(fill_color='red', back_color='white')

    img.save('time.png')

    # Draw the QR Code
    QRImg = pygame.image.load('time.png')
    screen.blit(QRImg,(0,0))
    
    ### TRIGONOMETRY GOES HERE

    # Draw the clock hands
    pygame.draw.line(screen,'black',CENTER,(HourX,HourY),width=50)
    pygame.draw.line(screen,'black',CENTER,(MinX,MinY),  width=20)
    pygame.display.flip()

    clock.tick(1)

