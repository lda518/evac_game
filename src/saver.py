import pickle
import os

class Saver:
    def __init__(self, path):
        self.path = path

    def save(self, data, name):
        self.name = name 
        self.data = data
        count = 0
        file_name = self.name+'_'+str(count).zfill(3)
        self.file_path = os.path.join(self.path, file_name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.file_path):
            self.dump()
        while os.path.exists(self.file_path):
            count += 1
            self.file_path = os.path.join(
                    self.path, self.name+'_'+str(count).zfill(3))
        self.dump()

    def dump(self):
        with open(self.file_path, 'wb') as f:
            pickle.dump(self.data, f)
