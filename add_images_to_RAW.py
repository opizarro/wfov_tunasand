#! /usr/bin/env python
# add_images__to_RAW iDIR RAWoutdir
# takes a directory with images
# and assembles a log file with VIS: entries consistent with seabed_localisation


import os
import glob
import re
import time
import calendar
import sys

#rawfile = '/media/lagoon/RAW_DATA/ScottReef200907/r20090726_074343_scott_05_long_transect_auv2/d20090726_074343/20090726_0743.RAW.auv'
#idir = '/Users/opizarro/research/data/seagras
#idir = '/Users/opizarro/research/data/ScottReef200907/r20090726_074343_scott_05_long_transect_auv2/i20090726_074343_cv/*.png'
#idir = '/media/lagoon/RAW_DATA/ScottReef200907/r20090726_074343_scott_05_long_transect_auv2/i20090726_074343/*.pgm'
# example of image name PR_20081012_021022_110_LC16.jpg

# read in arguments
idir = sys.argv[1]
rawoutdir = sys.argv[2]


# list of images
imlist = glob.glob(idir + '/*.tif')
imlist.sort()
nimages = len(imlist)

#print "\nDirectories:\nLOGS: " + rawdir + "\nIMGS: " + idir

if nimages==0 :
    print("\n\nNo IMAGES found! Nothing to merge. Exiting\n")
    quit()
else:
    print("\n\nCreating log entries for "+str(nimages)+ " \n")

# create the new log file that will merge both sources of info
(logpath,logname) = os.path.split(idir)

if not os.path.isdir(rawoutdir):
    os.makedirs(rawoutdir)

flog_merge = open(rawoutdir+"/VIS"+logname+'.RAW.auv','w')

for imfullpath in imlist:
    (impath,im) = os.path.split(imfullpath)
    #print imfullpath
    #print im
    # determine time from file name
    tyear = int(im[3:7])
    tmonth = int(im[7:9])
    tday = int(im[9:11])
    thour = int(im[12:14])
    tminute = int(im[14:16])
    tsecond = float(im[16:18] + '.' + im[19:22])
        
    # print str(tyear) + ' ' + str(tmonth) + ' ' + str(tday) + ' ' + str(thour) + ' ' + str(tminute) + ' ' + str(tsecond)
        
    #easy_tstring = im[3:15] + tsecond
        
    #tstruc = time.strptime(
        
    tunix = calendar.timegm([tyear,tmonth,tday,thour,tminute,tsecond])
    tstruc = time.gmtime(tunix)

    # swap extension
    logentry = "VIS: " + "%.3f" % tunix + " [" + "%.3f" % tunix + "] " + im[:-3] + "tif" + "\n"
        #logentry = "VIS: " + "%.3f" % tunix + " [" + "%.3f" % tunix + "] " + im[:-3] + "png" + "\n"

    flog_merge.write(logentry)

flog_merge.close()

        
                

        
