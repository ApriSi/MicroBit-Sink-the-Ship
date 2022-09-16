from microbit import *
import radio

radio.on()

loadingValue = 0
def Loading(loadImage):
    global loadingValue
    if loadingValue >= len(loadImage):
        loadingValue = 0
    else:
        display.show(loadImage[loadingValue])
        loadingValue = loadingValue + 1
        sleep(250)

class Cursor:
    def __init__(self, x, y, brightness = 9):
        self.x = x
        self.y = y
        self.brightness = brightness
        
class Shot:
    def __init__(self, x, y, brightness = 5):
        self.x = x
        self.y = y
        self.brightness = brightness

class Player:
    def __init__(self, playerNumber, ships = None):
        self.ships = ships
        self.hits = []
        self.playerNumber = playerNumber
        self.HasChangedRadio = False
        self.Dot = Cursor(2,2)
        self.OpponentShips = ""
        self.HitCounter = 0
        
    def SetShips(self):
        ChangedChannel = False 
        while self.ships == None:         
            if not ChangedChannel:
                display.show(self.playerNumber)
                radio.config(group=self.playerNumber+3)
                ChangedChannel = True  
            
            message = radio.receive()
            if self.ships == None:
                self.ships = message
                message = ""
        
    def Shoot(self):
        for position in self.OpponentShips.split(":"):
            if position != "":
                index = 0
                for ship in range(int(position.split(",")[2])):
                    if self.Dot.x == int(position.split(",")[0]) + index and self.Dot.y == int(position.split(",")[1]):
                        for shot in self.hits:
                            if self.Dot.x == shot.x and self.Dot.y == shot.y:
                                return False
                        return True
                    index += 1
        return False
    
    def Display(self):
        display.clear()
        for hit in self.hits:
            display.set_pixel(hit.x, hit.y, 5)
        display.set_pixel(self.Dot.x, self.Dot.y, self.Dot.brightness)
        
    def Turn(self):
        while True:
            if not self.HasChangedRadio:
                display.scroll(self.playerNumber)
                self.Display()
                self.HasChangedRadio = True
                radio.config(group=self.playerNumber)   
                
            message = radio.receive()
            if message == "a":
                self.Dot.x += 1
                if self.Dot.x > 4:
                    self.Dot.x = 0
                self.Display()
                
            if message == "b":
                self.Dot.y += 1
                if self.Dot.y > 4:
                    self.Dot.y = 0
                self.Display()
                    
            if message == "shake":
                
                if self.Shoot():
                    self.hits.append(Shot(self.Dot.x, self.Dot.y, 6))
                    self.HitCounter += 1
                    display.scroll("!")        
                
                self.HasChangedRadio = False
                message = ""
                break
        

Players = [Player(1), Player(2)]


for player in Players:
    player.SetShips()

Players[0].OpponentShips = str(Players[1].ships)
Players[1].OpponentShips = str(Players[0].ships)

GameRunning = True
while GameRunning:
    for player in Players:        
        player.Turn()  
        if player.HitCounter >= 10:
            display.show(player.playerNumber)
            GameRunning = False
            break
        