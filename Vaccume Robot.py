import random

class VacuumRobot:
    def __init__(self, room, battery=100):
        self.room = room
        self.battery = battery
        self.obstacle = 'O'  # Walls and things the robot can't pass
        self.dirt = 'D'
        self.clean = ' '
        self.chargingStation = 'C'
        self.door = 'P'
        self.position = self.findDoor()  # The robot starts at the door
        self.steps = 0 # keep track of how many steps it has taken and manage battery

    def goClean(self):
        # the robot keeps cleaning until the room is spotless.
        while not self.roomCleaned(): # Keep going until the room is clean
            self.move() # Move and clean
        print("Room cleaned, going to sleep...") # Job's done!

    def findDoor(self):
        #Find the door position in the room.
        for i, row in enumerate(self.room): # Go through each row
            for j, cell in enumerate(row): # Go through each spot in the row
                if cell == self.door: # If it's the door, remember its position
                    return (i, j)
        return (0, 0)  # If it can't find the door, just start in the top left corner.

    def move(self):
        # this is how the robot moves around.
        if self.battery <= 10: # If the battery is low, go charge!
            print("Battery low! Returning to charging station...")
            self.goToChargingStation()
            return # Stop moving for now

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
        random.shuffle(directions)  # Mix up the directions so it moves randomly

        for x, y in directions: # Try each direction
            newX = self.position[0] + x # figure out the new spot
            newY = self.position[1] + y

            # check if the new spot is okay (inside the room and not a wall)
            if 0 <= newX < len(self.room) and 0 <= newY < len(self.room[0]) and self.room[newX][newY] != self.obstacle:
                self.position = (newX, newY) # Move to the new spot
                if self.steps == 5: #after 5 steps, lose some battery.
                    self.battery -= 1
                    self.steps = 0 # reset the steps
                else:
                    self.steps += 1 #add a step.
                print(f"Moved to {self.position}, Battery: {self.battery}")

                # If there's dirt, clean it!
                if self.room[newX][newY] == self.dirt:
                    self.cleanDirt(newX, newY)
                return  # only move one spot at a time

    def goToChargingStation(self):
        # this is when the robot needs to go back to the charger.
        chargingStationPos = self.findChargingStation() # Find where the charger is
        if chargingStationPos: # if it found the charger
            print(f"Going to charging station at {chargingStationPos}...")
            self.position = chargingStationPos # Go to the charger
            self.battery = 100  # Fill up the battery!
            print("Recharged! Battery: 100%")
        else: # if it can't find the charger
            print("Charging station not found!")

    def findChargingStation(self):
        """Find the charging station position in the room."""
        # This looks for the charger in the room.
        for i, row in enumerate(self.room): # Go through each row
            for j, cell in enumerate(row): # Go through each spot in the row
                if cell == self.chargingStation: # If it's the charger, remember its position
                    return (i, j)
        return None # If it can't find the charger, say it's not there

    def cleanDirt(self, x, y):
        """Clean dirt at the given position."""
        # This is how the robot cleans up dirt.
        self.room[x][y] = self.clean # Change the dirt to clean space
        print(f"Cleaned dirt at ({x}, {y})")

    def roomCleaned(self):
        """Check if the room is fully cleaned."""
        # This checks if there's any dirt left in the room.
        for row in self.room: # Look at each row
            if self.dirt in row: # If there's any dirt, the room isn't clean
                return False
        return True # If no dirt is found, the room is clean!

# Example room layout
room = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ['O', ' ', ' ', 'D', ' ', ' ', ' ', ' ', ' ', 'O'],
    ['O', ' ', 'O', 'O', 'O', ' ', 'O', 'O', ' ', 'O'],
    ['O', ' ', ' ', 'C', ' ', ' ', ' ', 'D', ' ', 'O'],
    ['O', 'P', ' ', 'D', ' ', ' ', 'O', ' ', ' ', 'O'],
    ['O', ' ', 'O', 'O', 'O', ' ', 'O', 'O', ' ', 'O'],
    ['O', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'],
    ['O', ' ', 'O', 'O', 'O', 'O', 'O', 'O', ' ', 'O'],
    ['O', ' ', ' ', 'D', ' ', ' ', ' ', ' ', ' ', 'O'],
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O']
]

# Create a robot and let it clean!
robot = VacuumRobot(room)
robot.goClean()