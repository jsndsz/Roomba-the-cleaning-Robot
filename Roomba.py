''' 
The program contains 2 classes. One is the Environment class, which creates the 
environment. This can be done by, either manually entering all the coordinates of dirt patterns and agent start 
position or by letting the system randomize these vaiables. The user also has a choice on the size of the 
environment, the maximum size of the pile of dirt, the maximum number of piles, the total number of percepts and 
the total number of different setups which need to be run.

The second class is the reflex agent class. The reflex agent has its percepts and actuators defined as (move right,
left, up, down) and suck. The user can also decide on how many points the agent recieves for clean tiles, how many
points it looses for dirty tiles and the penalty points for moves. On running the program and answering the series
of questions, the user is able to see all the percept sequences, the performance measure scores and the average 
performance measure. 

Initial dirt configurations and respective agent positions are printed in the beginning of the output

'''

import numpy as np
import numpy.random as rand
import sys
from itertools import permutations, chain

class Environment(object):
   # initialize the size of the 2d environment, the max pile size, the number of dirt piles and number of percepts

    def __init__ (self, size, max_pile_size, pile_num , total_percept = 10):
        self.size = size
        self.pile_num = pile_num + 1
        #checking if max dirt piles are greater than total squares available
        if self.pile_num > (self.size[0]*self.size[1]):
            self.pile_num = self.size[0]*self.size[1]
            
        self.max_pile_size = max_pile_size + 1
        self.total_percept = total_percept
        self.check = [[2]]
        
    def random_dirt_place(self):
        #random dirt pile generator at random locations
        for i in range(self.pile_num):
            self.dirt = rand.randint(self.max_pile_size)
            self.x_val = rand.randint(self.size[0])
            self.y_val = rand.randint(self.size[1])
            #check to see if dirt exists in that spot
            while self.env[self.x_val][self.y_val] > 0:
                self.y_val = rand.randint(self.size[1])
                self.x_val = rand.randint(self.size[0])
            self.env[self.x_val][self.y_val] = self.dirt
        print("Dirt config \n" ,self.env)
            
    def defined_dirt(self):
        self.dirt = rand.randint(self.max_pile_size)
        self.count = 0
        #Runs until max pile number
        while (self.count < self.pile_num):
            self.xcod = input("Dirt pile coordinate " + str(self.count+1) + " (x): " )
            self.ycod = input("Dirt pile coordinate " + str(self.count+1) + " (y): " )
            #checking to see if dirt exists
            if self.env[int(self.xcod)-1][int(self.ycod)-1] >0:
                print("Oops , dirt already exists there: ")
            #checking to see if input is within bounds
            elif self.input_check() == True:
                self.env[int(self.xcod)-1][int(self.ycod)-1] = self.dirt
                self.count+=1
            else:
                print("Wrong input try again")
        print("Dirt config \n" , self.env)
            
    def env_all_dirt_f(self,d1,d2): #runs all combinations of dirt and permutes it into a list)
        self.dirt = 1
        self.zz=list()
        self.d1 =d1
        self.d2 =d2 
        for f in range(self.d1):  #generating one combination of dirt
            for g in range(self.d2):    
                self.env[f][g] = self.dirt
        self.zz[:] = []
        c1 = self.size[1]
        c2 = self.size[0]
        nc = 0
        y = [None]*c2
        for i in set(permutations(chain.from_iterable(self.env))): #permute that combination
            y[nc] = i[0:c1]
            for nn in range(c2-1):
                nc = nc+1
                y[nc] = i[c1:2*c1]
                c1 = c1*2   
            nc = 0
            c1 = self.size[1]
            self.f = np.array(y)
            for xx in self.check: #check for duplicates
                if np.array_equiv(xx,self.f):
                    pass
                else:
                    self.e = self.f
                    self.zz.append(self.e)
                    print("Dirt config \n" ,self.e)
                 
    def get_zz(self):
        return self.zz 
        
    def env_size(self): #random dirt placements
        self.env = np.zeros((self.size[0], self.size[1]))
        self.random_dirt_place()
        return self.env
    
    def env_size_manual(self): #defined dirt placements
        self.env = np.zeros((self.size[0], self.size[1]))
        self.defined_dirt()
        return self.env
    
    def env_size_all_f(self,a,b): #dirt placements for all configurations (adding)
        self.a = a
        self.b = b
        self.env = np.zeros((self.size[0], self.size[1]))
        self.env = self.env_all_dirt_f(a,b)
    
    def zero_config_setup(self):
        self.env = np.zeros((self.size[0], self.size[1]))
        print( "Dirt config \n" ,self.env)
        return(self.env)

    def collision_check(self): #boundary check
        if (0 <= self.agent_x < self.size[0]) and (0 <= self.agent_y < self.size[1]):
            return True
        else:
            return False
        
    def input_check(self): #boundary check
        if (0 < int(self.xcod) <= self.size[0]) and (0 < int(self.ycod) <= self.size[1]):
            return True
        else:
            return False
    

class Reflex_Agent (Environment):
    
    def agent_pos(self): #random position
        self.agent_x = rand.randint(self.size[0])
        self.agent_y = rand.randint(self.size[1])
        print("Agent location x: "+ str(self.agent_x) +" Agent location y: " + str(self.agent_y))
        
    def agent_pos_manual(self): #manual position
        self.xcod = input("Enter x coordinate for robot: ")
        self.ycod = input("Enter y coordinate for robot: ")
        if Environment.input_check():
            self.agent_x = int(self.xcod)-1
            self.agent_y = int(self.ycod)-1
            print("Agent location x: "+ str(self.agent_x) +" Agent location y: " + str(self.agent_y))
            
    def agent_all_pos(self,xa,ya): #agent is placed in all possible locations
        self.agent_x = int(xa)
        self.agent_y = int(ya)
        print("Agent location x: "+ str(self.agent_x) +" Agent location y: " + str(self.agent_y))
        
    def reflex(self,dec):#reflex agent program
        self.dec = dec
        self.ps = list()
        x = self.total_percept
        #decides on which configuration to run as per user input
        if self.dec == 1:
            self.r = Environment.env_size(self)
        elif self.dec== 2:
            self.r = Environment.env_size_manual(self)
        elif int(self.dec[0]) == 3:
            self.r = self.dec[3]
        elif int(self.dec[0]) == 4:
            self.r = Environment.zero_config_setup(self)
            
        while x > 0: #ommitted "for" loop to take care of multiple suck sequences
            while self.r[self.agent_x][self.agent_y] > 0: #Detect dirt
                self.ps.append("Suck") #Suck dirt
                x-=1
                self.r[self.agent_x][self.agent_y] = self.r[self.agent_x][self.agent_y] -1
                
            
            self.move = rand.randint(4)   # 0 means right, 1 means left, 2 means up, and 3 means down
            
            if self.move == 0: # move right
                self.agent_y = self.agent_y +1 
                if Environment.collision_check(self):
                    self.ps.append("Right")
                else:
                    self.agent_y = self.agent_y -1
                    self.ps.append("Collision right No move")
                      
            
            elif self.move == 1: #move left
                self.agent_y = self.agent_y -1
                if Environment.collision_check(self):
                    self.ps.append("Left")
                else:
                    self.agent_y = self.agent_y +1
                    self.ps.append("Collision left No move")
                
            
            elif self.move == 2: #move up
                self.agent_x = self.agent_x -1
                if Environment.collision_check(self):
                    self.ps.append("Up")
                else:
                    self.agent_x = self.agent_x +1
                    self.ps.append("Collision up No move")
                
                
            elif self.move == 3: # move down
                self.agent_x = self.agent_x +1
                if Environment.collision_check(self):
                    self.ps.append("Down")
                else:
                    self.agent_x = self.agent_x -1
                    self.ps.append("Collision down No move")
            x-=1    
     
    def performance_measure(self,cs = 10,ds = 1,mv =1):
            self.move_count = 0
            self.clean_score = 0
            self.dirty_score = 0
            self.cs = int(cs)
            self.ds = int(ds)
            self.mv = int(mv)
            for c in self.ps:
                if (c == "Right" or c == "Left"  or c == "Up" or c == "Down" ):
                    self.move_count = self.move_count+ self.mv
            
            #Every move is -1, every clean square is +10, every dirty square is -1 by default unless changed
            for row in range(self.size[0]):
                for column in range(self.size[1]):
                    if self.r[row][column] == 0:
                        self.clean_score = self.clean_score + self.cs
                    else:
                        self.dirty_score = self.dirty_score + self.ds
            
            self.total_score = self.clean_score - self.dirty_score - self.move_count
            
    def get_ps(self): 
        return self.ps;
    
    def get_total_score(self):
        return self.total_score;
     

def main():
	sum = 0
	state = True    
	perf = list()
	total_percept_seq = list()
	print("Hello, Welcome to the vacuum clearner environment!")
	esize = input("Please enter the environment size (row,column): ")            
	epsize = input("Please enter the maximum pile size: ")
	epnum = input("Please enter the maximum number of piles: ")            
	eperp = input("Please enter the number of percepts per run: ")
	cs = input("How many reward points for clean tiles? (default is 10, enter +ve num): ")
	ds = input("How many penalty points for dirty tiles? (default is 1, enter +ve num): ")
	mv = input("How many penalty points for number of moves? (deafult is 1, enter +ve num): " )
	esize = [int(x) for x in esize.split(',')] 
	try:
		assert esize[0] >= 0 and esize[1] >=0 and int(epnum) >=0 and int(epsize) >=0 and int(eperp) >=0 and int(cs)>=0 and int(ds) >=0 and int(mv)>=0
	except ValueError as err:
		sys.exit(err)  #exits program if value is unresonable
	y = Environment(esize,int(epsize),int(epnum),int(eperp))
	z = Reflex_Agent(esize,int(epsize),int(epnum),int(eperp))
	while state:
		decision = input("Press 1 if you want to randomize variables (dirt placement, agent placement). Press 2 to manually enter the variables, Press 3 to run all possible configurations: ") 
		#Calls methods to randomize variables
		if int(decision) == 1:
			config_num = input("How many configurations do you want to run? ") 
			for n in range(int(config_num)):
				y.env_size()
				z.agent_pos()
				z.reflex(int(decision))
				z.performance_measure(cs,ds,mv)
				sum = sum +z.get_total_score()
				total_percept_seq.append(z.get_ps())
				perf.append(z.get_total_score())
			state = False   
		 
		#Calls methods to enter variables manually
		elif int(decision) == 2:
			config_num = input("How many configurations do you want to run? ") 
			for n in range(int(config_num)):
				print("\nConfiguration number {}".format(n+1))
				y.env_size_manual()
				z.agent_pos_manual()
				z.reflex(int(decision))
				z.performance_measure(cs,ds,mv)
				sum = sum +z.get_total_score()
				total_percept_seq.append(z.get_ps())
				perf.append(z.get_total_score())
			state = False  
		
		#Calls methods to iterate over all possible combinations
		elif int(decision) == 3:
			decision =[None]*4
			decision[0] = int(3)
			for a in range(esize[0]):
				for b in range(esize[1]):
					y.env_size_all_f(a+1,b+1)
					decision[1] = a+1
					decision[2] = b+1
					for robx in range(esize[0]): 
						for roby in range(esize[1]):
							z.agent_all_pos(robx,roby)
							counter = 0
							for num in y.get_zz():   #Checks permutation list and runs the agent on it
								decision[3] = y.get_zz()[counter]
								counter = counter+1
								z.reflex(decision)
								z.performance_measure(cs,ds,mv)
								sum = sum+z.get_total_score()
								total_percept_seq.append(z.get_ps())
								perf.append(z.get_total_score())
			 
			decision[0] = 4
			y.zero_config_setup()
			for robx in range(esize[0]): 
				for roby in range(esize[1]):
					z.agent_all_pos(robx,roby)
					z.reflex(decision)
					z.performance_measure(cs,ds,mv)
					sum = sum +z.get_total_score()
					total_percept_seq.append(z.get_ps())
					perf.append(z.get_total_score())        
			state = False
						
		else:    
			print("Oops wrong input, please try again")   
			
	#Final result, can be printed to a file if required.
	print("All percept sequences", total_percept_seq)
	print("All scores",perf)
	print("Average performance measure:",sum/len(perf))
	
if __name__ == "__main__":
	main()