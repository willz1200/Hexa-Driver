import pickle
import matplotlib.pyplot as plt

class DataProcesser(  ):
    def __init__(self,filepath):
        self.filepath = filepath
        self.data = pickle.load( open( self.filepath, "rb" ) )
    
    def unpack_data(self):
        time = []
        position = []
        velocity = []
        for line in self.data:
            line = line.split(',')
            time.append(float (line[1]))
            position.append(float (line[2]))
            velocity.append(float (line[3]))
        self.time = time
        self.position = position
        self.velocity = velocity
    
    def plot_data(self):
        fig, ax = plt.subplots()
        
        ax.plot(self.time, self.position)
        ax.plot(self.time, self.velocity)
        plt.show()

if __name__ == '__main__':
    data = DataProcesser("../data_out/data.p")
    data.unpack_data()
    data.plot_data()
    breakpoint()