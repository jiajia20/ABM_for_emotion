import random as rd
from pylab import *

"""
This version I introduce two more realistic version of mood change: regression to normal and enviormental noise. the goal is to introduce randomness to see if the model is robost 
"""


# create an agent with a mood with 
class agent:
        
    def __init__(self, i, ww=0.1, wl=0.05, ll=0, moodb=0.5, mr = 0.5, mv = 0.01 ):
        self.mood = random()  # bound (0,1)  round(random(),2)
        self.index= i
        self.ww = ww  # cooperation - cooperation
        self.wl = wl  # cooperation - betrayal
        self.ll = ll  # betrayal- cooperation
        self.moodb = moodb  # decide which mood is good/bad
        self.mr = mr  # factor for mood regression
        self.mv = mv  # factor for mood variability
        
        
    def mood_regression(self): #    assume that agent mood will regress to normal (the moodb factor)
        #this manipulation will reduce the mood divergence according to the difference, more delta more change
        delta = self.mood - self.moodb
        if (delta > 0):
            self.mood -= delta * self.mr
        elif (delta < 0):
            self.mood -= delta * self.mr
    
        
    def mood_vary(self):  # assume the mood will vary from enviormental noise 
        self.mood += self.mv * (random() - 0.5) #change between (factor x (-0.5, 0.5))
        
    def change_mr(self, mr):  
        self.mr = mr
    
    def change_mv(self, mv):
        self.mv = mv
        
    def change_payoff(self, ww, wl, ll):
        self.ww = ww 
        self.wl = wl 
        self.ll = ll #betreial-cooperate
    
    def change_moodb(self, moodb):
        self.moodb = moodb
        
    def game(self, other):
        if self.mood >self.moodb and other.mood > self.moodb:  #cooperation - cooperation
            self.mood += self.ww
            other.mood += self.ww            
        elif self.mood > self.moodb and other.mood < self.moodb:  # cooperation - betrayal
            self.mood -= self.wl
            other.mood += self.wl 
        elif self.mood < self.moodb and other.mood > self.moodb:   # betrayal - cooperation
            self.mood += self.wl
            other.mood -= self.wl
        else:                                                 # betrayal - betrayal
            self.mood +=  self.ll
            other.mood +=  self.ll
            
        return 
    

    
    
def initialize_network_agent(network):
    directory = {} 
    node_num = network.number_of_nodes()
    for i in range (node_num):
        directory.update({ i : agent(i)})
    return directory

def change_all_payoff(di,ww,wl,ll):
    for i in range(len(di)):
        player = di.get(i)
        player.change_payoff(ww,wl,ll)
    return

def change_moodbi(di,mb):
    for i in range(len(di)):
        player = di.get(i)
        player.change_moodb(mb)
    return

def change_mood_noise(di, mv):
    for i in range(len(di)):
        player = di.get(i)
        player.change_mv(mv)
    return

def change_mood_regression(di,mr):
    for i in range(len(di)):
        player = di.get(i)
        player.change_mr(mr)
    return
    




def play(network, directory, mvy = 0, mry = 0):  #default: no mood noise, no mood regression
    #play game
    ##shuffule
    node_num = network.number_of_nodes()
    index = list(range(node_num))
    rd.shuffle(index)
    
    for i in index:
        #didn't shuffle neighbors but figured won't need to shuffle twice??
        neighbors = [n for n in network.neighbors(i)]
        player = directory.get(i) #return player agent
        for j in neighbors:
            player.game(directory.get(j)) #play a interaction game and update accordingly
         
    # each network only update their mood with noise and regression ONCE after everyone done playing
    if(mry == 1):
        for i in index:
            player = directory.get(i) 
            player.mood_regression()
            
    if(mvy == 1):
        for i in index:
            player = directory.get(i) 
            player.mood_vary() 

            
    #record the mood
    mood_value = []
    for i in list(directory.values()):
        mood_value.append(i.mood)
         
    return  mood_value

def run_sim(network, di, iters=100, mvy = 0, mry = 0):
    #make a storage list 
    mood_overtime = []
    for k in range(iters):
        mood_value = play(network, di, mvy, mry)
        mood_overtime.append(mean(mood_value))
        
    return mood_overtime   


"""
----------------------------------------radicalization simulation -----------------------------------------
"""
# examine the radicalizaton of the network

def play_rad(network, directory):
    #play game
    ##shuffule
    node_num = network.number_of_nodes()
    index = list(range(node_num))
    rd.shuffle(index)
    
    for i in index:
        neighbors = [n for n in network.neighbors(i)] #didn't shuffle neighbors but figured won't need to shuffle twice
        player = directory.get(i) #return player agent
        for j in neighbors:
            player.game(directory.get(j)) #play a interaction game and update accordingly
            
    #return min max
    mood_value = []
    for i in list(directory.values()):
        mood_value.append(i.mood)
    
    return  (max(mood_value)-min(mood_value))

def run_sim_rad(network,di,iters=100):
    #make a storage list 
    mood_diff = []
    for k in range(iters):
        minmax = play_rad(network,di)
        mood_diff.append(minmax)
        
    return mood_diff  

def mood_connectivity(network,directory):
    node_num = network.number_of_nodes()
    neighbors = []
    moods = []
    for i in range(node_num): 
        neighbors.append(len(list (network.neighbors(i) ) ))
        b=directory.get(i)
        moods.append(b.mood)
    return neighbors, moods
        
        
        
        
        
        
