
from graphs import Graph
from data_formatter import Data_formatter
import pickle
import os
stat_path = os.path.join('..','stats')

versions = []
ver_dict = {}
versions.append('best_running_algorithm')
versions.append('non_adaptive_run')

for ver in versions:
    path = stat_path
    data_path = os.path.join(path, ver)
    datas = os.listdir(data_path)
    data_list = []
    for data in datas:
        with open(os.path.join(data_path,data), 'rb') as file:
            data_list.append(pickle.load(file))
    ver_dict[ver] = data_list


formatter = Data_formatter(ver_dict)
grapher = Graph(formatter.formatted_vers, formatter.gen, show=True)

grapher.avg_graph(versions)
