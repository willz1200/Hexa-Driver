import pickle
import matplotlib.pyplot as plt
from os import walk

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
            position.append(float (line[2]))
            velocity.append(float (line[3]))
            dutyCycle.append(float (line[4]))
        self.time = time
        self.dutyCycle = dutyCycle
        self.position = position
        self.velocity = velocity
    
    def plot_data(self, path, filename):
        fig, ax = plt.subplots()
        ax.plot(self.time, self.dutyCycle, label = "Duty Cycle")
        ax.plot(self.time, self.position, label = "Position")
        ax.plot(self.time, self.velocity, label = "Velocity")
        ax.set_xlabel('Time (ms)')
        ax.set_ylabel('Amplitude')
        ax.set_title('Frequency responce')
        ax.legend()
        plt.savefig(path+filename)
        # plt.show()

    # def print_all_files(self, mypath):

    #     f = []
    #     for (dirpath, dirnames, filenames) in walk(mypath):
    #         f.extend(filenames)
    #         break
    #     print f

    def find_max_vel(self):
        return max(self.velocity)

if __name__ == '__main__':
    data = DataProcesser("./pickle_data/frequency_responce_data.p")
    data.unpack_data()
    data.plot_data()
    # breakpoint()