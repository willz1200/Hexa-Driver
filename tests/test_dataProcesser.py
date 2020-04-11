from sdk.data_processer import *

def test_m():
    assert True

def test_freq_reponce():
    data = DataProcesser("../data_out/pickle_data/frequency_responce_data_30_Hz.p")
    data.unpack_data()
    data.plot_data()

def test_step_reponce():
    data = DataProcesser("../data_out/pickle_data/frequency_responce_data_step_255_Hz.p")
    data.unpack_data()
    data.plot_data()

def test_multi_files():
    print_all_files('../data_out/pickle_data/')

def print_all_files( mypath):

        f = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            f.append(filenames)
            break
        for file_name in f[0]:
            data = DataProcesser("../data_out/pickle_data/" + file_name)
            data.unpack_data()
            print ( '%s ----------> %s' %(file_name ,data.find_max_vel()) ) 
            fig_name = file_name.strip(".p")+".png" 
            data.plot_data("../figures/" , fig_name)