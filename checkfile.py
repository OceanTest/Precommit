import os
import re
import sys
import time
import glob
from itertools import izip

filepath = "/home/jenkins/workspace/Dramless_Precommit/"
ExpectedLog = [(filepath + "1098R20_SDK_sdk_nvme_ramdrive_debug.log"), (filepath + "ASIC_NVME_Ramdisk_0.log"), (filepath + "C1_ATCM.log")]
LogName = ["1098R20_SDK_sdk_nvme_ramdrive_debug.log", "ASIC_NVME_Ramdisk_0.log", "C1_ATCM.log"]

if __name__ == "__main__":	
	f = open("./testlogs/Build/summary.log","w")
	Log = glob.glob(filepath + r"*.log")           
	for (FileinBuildStatus, LogNameinBuildStatus) in izip(Log, LogName):
		if FileinBuildStatus in ExpectedLog:
			f.write("%-30s:\tPASS\n" %LogNameinBuildStatus)
		else:
			f.write("%-30s:\tFail\n" %LogNameinBuildStatus)	
	f.close()
	print "Finished"		
