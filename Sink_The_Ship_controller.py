from microbit import *
import radio

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ship:
    def __init__(self, length, position = Vector2(0,0), brightness = 9):
        self.length = length
        self.position = position
        self.brightness = brightness
        
    def display(self):
        for length in range(self.length):
            display.set_pixel(length+self.position.x, self.position.y, self.brightness)


PLAYER_NAME = 2
myShips = []
currentShipLength = 1

radio.config(group=23)
radio.on()

invertedMovementY = False
invertedMovementX = False

gameStarted = False
canPlace = True
hasChangedRadio = False
hasTransferedPositions = False
hasShot = False

radio.send(str(PLAYER_NAME))
display.scroll(PLAYER_NAME)
def TransferShipPositions():
    positions = ""
    for ship in myShips:
        positions += "{0},{1},{2}:".format(ship.position.x, ship.position.y, ship.length)
    radio.send(positions)
    print("Positions sent")

while True:
    if not gameStarted:
        for ship in myShips:
            ship.display()
        currentShip = Ship(currentShipLength)
        currentShip.display()

        while button_b.is_pressed():
            if button_a.was_pressed():
                for myShipLength in range(currentShip.length):
                    for ship in myShips:
                        for shipLength in range(ship.length):
                            if ship.position.x == currentShip.position.x+myShipLength and ship.position.y == currentShip.position.y:
                                canPlace = False
                                
                if canPlace:
                    myShips.append(Ship(currentShip.length, Vector2(currentShip.position.x, currentShip.position.y), 5+currentShipLength))
                    currentShip.position.x = 0
                    currentShip.position.y = 0
                    currentShipLength += 1
                    if currentShipLength > 4:
                        gameStarted = True
                        display.clear()
                canPlace = True
        if button_a.was_pressed():
            display.clear()
            if not invertedMovementY:
                currentShip.position.y += 1
                if(currentShip.position.y > 3):
                    invertedMovementY = True
            else:
                if currentShip.position.y < 1:
                    invertedMovementY = False
                else:
                    currentShip.position.y -= 1
                
        if button_b.was_pressed():
            display.clear()
            if not invertedMovementX:
                if(currentShip.position.x+currentShip.length > 4):
                    invertedMovementX = True
                else:
                    currentShip.position.x += 1
            else:
                if currentShip.position.x < 1:
                    invertedMovementX = False
                else:
                    currentShip.position.x -= 1
    else:
        if not hasChangedRadio:
            radioGroup = PLAYER_NAME+3
            radio.config(group=radioGroup)
            print("Changed Radio to {0}".format(radioGroup))
            
        message = radio.receive()
        if not hasTransferedPositions and message == None:
            print(message)
            TransferShipPositions()
            hasTransferedPositions = True
            
        if not hasChangedRadio and hasTransferedPositions:
            radio.config(group=PLAYER_NAME)
            print("Changed Radio to {0}".format(PLAYER_NAME))
            hasChangedRadio = True

            
        for ship in myShips:
            ship.display()
            
        while button_b.is_pressed():
            if button_a.was_pressed():
                radio.send('shake')

        if button_a.was_pressed():
            radio.send('a')
        if button_b.was_pressed():
            radio.send('b')