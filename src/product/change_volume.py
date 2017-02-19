from subprocess import call, Popen, PIPE
import time

default_vol = 0
vol_floor = 0

def get_system_vol():
	process = Popen(["amixer", "-D", "pulse", "sget", "Master"], stdout=PIPE)
	(output, err) = process.communicate()
	process.wait()
	output = str(output)
	location = output.find("[") + 1
	location2 = output.find("%")
    
	return (int(output[location : location2 ]))

def lower_vol():
    print("Lowering volume...")
    currentVol = get_system_vol()
    for x in range(0, currentVol - vol_floor + 1):
        call(["amixer", "-D", "pulse", "sset", "Master", "1%-"])
        time.sleep(.05)
	

def reset():
    print("Resetting volume...")
    currentVol = get_system_vol()
    for x in range(0, default_vol - currentVol + 1):
        call(["amixer", "-D", "pulse", "sset", "Master","1%+"])
        time.sleep(0.1)
        
def setup_vol():
    global default_vol
    default_vol =  get_system_vol()
    print("Volume setup complete.")

def setup_vol_floor(percentLowered = 10):
    global vol_floor
    vol_floor =  get_system_vol() - percentLowered
    print("Volume setup complete.")
