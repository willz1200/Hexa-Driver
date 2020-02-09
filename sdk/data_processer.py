import pickle
import matplotlib.pyplot as plt

class DataProcesser(  ):
    def __init__(self,filepath):
        self.filepath = filepath
        self.data = pickle.load( open( self.filepath, "rb" ) )
    
    def unpack_data(self):
        time = []
        dutyCycle = []
        position = []
        velocity = []
        for line in self.data:
            
            line = line.split(',')
            time.append(float (line[1]))
            dutyCycle.append(float (line[2]))
            position.append(float (line[3]))
            velocity.append(float (line[4]))
        self.time = time
        self.dutyCycle = dutyCycle
        self.position = position
        self.velocity = velocity
    
    def plot_data(self):
        fig, ax = plt.subplots()
        ax.plot(self.time, self.dutyCycle, label = "dutyCycle")
        ax.plot(self.time, self.position, label = "position")
        ax.plot(self.time, self.velocity, label = "velocity")
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Frequency responce')
        ax.legend()
        plt.show()

if __name__ == '__main__':
    data = DataProcesser("../data_out/data.p")
    data.unpack_data()
    data.plot_data()
    # breakpoint()