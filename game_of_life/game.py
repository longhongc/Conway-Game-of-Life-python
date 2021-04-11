import numpy as np
import json
import time
import os
from collections import defaultdict

directory = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(directory, "config.json")

class Game():
    # game map symbols 
    vwall="-"
    hwall="|"
    corner="+"
    
    def __init__(self):
        with open(config_file) as f:
            config = json.load(f)
        empty_world = np.zeros(config["world_size"])
        self.current_world = empty_world
        self.rows = empty_world.shape[0]
        self.cols = empty_world.shape[1]
        self.step_time = config["step_time"]
        self.init_state = config["init_state"] 

    def choose_init_state(self):
        print("Choose a init shape:")
        for shape in self.init_state:
            print(shape)
            init_helper = np.zeros([5,5]) 
            for rel_pos in self.init_state[shape]["points"]:
                pos = (2+rel_pos[0], 2+rel_pos[1])
                init_helper[pos]=1
            self.display(init_helper)
        print("Enter a shape: ", end="")
        init_state = input()
            
        center = [int(self.rows/2), int(self.cols/2)]
        for rel_pos in self.init_state[init_state]["points"]:
            pos = (center[0]+rel_pos[0], center[1]+rel_pos[1])
            self.current_world[pos]=1
     

    def display(self, world):
        vwalls = Game.corner + Game.vwall * world.shape[1] + Game.corner  
        total_map = vwalls + "\n"
        for row in world:
            layer = ""
            for col in row:
                if col == 1:
                    layer += "*"
                else:
                    layer += " "
            total_map += Game.hwall + layer + Game.hwall + "\n"
        total_map += vwalls  
        print(total_map)

    def next(self, world):
        def find_neighbors(point):
            rel_pos=[(-1,-1), (-1,0), (-1,1),
                     ( 0,-1),         ( 0,1),
                     ( 1,-1), ( 1,0), ( 1,1)]
            neighbors = []
            for pos in rel_pos:
                neighbor = np.array(pos)+np.array(point)
                neighbors.append(tuple(neighbor.tolist()))
            return neighbors

        # count alive neighbors for possible candidates(alive points and its neighbors) 
        alive_neighbors = defaultdict(int)
        alives = np.where(world==1)
        alives = list(zip(alives[0], alives[1]))
        for point in alives:
            neighbors = find_neighbors(point)
            for neighbor in neighbors:
                if neighbor[0] < 0 or \
                   neighbor[0] >= self.rows or \
                   neighbor[1] < 0 or \
                   neighbor[1] >= self.cols:
                   continue
                alive_neighbors[neighbor]+=1

        # apply survival rules to candidates
        next_world = world.copy()
        for point in alive_neighbors:
            if alive_neighbors[point] <= 1 or alive_neighbors[point] >= 4:
                next_world[point]=0
            elif alive_neighbors[point] == 3:
                next_world[point]=1
        return next_world

    def start(self):
        self.choose_init_state()
        count =  0
        while True:
            try:
                print("Day", count)
                self.display(self.current_world)
                next_world = self.next(self.current_world)
                # game stops when the world doesn't change and when all points died
                if np.all(next_world==self.current_world) or \
                   (not np.any(next_world)):
                    break
                self.current_world = next_world
                count+=1
                time.sleep(self.step_time)
            except KeyboardInterrupt:
                break
        print()
        print("Thank you for playing.")

            

if __name__ == "__main__":
    myGame = Game()
    myGame.start()

