# -*- coding: utf-8 -*-
import time
import datetime
import csv
import rrdtool
import Adafruit_DHT as dht
import os

### User configuration starts here
interval = 60                       #Measuring interval in seconds
rrddbname = 'pimatelogger'          #Name of the RRD Database
sensorname='Livingroom'                 #Sensor Label
sensor = dht.AM2302                 #Sensor Type
pin = 4                             #Data Pin



### Nothing to configure below this line
#Construct some variables
rrdfilename = rrddbname +'.rrd'     #Filename of the RRD Database
path = '/var/lib/pimatelogger'     #Path to the Data Directory
graphpath = path+'/graphs'          #Path to Graph directory

i=0

#Funktionen vorbereiten
def printgraph(a):
    if a == 'temp':
        title = 'Temperatur'
        label = 'in *C'
    elif a == 'humidity':
        title = 'Rel. Luftfeuchtigkeit'
        label = 'in %'

    for plot in ['hourly', 'daily', 'weekly', 'monthly']:
        if plot == 'weekly':
            period = 'w'
        elif plot == 'daily':
            period = 'd'
        elif plot == 'monthly':
            period = 'm'
        elif plot == 'hourly':
            period = 'h'

        ret = rrdtool.graph("/%s%s_%s-%s.png" %(graphpath,rrddbname,a,plot),
                            "--start",
                            "-1%s" %(period),
                            "--title=%s (%s)" %(title,plot),
                            "--vertical-label=%s" %(label),
                            '--watermark=%s' %(st),
                            "-w 800",
                            "--slope-mode",
                            "DEF:%s=%s:%s_%s:AVERAGE" %(a,rrdfilename,rrddbname,a),
                            "LINE1:%s#0000FF:%s_%s" %(a, rrddbname, a))


def printconsgraph():
    for plot in ['hourly', 'daily', 'weekly', 'monthly']:
        if plot == 'weekly':
            period = 'w'
        elif plot == 'daily':
            period = 'd'
        elif plot == 'monthly':
            period = 'm'
        elif plot == 'hourly':
            period = 'h'

        ret = rrdtool.graph("/%s%s_%s_%s.png" %(graphpath,rrddbname,sensorname,plot),
                            "--start",
                            "-1%s" %(period),
                            "--title=Temp and Humidity %s (%s)" %(sensorname,plot),
                            "--vertical-label=Temp. in C",
                            "--right-axis-label=rel. Humidity in %",
                            "--right-axis=1:0",
                            '--watermark=%s (%s)' %(rrddbname,st),
                            "-w 600",
                            "-h 300",
                            "--slope-mode",
                            "DEF:temp=%s:%s_temp:AVERAGE" %(rrdfilename,rrddbname),
                            "DEF:humidity=%s:%s_hum:AVERAGE" %(rrdfilename,rrddbname),
                            "LINE1:temp#0000FF:Temperature",
                            "LINE2:humidity#00FF00:Humidity"
                            )
        os.system ("rm -rf /var/www/graphs")
        os.system ("cp -rf %s/ /var/www/graphs" %(graphpath))



try:
    os.stat(path)
except:
    os.mkdir(path)

try:
    os.stat(graphpath)
except:
    os.mkdir(graphpath)

#RRD-Datenbank anlegen falls sie noch nicht existiert
try:
    with open(rrdfilename): pass
    print "Database found: " + path + "/" + rrdfilename
    i=1
except IOError:
    print "Creating new database: " + path + "/" + rrdfilename
    ret = rrdtool.create("%s" %(rrdfilename),
                         "--step","%s" %(interval),
                         "--start", '0',
                         "DS:%s_temp:GAUGE:2000:U:U" %(rrddbname),
                         "DS:%s_hum:GAUGE:2000:U:U" %(rrddbname),
                         "RRA:AVERAGE:0.5:1:2160",
                         "RRA:AVERAGE:0.5:5:2016",
                         "RRA:AVERAGE:0.5:15:2880",
                         "RRA:AVERAGE:0.5:60:8760")
    i=1



while i!=0:
    h, t = dht.read_retry(sensor, pin)
    st=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

#    with open('test.csv', 'a') as fp:
#        a = csv.writer(fp, delimiter=';')
#        a.writerow([st,str(t),str(h)])

    from rrdtool import update as rrd_update
    ret = rrd_update('%s' %(rrdfilename), 'N:%s:%s' %(t, h));

    print "Creating graphics at " + graphpath
    printgraph('temp')
    printgraph('humidity')
    printconsgraph()

    print st, t, h
    print "Next measurement in %s seconds" %(interval)
    time.sleep(interval)
