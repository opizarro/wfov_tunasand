# read a GAPS standard output file
# particular string of interest is  $PTSAG
# Transponder Absolute Positioning Message (geographical coordinates and depth)
# $PTSAG,#NNNNN, hhmmss.sss,jj,mm,aaaa,BBB,DDMM.MMMMM,H,DDDMM.MMMMM,D,A,MMMM.M,A, MMMM.M *CK
# want to write to something like
#fprintf(fid,'GPS_RMC: %.3f\t Lat:%.6f N Lon:%.6f W Bad:0 A Spd:0 Crs:0 Mg:nan\n',sps.t(k),sps.lat(k),sps.lon(k));

import pynmea2
import string
import datetime
import calendar
import time


#GAPSlog = open('/Users/opizarro/data/TunaSand/GAPSexample/20140605163#709-001.dat')
#GAPSlog = open('/Users/opizarro/data/TunaSand/Dive_15/GAPS/20160714124941-003.dat')
GAPSlog = open('/media/data/RAW_DATA/Sesoko201607/TunaSand/Dive_16/GAPS/combinedGAPS16.dat')

GAPS_rawlog = open('/tmp/test.RAW.auv','w')


#head=GAPSlog.readline()
#print head

def dm2dd(dm ):
    degrees = int(dm/100)
    minutes = dm-degrees*100
    dd = float(degrees) + float(minutes)/60 ;
    return dd;


streamreader = pynmea2.NMEAStreamReader()
for line in GAPSlog:
    try:
        #strip leading <
        cleanline = line.strip('< ')
        msg = pynmea2.parse(cleanline)

        #print msg
        #print msg.data
        #print msg.identifier()
        #print vars(msg)
        #print see(msg)
        #print 'parsed from ' + line
    except:
        print('could not parse ' + line )
        continue

    if msg.identifier()=='PTSA' and msg.data[0]=='G':
        print('message PTSAG')
        #$PTSAG,#02754,043516.771,14,07,2016,0,2640.20937,N,12751.97519,E,F,0000.0,0,0000.0*2A
             #0,    1 ,  2       ,3 ,4 , 5  ,6, 7        ,8, 9         ,10,
        # get timestamp lat and lon and print out RAW message

        if msg.data[6]=='1':   # transponder number for AUV
            print(msg)
            LatDM = msg.data[7]
            Lat = dm2dd(float(LatDM))
            NS = msg.data[8]

            LonDM = msg.data[9]
            Lon = dm2dd(float(LonDM))
            EW = msg.data[10]

            HMS = msg.data[2]
            hh = HMS[0:2]
            mm = HMS[2:4]
            ss = HMS[4:6]
            micros = HMS[7:10]

            day = msg.data[3]
            month = msg.data[4]
            year = msg.data[5]



            # timestring = year + ' ' + month + ' ' + day + ' ' + hh +':' + mm + ':' + ss
            # print(timestring)
            # dt= datetime.datetime.strptime(timestring, "%Y %m %d %H:%M:%S")
            # this requires python 3.3
            #utime_nomicro = (dt - datetime.datetime(1970, 1, 1)) / datetime.timedelta(seconds=1)

            # withmicroseconds
            #utime = utime_nomicro + float(micros) / 1000

            tyear = int(year)
            tmonth = int(month)
            tday = int(day)
            thour = int(hh)
            tminute = int(mm)
            tsecond = float(ss)+float(micros)/1000
            tunix = calendar.timegm([tyear, tmonth, tday, thour, tminute, tsecond])
            tstruc = time.gmtime(tunix)

            outputstr = 'GPS_RMC: {:.3f}\t Lat:{:.6f} {} Lon:{:.6f} {} Bad:0 A Spd:0 Crs:0 Mg:nan\n'.format(tunix,Lat,NS,Lon,EW)
            print(outputstr)
            GAPS_rawlog.write(outputstr)
