import matplotlib.pyplot as plt
import os
import numpy as np

class Graph:
    def __init__(self, versions, gens, hof=None, save=None, show=False):
        self.formatted_vers = versions            
        self.gen = gens
        self.save = save
        self.show = show
        self.resolution = [8,5]

    def line_gen(self, lines, _type):
        plt.rc('axes', labelsize=14)
        plt.rc('xtick', labelsize=14)
        plt.rc('ytick', labelsize=14) 
        plt.rc('legend', fontsize=14)

        fig, ax1 = plt.subplots()
        for line in lines:
            l = np.array(self.formatted_vers[line][_type][:len(self.gen)])
            if len(l.shape) == 2:
                ax1.plot(self.gen, l[:,0], label=line+" food eaten")
                ax1.plot(self.gen, l[:,1], label=line+" move score")
                ax1.plot(self.gen, l[:,2], label=line+" available squares")
            else: 
                ax1.plot(self.gen, l, label=line)
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Fitness")
        plt.title(_type)
        plt.legend()
        plt.grid()
        figure = plt.gcf()
        figure.set_size_inches(self.resolution[0],self.resolution[1])
        if self.save != None:
            line_graph_dir = os.path.join(self.save, 'line_graph')
            if not os.path.exists(line_graph_dir):
                os.mkdir(line_graph_dir)
            plt.savefig(os.path.join(line_graph_dir, _type+'.jpg'), dpi=300)
        if self.show:
            plt.show()

    def line_filled(self, lines, _type):
        plt.rc('axes', labelsize=14)
        plt.rc('xtick', labelsize=14)
        plt.rc('ytick', labelsize=14) 
        plt.rc('legend', fontsize=14)

        fig, ax1 = plt.subplots()
        for line in lines:
            l = self.formatted_vers[line][_type][:len(self.gen)]
            _std = self.formatted_vers[line]['std']
            ax1.plot(self.gen, l, lw=1, label=line)
            high_bound = [ l[x] +(_std[x]/2) for x in range(len(self.gen))]
            low_bound = [ l[x] - (_std[x]/2) for x in range(len(self.gen))]
            if isinstance(high_bound[0], np.ndarray):
                high_bound = self.extract_nd(high_bound)
                low_bound = self.extract_nd(low_bound)
            ax1.fill_between(self.gen, high_bound, low_bound, alpha=0.5)
        ax1.set_xlabel("Generation")
        ax1.set_ylabel("Fitness")
        plt.title(_type)
        plt.legend()
        plt.grid()
        figure = plt.gcf()
        figure.set_size_inches(self.resolution[0],self.resolution[1])
        if self.save != None:
            filled_line_dir = os.path.join(self.save, 'filled_line_graph')
            if not os.path.exists(filled_line_dir):
                os.mkdir(filled_line_dir)
            plt.savefig(os.path.join(filled_line_dir, _type+'.jpg'), dpi=300)
        if self.show:
            plt.show()


    def box_plot(self, lines, _type):
        plt.rc('axes', labelsize=14)
        plt.rc('xtick', labelsize=14)
        plt.rc('ytick', labelsize=14) 
        plt.rc('legend', fontsize=14)

        fig, ax1 = plt.subplots()
        for i in range(len(lines)):
            l = self.formatted_vers[lines[i]][_type][:len(self.gen)]
            if isinstance(l[0], np.ndarray):
               l = self.extract_nd(l)
            ax1.boxplot(l,labels=[lines[i]], positions = [i])
        ax1.set_xlabel("Variant")
        ax1.set_ylabel("Fitness")
        plt.title(_type)
        plt.legend()
        figure = plt.gcf()
        figure.set_size_inches(self.resolution[0],self.resolution[1])
        if self.save != None:
            box_plot_dir = os.path.join(self.save, 'box_plot')
            if not os.path.exists(box_plot_dir):
                os.mkdir(box_plot_dir)
            plt.savefig(os.path.join(box_plot_dir, _type+'.jpg'), dpi=300)
        if self.show:
            plt.show()

    def extract_nd(self, array):
        final = []
        for a in array:
            final.append(a[0])
        return final

    def hof_box(self, versions):
        self.stat = 'hof'
        self.box_plot(versions, self.stat)
   
    def max_graph(self, versions):
        self.stat = 'max'
        self.line_gen(versions, self.stat)
        self.line_filled(versions, self.stat)
        self.box_plot(versions, self.stat)

    def avg_graph(self, versions):
        self.stat = 'avg'
        self.line_gen(versions, self.stat)
        self.line_filled(versions, self.stat)
        self.box_plot(versions, self.stat)

    def min_graph(self, versions):
        self.stat = 'min'
        self.line_gen(versions, self.stat)

