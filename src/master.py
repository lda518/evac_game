from ga import GA
import random 
import os
import numpy as np
from deap import base
from deap import creator
from deap import tools
from network import MLP
from society import Society
from saver import Saver

class Master:
    def __init__(self):
        self.set_defaults()
        self.stat_path = os.path.join('..','stats')

    def set_defaults(self):
        mut = 0.3
        cxpb = 0.0
        its = 5 
        ngen = 5000
        popsize = 50  
        games = 500
        non_adapt = False
        self.hyperparams = [mut, cxpb, its, ngen, popsize, games, non_adapt]

    def set_ga(self):
        myNet = MLP()
        IND_SIZE = myNet.getIndSize()

        toolbox = base.Toolbox()
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox.register("attr_float", random.uniform, -1.0, 1.0)
        toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_float, n=IND_SIZE)

        toolbox.register("select", tools.selTournament, tournsize=6)
        toolbox.register("mutate", tools.mutGaussian, mu=0.0, sigma=0.5, indpb=self.hyperparams[0])
        toolbox.register("mate", tools.cxUniform, indpb=self.hyperparams[1])
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        stats = tools.Statistics(key=lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)

        self.ga = GA(self.hyperparams, toolbox, stats, myNet)

    def run(self):
        self.set_ga()
        self.logbooks = self.ga.evolve()
        #self.mean_score = np.mean(self.log_avg)
        
    def get_log_avg(self):
        total_avg = 0
        avg_logs = []
        for logbook in self.logbooks:
            log_vals = [0]*len(logbook)
            for gen in range(len(logbook)):
                log_vals[gen] += logbook[gen]['avg']/len(self.logbooks)
            avg_logs.append(log_vals)
        log_sum = [ sum(x) for x in zip(*avg_logs) ]
        self.log_avg = [x/len(self.logbooks) for x in log_sum]

    def mut_sweep(self):
        self.best_runs = {}
        for i in range(10):
            self.hyperparams[0] = i/10
            self.hyperparams[1] = 0
            self.name = 'mut:_{0}'.format(self.hyperparams[0])
            self.run()
            self.best_runs[mean_score] = name
        
    def cross_sweep(self):
        self.best_runs = {}
        for i in range(10):
            self.hyperparams[0] = 0
            self.hyperparams[1] = i/10
            self.name = 'cross:_{0}'.format(self.hyperparams[1])
            self.run()
            self.best_runs[mean_score] = name

    #def mut_cross_sweep(self):
    #    saver = Saver(os.path.join(stat_path, 'mut_cross_sweep'))
    #    best_runs = {}
    #    self.hyperparams = set_defaults()
    #    for i in range(10):
    #        for j in range(10):
    #            self.hyperparams[0] = i/10 
    #            self.hyperparams[1] = j/10
    #            name = 'mut:_{0},cross:_{1}'.format(self.hyperparams[0],self.hyperparams[1])
    #            self.logbooks = self.run(self.hyperparams)
    #            #saver.save(self.logbooks, name)
    #            avg_log = get_log_avg(self.logbooks)
    #            mean_score = np.mean(avg_log)
    #            best_runs[mean_score] = name
    #    return best_runs, saver

    def non_adaptive(self):
        self.hyperparams[6] = True
        self.name = 'non_adaptive_run'
        self.run()

    def normal_run(self):
        self.name = 'best_running_algorithm'
        self.run()

    def save(self):
        saver = Saver(os.path.join(self.stat_path, self.name))
        saver.save(self.logbooks, self.name)


