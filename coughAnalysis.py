# -*- coding: utf-8 -*- 
from pyquery import PyQuery as pyq
from datetime import*
import time
import matplotlib.pyplot as pl
import os
import re
from WeiBoFans import *
""" timestructure
tm_year 2011
1  tm_mon   1 - 12 
2  tm_mday   1 - 31 
3  tm_hour   0 - 23 
4  tm_min   0 - 59 
5  tm_sec   0 - 61 
tm_wday weekday   0 - 6 
tm_yday
tm_isdst
"""

def LoadData(analysisDict,analysisResult,analysisResult_day):
	finddict={}
	searchdict={}
	cur_index_folder=1
	finishnum=getfinishnum()
	for i in os.listdir('Cough'):
		if i.find('cough_')>=0:
			number=int(i[i.find('_')+1:])
			if cur_index_folder<number:
				cur_index_folder=number
	for j in range(cur_index_folder):
		cur_file_num=0
		cough_folder='Cough/cough_'+str(j+1)
		for i in os.listdir(cough_folder):
			uid=i[0:i.find('.')]
			cur_file_num+=1
			finddict[uid]=1
			if cur_file_num%1000==0:
				print  '[File] Finish Reading  %s Data From %s'%(str(cur_file_num),cough_folder)
			datttimefile=open(cough_folder+'/'+i,'r')
			datetimeLines=datttimefile.readlines()
			analysisDict['FoundWeibo']+=len(datetimeLines)
			analysisDict['FoundPeople']+=1
			for k in datetimeLines:
				timedata=time.strptime(k[0:k.find('\n')],'%Y-%m-%d %H:%M')
				if analysisResult.has_key(str(timedata.tm_year))==False:
					analysisResult[str(timedata.tm_year)]=[0]*12
					analysisResult[str(timedata.tm_year)][timedata.tm_mon-1]+=1
				else:
					analysisResult[str(timedata.tm_year)][timedata.tm_mon-1]+=1

				if analysisResult_day.has_key(str(timedata.tm_year))==False:
					analysisResult_day[str(timedata.tm_year)]=[0]*366
					analysisResult_day[str(timedata.tm_year)][timedata.tm_yday-1]+=1
				else:
					analysisResult_day[str(timedata.tm_year)][timedata.tm_yday-1]+=1
				
				pass
			datttimefile.close()


	fans_folder_index=1
	for i in os.listdir('Fan'):
		number=int(i[i.find('_')+1:])
		if fans_folder_index<number:
			fans_folder_index=number
	for k in range(fans_folder_index):
		load_num=0
		fans_folder='Fan/fansdata_'+str(k+1)
		for i in os.listdir(fans_folder):
			fans_filepath=fans_folder+'/'+i+'/fans/weibo_fans.html'
			if not os.path.exists(fans_filepath):
				os.rmdir(fans_folder+'/'+i+'/fans')
				if os.path.exists(fans_folder+'/'+i):
					os.rmdir(fans_folder+'/'+i)
				continue
			if searchdict.has_key(i)==False:
				searchdict[i]=1

			fan_file=open(fans_filepath)
			load_num+=1
			if load_num%1000==0:
				print '[File]=>load %s files Finish of:%s'%(str(load_num),fans_folder)
			fanslines=fan_file.readlines()
			for j in range(len(fanslines)):
				if j%7!=0:
					continue
				if fanslines[j].find('<fan>')>=0:

					if j+6>len(fanslines)-1:
						break
					uid=fanslines[j+1]
					weibo=fanslines[j+5]
					uid=uid[uid.find(':')+1:uid.find('\n')]
					weibonum=int(weibo[weibo.find(':')+1:weibo.find('\n')])
					if searchdict.has_key(uid)==False:
						searchdict[uid]=1
						analysisDict['TotalWeibo']+=weibonum
						if len(searchdict)<finishnum:
							analysisDict['SearchedWeibo']+=weibonum
			fan_file.close()
	analysisDict['TotalPeople']=len(searchdict)


def getfinishnum(filename='test.log'):
	f=open(filename,'r')
	line = f.readline()
	finishnum=-1
	while line:
		#print line
		
		if line.find('[Job Count]=>')>=0:
			line=line[line.find('>')+1:]
			finishdata=re.findall(r'\d+',line)
			d=finishdata[0]
			num=int(d)
			if num>finishnum:
				finishnum=num
		line = f.readline()
	f.close()
	return finishnum





if __name__ =='__main__':

	#print getfinishnum()

	#sys.exit(0)

	analysisDict={'TotalWeibo':0,'SearchedWeibo':0,'FoundWeibo':0,'TotalPeople':0,'FoundPeople':0}
	analysisResult={}
	analysisResult_day={}
	LoadData(analysisDict,analysisResult,analysisResult_day)
	print('Search Result   %s Person of Total %s Person \n'%(str(analysisDict['FoundPeople']),str(analysisDict['TotalPeople'])))
	print('Search Result   %s Weibo of Total %s Weibo \n'%(str(analysisDict['SearchedWeibo']),str(analysisDict['TotalWeibo'])))
	print('Search Result %s Count List'%str(analysisDict['FoundWeibo']))
	print('Total Finish People %s'% str(getfinishnum()))

	x=[0]*12
	for i in range(12):
		x[i]=i+1
	pl.figure(1)
	colorlist=['black','blue','red','yellow','green','darkblue','darkgreen','darkcyan','darkred','darkmagenta','brown','darkwhite','cyan','magenta','white']
	j=0
	for (key,value) in analysisResult.items():
		#if key=='2013':
		#	continue
		y=value
		pl.plot(x, y,label=key,color=colorlist[j],linewidth=2)
		j+=1
	pl.ylabel("WeiBo Num")
	pl.xlabel("Time")
	pl.title("Cough Analisis of WeiBo")
	pl.ylim(-1,)
	pl.legend()
	pl.grid() 
	pl.show() 

	x=[0]*366
	for i in range(366):
		x[i]=i+1
	pl.figure(1)
	colorlist=['black','blue','red','yellow','green','darkblue','darkgreen','darkcyan','darkred','darkmagenta','brown','darkwhite','cyan','magenta','white']
	j=0
	for (key,value) in analysisResult_day.items():
		#if key=='2013':
		#	continue
		y=value
		#avgsort(y)
		pl.plot(x, y,label=key,color=colorlist[j],linewidth=2)
		j+=1
	pl.ylabel("WeiBo Num")
	pl.xlabel("Time")
	pl.title("Cough Analisis of WeiBo")
	pl.ylim(-1,)
	pl.legend()
	pl.grid() 
	pl.show() 
