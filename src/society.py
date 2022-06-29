import numpy as np
import random 

class Society:
    def __init__(self, players, brains, net, non_adapt=False):
        self.players = {player:None for player in players}
        self.brains = brains
        self.net = net
        self.non_adapt = non_adapt
        self.set_initial_socs()

    def set_initial_socs(self):
        for player in self.players:
            self.net.setWeightsLinear(self.brains[player])
            output = self.net.feedForward([-1]*3) # TODO Find right initial values for net
            self.set_soc(player, output)

    def set_soc(self, player, output):
        decision = np.argmax(output, axis=0)
        if self.non_adapt == True:
            decision = random.randint(0,3)
        # Saints encoded to 0, buddies encoded to 1, fight_club encoded to 2,
        # vandals encoded to 3
        if decision == 0:
            self.players[player] = 0
        if decision == 1:
            self.players[player] = 1
        if decision == 2:
            self.players[player] = 2
        if decision == 3:
            self.players[player] = 3

    def run_round(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.get_behaviour()
        self.get_points()
        if self.non_adapt == False:
            self.normalize_data()
            self.make_decisions()
        return self.p1_points, self.p2_points

    def get_behaviour(self):
        # 0 for cooperate, 1 for be selfish
        self.p1_soc = self.players[self.player1]
        self.p2_soc = self.players[self.player2]

        if self.p1_soc == 0:
            self.p1_behav = 0
        if self.p2_soc == 0:
            self.p2_behav = 0

        if self.p1_soc == 1:
            if self.p2_soc == 1:
                self.p1_behav = 0
            else:
                self.p1_behav = 1
        if self.p2_soc == 1:
            if self.p1_soc == 1:
                self.p2_behav = 0
            else:
                self.p2_behav = 1

        if self.p1_soc == 2:
            if self.p2_soc == 2:
                self.p1_behav = 1
            else:
                self.p1_behav = 0
        if self.p2_soc == 2:
            if self.p1_soc == 2:
                self.p2_behav = 1
            else:
                self.p2_behav = 0

        if self.p1_soc == 3:
            self.p1_behav = 1
        if self.p2_soc == 3:
            self.p2_behav = 1

    def get_points(self):
        if self.p1_behav == 0:
            if self.p2_behav == 0:
                self.p1_points = 4
                self.p2_points = 4
            else:
                self.p1_points = 0
                self.p2_points = 6
        if self.p1_behav == 1:
            if self.p2_behav == 0:
                self.p1_points = 6
                self.p2_points = 0
            else:
                self.p1_points = 1
                self.p2_points = 1

    def normalize_data(self):
        self.relative_points = (self.p1_points-self.p2_points) / (self.p1_points + self.p2_points) 

    def make_decisions(self):
        self.net.setWeightsLinear(self.brains[self.player1])
        output = self.net.feedForward([self.relative_points,
                                       self.p1_soc, self.p2_soc])
        self.set_soc(self.player1, output)

        self.net.setWeightsLinear(self.brains[self.player2])
        output = self.net.feedForward([self.relative_points*-1,
                                       self.p2_soc, self.p1_soc])
        self.set_soc(self.player2, output)
