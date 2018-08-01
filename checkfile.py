import os
import re
import sys
import time

filepath = sys.argv[1]
LogName = os.listdir(filepath)
Expect_LogName = ["1098R20_SDK_sdk_nvme_ramdrive_debug.axf", "ASIC_NVME_Ramdisk_0.lst", "C1_ATCM", "PROGRAM0"]

if __name__ == "__main__":	
	f = open(filepath + "/summary.log","w")	         
	for LogNameinBuildStatus in Expect_LogName:
		#print "(filepath + LogNameinBuildStatus) ->", (filepath + LogNameinBuildStatus)
		if os.path.exists(filepath + LogNameinBuildStatus):
			f.write("%-30s:\tPASS\n" %LogNameinBuildStatus)
		else:
			f.write("%-30s:\tFail\n" %LogNameinBuildStatus)	
	f.close()
	print "Finished"
		
