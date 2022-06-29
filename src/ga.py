import random 
import numpy as np
from deap import base
from deap import creator
from deap import tools
from network import MLP
from society import Society

class GA:
    def __init__(self, hyperparams, toolbox, stats, net):
        self.MUTPB = hyperparams[0]
        self.CXPB = hyperparams[1]
        self.ITERATIONS = hyperparams[2]
        self.NGEN = hyperparams[3]
        self.POPSIZE = hyperparams[4]
        self.GAMES = hyperparams[5]
        self.NONADAPT = hyperparams[6]

        self.myNet = net
        self.IND_SIZE = self.myNet.getIndSize()

        self.toolbox = toolbox
        self.stats = stats

    def evolve(self):
        logbook = tools.Logbook()
        self.pop = self.toolbox.population(n=self.POPSIZE)
        #fitnesses = evaluate_self.pop(self.pop)
        fitnesses = self.evaluate()
        for ind, fit in zip(self.pop, fitnesses):
            ind.fitness.values = fit

        for g in range(self.NGEN):
            offspring = self.toolbox.select(self.pop, len(self.pop))
            offspring = list(map(self.toolbox.clone, offspring))
            if self.CXPB > 0.0:
                for child1, child2 in zip(offspring[::2], offspring[1::2]):
                    if random.random() < self.CXPB:
                        self.toolbox.mate(child1, child2)
                        del child1.fitness.values
                        del child2.fitness.values

            for mutant in offspring:
                self.toolbox.mutate(mutant)
                del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            #fitnesses = evaluate_self.pop(invalid_ind)
            fitnesses = self.evaluate()
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            self.pop[:] = offspring
            record = self.stats.compile(self.pop)
            logbook.record(gen=g, **record)
     
            if g % 100 == 0:
                print("-- Generation %i --" % g)
                pop_fitnesses = [self.pop[x].fitness.values for x in range(len(self.pop))]
                pop_average = round(np.mean(pop_fitnesses),2)
                print("Avg: " + str(pop_average))
        return logbook

    def evaluate(self):
        pop_stats = [[0,0]]*len(self.pop)
        fitnesses = []
        players = list(range(len(self.pop)))
        society = Society(players, self.pop, self.myNet, self.NONADAPT)
        
        for game in range(self.GAMES):
            player1 = players[random.randrange(len(players))]
            player2 = players[random.randrange(len(players))] 
            score1, score2 = society.run_round(player1, player2)
            pop_stats[player1][0] += 1 
            pop_stats[player2][0] += 1 
            pop_stats[player1][1] += score1 
            pop_stats[player2][1] += score2 
        
        for player in pop_stats:
            fitnesses.append((player[1]/player[0],))
        return fitnesses
