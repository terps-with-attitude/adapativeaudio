from subprocess import call, Popen, PIPE

vol = 0

def getSystemVol():
	process = Popen(["amixer", "-D", "pulse", "sget", "Master"], stdout=PIPE)
	(output, err) = process.communicate()
	exit_code = process.wait()

	output = str(output)

	location = output.find("[") + 1
	location2 = output.find("%")

	vol = int(output[location : location2 ])

def lowerVol(percentLowered = 10):
	percentLowered = str(percentLowered)
	call(["amixer", "-D", "pulse", "sset", "Master", percentLowered + "%" + "-"])

def setVol(volVal = vol):
	volVal = str(volVal)
	call(["amixer", "-D", "pulse", "sset", "Master", volVal + "%"])



getSystemVol()