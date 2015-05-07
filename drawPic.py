# -*- coding: utf-8 -*- 
from pyquery import PyQuery as pyq
from datetime import*
import matplotlib.pyplot as pl

datafile = open('weibodata.txt')
lines=datafile.readlines()
datalist=[]
for i in lines:
	datalist.append(datetime.strptime(i[0:i.find('\n')],'%Y-%m-%d %H:%M'))
waitetimevector=[]
datalist.sort()
for i in range(len(datalist)-1):
	delta=datalist[i+1]-datalist[i]
	utc = delta.days * 1440 + delta.seconds/60
	if utc==38928:
		print '>>>>>>>>>'
		print datalist[i]
		print datalist[i+1]
	waitetimevector.append(utc)
waitetimevector.sort()
minwaittime=waitetimevector[0]
if minwaittime==0:
	minwaittime=2
maxwaittime=waitetimevector[len(waitetimevector)-1]
print 'minwaittime:'+str(minwaittime)
print 'maxwaittime:'+str(maxwaittime)
vectorxnum=int(maxwaittime/minwaittime)+1
x=[0]*vectorxnum
y=[0]*vectorxnum
for i in range(vectorxnum):
	x[i]=i*minwaittime
for i in range(len(waitetimevector)):
	y[int(waitetimevector[i]/minwaittime)]+=1
pl.figure(1)
pl.plot(x[0:50], y[0:50],label="send",color="red",linewidth=2)
pl.ylabel("WeiBo Num")
pl.xlabel("Time")
pl.title("Day Analisis of WeiBo")
pl.ylim(-1,)
#pl.legend()
pl.grid() 
pl.show() 