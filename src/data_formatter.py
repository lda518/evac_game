import numpy as np
import random
import os
from scipy.stats import mannwhitneyu
class Data_formatter:
    def __init__(self, versions):
        self.versions = versions
        self.formatted_vers = {}
        gen_list = []
        for ver in self.versions:
            gens = self.versions[ver][0].select('gen')
            gen_list.append(gens)
            _min, _max, _avg, _std = self.get_all_means(self.versions[ver])
            mean = np.mean(_avg)
            stdv = np.std(_avg)
            max_mean = np.mean(_max)
            stats = {'gens':gens,'min':_min, 'max':_max, 'avg':_avg, 'std':_std,
                    'mean':mean, 'max_mean':max_mean, 'stdv':stdv}
            self.formatted_vers[ver] = stats
        self.gen = min(gen_list)

    def get_all_means(self,logs):
        _min = self.get_mean(logs, 'min')
        _max = self.get_mean(logs, 'max')
        _avg = self.get_mean(logs, 'avg')
        _std = self.get_mean(logs, 'std')
        return _min, _max, _avg, _std

    def get_mean(self,logbooks, selection):
        running = [0]*len(logbooks[0].select('gen'))
        for l in logbooks:
            sel = l.select(selection)
            for i in range(len(sel)):
                #print(i)
                running[i] += sel[i]
        return [x / len(logbooks) for x in running]
    
    def save_stats(self, save_path, versions):
        stats = ''
        if len(versions) >= 2:
            for ver in range(len(versions)):
                for comb in range(len(versions)-(ver+1)):
                    ver1 = versions[ver] 
                    ver2 = versions[ver+comb+1]
                    stats += '{0} against {1}\n'.format(ver1, ver2)
                    to_test = [ver1, ver2]
                    avg_p, max_p = self.mann_test(to_test)
                    stats += 'avg_p: {0} \nmax_p: {1}\n\n'.format(round(avg_p,3), 
                                                                  round(max_p,3))
        for ver in versions:
            mean = self.formatted_vers[ver]['mean']
            stdv = self.formatted_vers[ver]['stdv']
            max_mean = self.formatted_vers[ver]['max_mean']
            stats += '\n' + ver
            stats += '\nmean: {0} \nstdv: {1}\nmax_mean: {2}\n'.format(round(mean,3), 
                                                        round(stdv,3), round(max_mean,3))
        save_path = os.path.join(save_path, 'stats')
        with open(save_path, "w") as text_file:
           text_file.write(stats)


    def mann_test(self, versions):
        avg_stat, avg_p = mannwhitneyu(self.formatted_vers[versions[0]]['avg'],
                                self.formatted_vers[versions[1]]['avg'])
        max_stat, max_p = mannwhitneyu(self.formatted_vers[versions[0]]['max'],
                                self.formatted_vers[versions[1]]['max'])
        return avg_p, max_p
        
    def u_value(self, versions):
        u1 = 0
        u2 = 0
        group_a = self.formatted_vers[versions[0]]['avg']
        group_b = self.formatted_vers[versions[1]]['avg']
        length = min(len(group_a), len(group_b))
        for i in range(length):
            if (self.formatted_vers[versions[0]]['avg'][i] >
                self.formatted_vers[versions[1]]['avg'][i]):
                u1 += 1
            else:
                u2 += 1
        return min(u1,u2)

    def one_tailed(self, versions):
        iterations = 9999   
        diffs = [0] * iterations
        data_a = self.formatted_vers[versions[0]]['avg']
        data_b = self.formatted_vers[versions[1]]['avg']
        for i in range(iterations):
            list_a, list_b = self.shuffle_groups(data_a, data_b)
            meanA = sum(list_a) / len(list_a)
            meanB = sum(list_b) / len(list_b)
            diffs[i] = abs(meanA - meanB)
        actual_diff = abs(np.mean(data_a) - np.mean(data_b))
        counter = 0
        for i in range(iterations):
            if diffs[i] >= actual_diff:
                counter += 1 
        p = (counter + 1) / (iterations + 1)
        return p

    def shuffle_groups(self, list_a, list_b):
        list_both = list(list_a) + list(list_b)
        random.shuffle(list_both)
        list_a, list_b = list_both[:len(list_a)], list_both[len(list_a):]
        return(list_a, list_b)        


