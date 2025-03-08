import urllib
import datetime
import time
import csv
from subprocess import check_output,Popen,CalledProcessError
import os,sys
import psycopg2
from psycopg2 import Date
from decimal import Decimal

dissemination_times=['04:44','10:44','16:44','22:44']
weekdays=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
tstarts=['00','06','12','18']
app_path=sys.path[0].replace('\\','/')
to_yesterday=0


def writeLog(list):
        logfile=open('data/gfstdl.log','a')
        logfile.write(list)

def chkFile(fname):
    print(fname)
    if not os.access(fname,os.F_OK):
        print('File not found: ' + fname)
        exit(0)

def get_param(fname,lon,lat,pname):
        if float(lon)<0:
                lon=str(360+float(lon))
        if not os.access(fname,os.F_OK):
                print ('File not found: ' + lfile)
                return -1
        #print "get param from file: " + fname
        print(fname)
        print(app_path)
        out = check_output([app_path + "/wgrib2.exe",fname,"-lon",lon,lat,"-match",pname]).decode('utf-8').strip()
        ar=out.split(",")
        print(ar)
        val=ar[2].split("=")
        print(val)
        return val[1]

def K2F(K):
        return ((float(K)-273.15)*1.8+32.0)

def time2min (stTime):
        m=stTime.split(":")
        return int(int(m[0])*60+int(m[1]))

##def getTstart(gm): # this function determines which forecast category will be downloaded.
##        tstart='00'
##
##        gmin=60*gm.hour + gm.minute # convert time variables to minutes for easier processing.
##
##        if gmin < time2min(dissemination_times[0]): # if gm (time snapshop where this script is run) is earlier than 00z.
##                gmin += 60*24                                                   #increment by 1 day
##
##        for i in range (0,len(dissemination_times)):
##                tmin=time2min(dissemination_times[i])
##                if gmin - tmin < 360:
##                                tstart=tstarts[i]
##                                break
##        return tstart

def getTstart(gm): # this function determines which forecast category will be downloaded.

        gmin=60*gm.hour + gm.minute # convert time variables to minutes for easier processing.

        if gmin < time2min(dissemination_times[0]):
             tstart=tstarts[3]
             to_yesterday=1
        elif gmin < time2min(dissemination_times[1]):
             tstart=tstarts[0]
        elif gmin < time2min(dissemination_times[2]):
             tstart=tstarts[1]
        elif gmin < time2min(dissemination_times[3]):
             tstart=tstarts[2]
        else:
            tstart=tstarts[3]

        return tstart

def downloadGrib(date,tstart,tfcst,step,modelres):
    output = "none"
    print(date + (tstart))
    try:

        output = check_output(["/usr/bin/perl",app_path + "/get_AIFS.pl","data",date + (tstart), 
        	                   str(tfcst), str(tfcst), str(step), "all","50t|500t|tmax_2m|tmin_2m)", '.' ])
    except CalledProcessError as e:

        output = e.output

    output = output.decode('utf-8')
    if output.find('finished download') < 0:
        return "download failed"
    else:
    	return "/"+output.split("./")[-1].strip()


def getTZoffset(tzinfo):

    with open(tzfile_name, 'r') as csvfile:
        tzdata=csv.reader(csvfile,delimiter=';')
        for row in tzdata:
            if row[0]==tzinfo:
                return row[1]
            else:
                return 0

def chkLfile(fname):
    fname=fname.replace('/',"\\")
    if not os.access(fname,os.F_OK):
        print ('File not found: ' + fname)
        return False
    else:
        return True


def removeFile(lfile):
    lfile=lfile.replace('/',"\\")
    if os.access(lfile,os.F_OK):
        os.remove(lfile)

def getDataDir():
    base=os.path.basename(__file__)
    folder = os.path.splitext(base)[0] + 'Data'
    full = os.path.dirname(__file__) +  '\\' + folder
    if not os.path.exists(full):
        try:
            os.makedirs(full)
        except OSError:
            print ("Error: cannot create data folder.")
            #quit()
    return folder

datadir = getDataDir()
pfile_name=app_path + '/placesAIFS.csv'
tzfile_name=app_path +'/tzcode.csv'
model='gfs'
timestepmax=192
tmax_init=-999
tmin_init=999
dbOn = False
#dissemination_times=['04:40','10:38','16:10','22:41']

print (' ')
print( '------------------------------------------')
print ('\t' + str(datetime.datetime.now()))
print ('------------------------------------------')
print( ' ')

d=datetime.date.today()
gm=datetime.datetime.utcnow() #

tstart=getTstart(gm)

print ("GFS server date: ",str(gm.year) + "-" + str(gm.month) + "-" + str(gm.day))
print ("GFS server time: ",str(gm.hour) + ':' +  '{:02d}'.format(gm.minute))
print ("Latest valid forecast start time: " + str(tstart))
print ('')

# params=["T","TMAX","TMIN"]
params = ["50T", "500T", "TMAX", "TMIN"]

#params = ["TMP", "RH"]
y=d.year
m=d.month
ddd=d.day

ffile_name=app_path + '/' +  str(gm.year) + '{:02d}'.format(gm.month) + '{:02d}'.format(gm.day) + str(tstart) + 'z.csv'
chkFile(pfile_name)
#pfile=open(pfile_name,'rb')
#plcdata=csv.reader(pfile,delimiter=';')

ffile=open(ffile_name,'w')
#pfile.close

output=csv.writer(ffile,delimiter=';',lineterminator='\n')

fcsteps=[6,12]
stepstarts=[6,252]
stepends=[240,384]
#modelres=['0p25','1p0']
modelres=['0p25','0p25']

##dmin=time2min(dissemination_times[tstarts.index('00')])
##emin =  time2min(str(gm.hour)+':'+str(gm.minute))
##
##if( (tstart=='18') and emin < dmin ) :
##        cdate=str(gm.year) + '{:02d}'.format(gm.month) + '{:02d}'.format(gm.day-1)
##else:
##        cdate=str(gm.year) + '{:02d}'.format(gm.month) + '{:02d}'.format(gm.day)

d=gm
d = d.replace(day=d.day-to_yesterday)
cdate=str(d.year) + '{:02d}'.format(d.month) + '{:02d}'.format(gm.day)
d = d.replace(hour=int(tstart), minute=0,second=0,microsecond=0)


if dbOn:
        try:
            conn = psycopg2.connect("dbname='GFSData' user='postgres' host='localhost' password='Neil1928'")
        except:
            print ("I am unable to connect to the database")
        cur = conn.cursor()

print ("d: " + str(d))

#output.writerow(['Location', 'Forecast_Date', '850_mb','Tmax','Tmin']) # Write headers
fields = ['Location', 'Day', 'Forecast_Date', 'Run', 'Forecast_Hr', '50T', '500T', 'TMAX', 'TMIN']
output.writerow(fields) # Write headers

for i in range(0,len(fcsteps)):
        #print 'i:', i
        for tfcst in range (stepstarts[i],stepends[i]+fcsteps[i],fcsteps[i]):
                print ('tfcst:', tfcst, '--------------------\n')

                dt=datetime.timedelta(hours=fcsteps[i])
                d+=dt
                fetched=False
                waitTime=0 #seconds
                while(not fetched):
                        time.sleep(waitTime)
                        #pfile.seek(0)
                        fname = downloadGrib(str(cdate),tstart,tfcst,fcsteps[i],modelres)
                        with open(pfile_name, "r") as csvfile:
                            plcdata=csv.reader(csvfile,delimiter=';')
                            for row in plcdata:

                                cName=row[0]
                                lat=row[1]
                                lon=row[2]
                                tzinfo=row[3]
                                tzoffset=getTZoffset(tzinfo)
                                print( cName,lat,lon,tzinfo,tzoffset)
                                newday=1
                                dd=d.day
                                cName=cName.replace('.','')

                                lfile=app_path +  fname
                                if chkLfile(lfile):
                                        vals=[]

                                        for p in range(len(params)):
		
                                                vals.append(K2F(get_param(lfile,lon,lat,params[p])))
                                        temp = vals[0]
                                        tmax = vals[1] #if tmax<vals[1] else tmax
                                        tmin = vals[2] #if tmin>vals[2] else tmin
                                        
                                        t50 = vals[0]   # 50 mb Temperature
                                        t500 = vals[1]  # 500 mb Temperature
                                        tmax = vals[2]  # Max Temp at 2m
                                        tmin = vals[3] 

                                        print('50T={:.1f}'.format(t50), '500T={:.1f}'.format(t500), 'TMAX={:.1f}'.format(tmax), 'TMIN={:.1f}'.format(tmin))


                                        offset = int(tzoffset)

                                        if (offset > 0) :
                                                plcd = d + datetime.timedelta(hours=offset)
                                        else :
                                                plcd = d - datetime.timedelta(hours=abs(offset))

                                        print ('UTC:', weekdays[d.weekday()], str(d), ' ', cName,':',weekdays[plcd.weekday()], str(plcd),'\n')

                                        if dbOn:
                                                try:
                                                        cur = conn.cursor()

                                                        try:
                                                                cur.execute("""INSERT INTO datalog(location,dissem,hour,date,tmp,tmax,tmin) VALUES (%(loc)s,%(dis)s,%(hr)s,%(date)s,%(t1)s,%(t2)s,%(t3)s) ;""",{ 'loc':cName,'dis':tstart ,'hr':tfcst ,'date':plcd,'t1': Decimal(temp),'t2': Decimal(tmax), 't3':Decimal(tmin)})
                                                        except psycopg2.IntegrityError:
                                                                conn.rollback()
                                                        else:
                                                                conn.commit()
                                                                cur.close()
                                                except Exception as e:
                                                        print ('ERROR:', e[0])
                                                        quit()
                                        output.writerow([cName, weekdays[plcd.weekday()], plcd.date().strftime("%d/%m/%Y"),
                                                        str(tstart) + 'z', 'f' + '{:03d}'.format(tfcst), '{:.1f}'.format(t50),
                                                        '{:.1f}'.format(t500), '{:.1f}'.format(tmax), '{:.1f}'.format(tmin)])

                                        # output.writerow([cName,weekdays[plcd.weekday()],plcd.date().strftime("%d/%m/%Y"),str(tstart) + 'z','f' + '{:03d}'.format(tfcst),  '{:.1f}'.format(temp) ,'{:.1f}'.format(tmax), '{:.1f}'.format(tmin)])
                                       # print vals
                                        fetched=True
                                        waitTime=0
 

                                else :
                                        print ('chkLfile failed: url is not valid (data not available yet, will wait for ' + str(waitTime/60) +' minute(s)...)')
                                        waitTime=60
                                        break


                        lfile=lfile.replace('/',"\\")
                        if os.access(lfile,os.F_OK):
                            os.remove(lfile)

if dbOn:
        conn.close()
ffile.flush
ffile.close
