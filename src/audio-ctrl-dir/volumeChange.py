from subprocess import call, Popen, PIPE
import time

defaultVol = 0

def getSystemVol():
	process = Popen(["amixer", "-D", "pulse", "sget", "Master"], stdout=PIPE)
	(output, err) = process.communicate()
	exit_code = process.wait()

	output = str(output)

	location = output.find("[") + 1
	location2 = output.find("%")

	return (int(output[location : location2 ]))

def lowerVol(percentLowered = 10):
	#percentLowered = str(percentLowered)
	for x in range(0, percentLowered + 1):
		call(["amixer", "-D", "pulse", "sset", "Master", "1%-"])
		time.sleep(.05)

def setVol(volVal):

	currentVol = getSystemVol()
	print(currentVol)
	print(volVal)

	for x in range(0, volVal - currentVol + 1):
		call(["amixer", "-D", "pulse", "sset", "Master","1%+"])
		time.sleep(.05)



defaultVol = getSystemVol()
print("defualt vol is", defaultVol)
lowerVol()
time.sleep(5)
setVol(defaultVol)