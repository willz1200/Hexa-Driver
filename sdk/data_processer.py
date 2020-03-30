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
            position.append(float (line[2]))
            velocity.append(float (line[3]))
            dutyCycle.append(float (line[4]))
        self.time = time
        self.dutyCycle = dutyCycle
        self.position = position
        self.velocity = velocity
    
    def plot_data(self):
        fig, (ax1,ax2) = plt.subplots(2)
        ax1a = ax1.twinx()
        ax1.plot(self.time, self.dutyCycle, 'b', label = "Duty Cycle")
        
        ax2.plot(self.time, self.position, 'y' , label = "Position")
        ax1a.plot(self.time, self.velocity, 'r' , label = "Velocity")
        ax1.set_xlabel('Time (ms)')
        ax2.set_xlabel('Time (ms)')
        ax1.set_ylabel('Input: Duty cycle (bits)')
        ax1a.set_ylabel('Output: Motor velocity (samples/ms) ')
        ax2.set_ylabel('Motor position (samples/ms) ')
        ax1.set_title('Frequency responce')
        ax1.legend()
        ax1a.legend()
        ax2.legend()
        plt.show()

if __name__ == '__main__':
    data = DataProcesser("./pickle_data/frequency_responce_data.p")
    data.unpack_data()
    data.plot_data()
    # breakpoint()