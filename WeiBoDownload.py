# -*- coding: utf-8 -*- 
from WeiBoLogin import *
import os
import json
import Queue
import threading
import inspect
import ctypes
import time
import logging   
  


class DownLoadLog(object):
	"""docstring for DownLoadLog"""
	def __init__(self):
		super(DownLoadLog, self).__init__()
		self.writelist = []
		self.loglist=[]
		
	

class WeiBoDownloader(object):
	"""docstring for WeiBoDownloader"""
	def __init__(self, WeiBoInstance,thread_instance=None):
		self.weiboinstance=WeiBoInstance
		self.save_file=0
		self.weibodata=''
		if thread_instance!=None:
			self.thread_instance=thread_instance
		assert self.weiboinstance.login()==True,"Weibo Login Failed"  



	def downloadWeibo(self,targetuserid,downLoad=False,keylist=None,timeout=60):
		global logger
		self.target=targetuserid
		#print '>>>>>>>>>>>>>>>>>>>>>>>'+self.target+'<<<<<<<<<<<<<<<<<<<<<<'
		datablog=self.weiboinstance.resuestpage('http://weibo.com/u/'+targetuserid+'?from=profile&wvr=5&loc=tagweibo',timeout).content
		#print datablog
		if hasattr(self, "thread_instance"):
			self.thread_instance.starttime=time.time()
		findparam=r'<div\saction-type=.{2}feed_list_item.{4}mid=.{2}\d+.{2}.{1,20}class=.{2}WB_feed_type SW_fun.{4}>'
		weibodatalist=re.findall(findparam,datablog)

		if downLoad:
			self.saveDatafile(datablog)
		self.weibodata=datablog
		if keylist!=None:
			self.weiboContentAnalisis(datablog,keylist)




		#print datablog
		weibo_page_num_str=re.findall(r'<strong node-type=\\"weibo\\">\d+<\\/strong>',datablog)
		if len(weibo_page_num_str)==0:
			return
		weibo_page_num=int(re.findall(r'\d+',weibo_page_num_str[0])[0])
		weiboleft=weibo_page_num
		#print datablo
		#http://weibo.com/u/1684211790?from=profile&wvr=5&loc=tagweibo&page=4&pre_page=3&end_id=3583067878801192&end_msign=-1
		ss=str(int(time.time()))

		weiboleft-=15
		if weiboleft<=0:
			return
		weiboid=re.findall(r'mid=\\"\d+\\".{1,17}class=\\"WB_feed_type SW_fun  \\">',datablog)
		if len(weiboid)==0:
			return
		weiboidlist=[]
		for i in weiboid:
			weiboidlist.append(re.findall(r'\d{5,30}',i)[0])
		if len(weiboidlist)<=0:
			return

		end_id=weiboidlist[0]
		_k_value=ss
		body='http://weibo.com/aj/mblog/mbloglist?_wv=5&page=1&count=15&pre_page=1&_k='+_k_value+'&_t=0&max_id='+str(weiboidlist[len(weiboidlist)-1])+'&end_id='+end_id+'&pagebar=0&uid='+self.target+'&__rnd='+ss;
		datablog=self.weiboinstance.resuestpage(body,timeout).content
		if hasattr(self, "thread_instance"):
			self.thread_instance.starttime=time.time()

		obj=json.loads(datablog)
		self.weibodata=obj['data']


		if downLoad:
			self.saveDatafile(datablog)

		if keylist!=None:
			self.weiboContentAnalisis(self.weibodata,keylist)
		weiboleft-=15
		if weiboleft<=0:
			return

		weiboid=re.findall(r'mid=\\"\d+\\".{1,17}class=\\"WB_feed_type SW_fun  \\">',datablog)
		weiboidlist=[]
		for i in weiboid:
			weiboidlist.append(re.findall(r'\d{5,30}',i)[0])

		if len(weiboidlist)<=0:
			return

		body='http://weibo.com/aj/mblog/mbloglist?_wv=5&page=1&count=15&pre_page=1&_k='+_k_value+'&_t=0&max_id='+str(weiboidlist[len(weiboidlist)-1])+'&end_id='+end_id+'&pagebar=1&uid='+self.target+'&__rnd='+ss;
		datablog=self.weiboinstance.resuestpage(body,timeout).content
		if hasattr(self, "thread_instance"):
			self.thread_instance.starttime=time.time()


		obj=json.loads(datablog)
		self.weibodata=obj['data']
		if downLoad:
			self.saveDatafile(datablog)
		if keylist!=None:
			self.weiboContentAnalisis(self.weibodata,keylist)
		weiboleft-=15
		if weiboleft<=0:
			return
		weiboid=re.findall(r'mid=\\"\d+\\".{1,17}class=\\"WB_feed_type SW_fun  \\">',datablog)
		weiboidlist=[]
		for i in weiboid:
			weiboidlist.append(re.findall(r'\d{5,30}',i)[0])
		if len(weiboidlist)<=0:
			return

		weibo_page_num=int(weibo_page_num/45)+1
		logstr= '[Weibo Log]=>UID<%s> Total Weibo pages=%s'%(self.target,str(weibo_page_num))
		print logstr
		logger.info(logstr)  

		for i in range(weibo_page_num-1):
			logstr= '[Weibo Log]=> Thread<'+str(self._get_my_tid())+'>:Request page '+str(i+2)+'/'+str(weibo_page_num)+' of '+self.target
			


			print logstr
			#logger.info(logstr)  
			body='http://weibo.com/u/'+targetuserid+'?from=profile&wvr=5&loc=tagweibo&page='+str(i+2)+'&pre_page='+str(i+1)+'&end_id='+end_id+'&end_msign=-1'
			
			#logger.info(str(i+2)+'/'+str(weibo_page_num)+'=='+body)  
			datablog=self.weiboinstance.resuestpage(body,timeout).content
			if hasattr(self, "thread_instance"):
				self.thread_instance.starttime=time.time()
			if downLoad:
				self.saveDatafile(datablog)
			self.weibodata=datablog
			if keylist!=None:
				self.weiboContentAnalisis(self.weibodata,keylist)

		

			weiboid=re.findall(r'mid=\\"\d+\\".{1,17}class=\\"WB_feed_type SW_fun  \\">',datablog)
			weiboidlist=[]
			for j in weiboid:
				weiboidlist.append(re.findall(r'\d{5,30}',j)[0])
			if len(weiboidlist)<=0:
				continue
			ss=str(int(time.time()))
			#print 'second request analysis index==>'+str(i)



			weiboleft-=15
			if weiboleft<=0:
				break
			body='http://weibo.com/aj/mblog/mbloglist?_wv=5&__rnd='+ss+'&_k='+_k_value+'_t=0&count=15&end_id='+end_id+'&max_id='+str(weiboidlist[len(weiboidlist)-1])+'&page='+str(i+2)+ '&pagebar=0&pre_page='+str(i+2)+'&uid='+self.target
			
			#logger.info(str(i+2)+'/'+str(weibo_page_num)+'=='+body) 
			datablog=self.weiboinstance.resuestpage(body,timeout).content
			if hasattr(self, "thread_instance"):
				self.thread_instance.starttime=time.time()

			obj=json.loads(datablog)
			self.weibodata=obj['data']
			if downLoad:
				self.saveDatafile(datablog)



			if keylist!=None:
				self.weiboContentAnalisis(self.weibodata,keylist)

			weiboid=re.findall(r'mid=\\"\d+\\".{1,17}class=\\"WB_feed_type SW_fun  \\">',datablog)
			weiboidlist=[]
			for j in weiboid:
				weiboidlist.append(re.findall(r'\d{5,30}',j)[0])
			if len(weiboidlist)<=0:
				continue
			


			weiboleft-=15
			if weiboleft<=0:
				break
			body='http://weibo.com/aj/mblog/mbloglist?_wv=5&__rnd='+str(int(time.time()))+'&_k='+_k_value+'_t=0&count=15&end_id='+end_id+'&max_id='+weiboidlist[len(weiboidlist)-1]+'&page='+str(i+2)+ '&pagebar=1&pre_page='+str(i+2)+'&uid='+self.target
			
			#logger.info(str(i+2)+'/'+str(weibo_page_num)+'=='+body) 
			datablog=self.weiboinstance.resuestpage(body,timeout).content
			if hasattr(self, "thread_instance"):
				self.thread_instance.starttime=time.time()

			obj=json.loads(datablog)
			self.weibodata=obj['data']
			if keylist!=None:
				self.weiboContentAnalisis(self.weibodata,keylist)
			if downLoad:
				self.saveDatafile(datablog)


			weiboid=re.findall(r'mid=\\"\d+\\".{1,17}class=\\"WB_feed_type SW_fun  \\">',datablog)
			weiboidlist=[]
			for j in weiboid:
				weiboidlist.append(re.findall(r'\d{5,30}',j)[0])
			if len(weiboidlist)<=0:
				continue

			weiboleft-=15
			if weiboleft<=0:
				break
		logstr= '[Weibo Log]=>'+self.target+' downLoad finish'  
		print logstr
		logger.info(logstr)          



	def weiboContentAnalisis(self,data,keylist):
		#a class=\"S_link2 WB_time\" target=\"_blank\" title=\"2013-06-01 20:38\" 
		# mid=\"3584480822127616\"  class=\"WB_feed_type SW_fun  \">
		global cur_index_folder

		time_search_param=r'a class=\\"S_link2 WB_time\\" target=\\"_blank\\" title=\\"\d{4}-\d{2}-\d{2} \d{2}:\d{2}\\"'
		weibo_detail=r'<div class=\\"WB_detail\\">'
		time_match=re.findall(time_search_param,data)
		detail_match=re.findall(weibo_detail,data)
		len_data=len(time_match)
		search_param=data
		output_data=''
       
		output_file='Cough/cough_'+str(cur_index_folder)
		if os.path.exists(output_file)==False:
			os.mkdir(output_file)
		output_file+='/'+self.target+'.txt'
		for i in range(len_data):
			detail=search_param[search_param.find(detail_match[i]):search_param.find(time_match[i])]
			for j in keylist:
				if detail.find(j)>=0:
					time_str=re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}',time_match[i])[0]
					output_data+=time_str
					output_data+='\n'
					continue
			search_param=search_param[search_param.find(time_match[i])+len(time_match[i]):]
		if output_data!='':
			self.saveDatafile(output_data,output_file)




	def saveDatafile(self,data,filename=''):
		if filename=='':
			if os.path.exists(self.target)==False:
				os.mkdir(self.target)
			filename=self.target+"/weibodata_"+str(self.save_file)+'.html'
		global cur_file_num
		global cur_index_folder
		if os.path.exists(filename)==False:
			cur_file_num+=1
		if cur_file_num>=10000:
			cur_file_num=0
			cur_index_folder+=1
		file_output=open(filename, 'a')
		file_output.write(data)
		file_output.close()
		self.save_file+=1

	def _get_my_tid(self):
		"""determines this (self's) thread id"""
		selfthread= threading.currentThread()
		if not selfthread.isAlive():
			raise threading.ThreadError("the thread is not active")
			# do we have it cached?
		if hasattr(self, "_thread_id"):
			return self._thread_id
		# no, look for it in the _active dict
		
		for tid, tobj in threading._active.items():
			if tobj is selfthread:
				self._thread_id = tid
				return tid



cur_index_folder=1
cur_file_num=0


def _async_raise(tid, exctype):
	if not inspect.isclass(exctype):
		"""raises the exception, performs cleanup if needed"""    
		raise TypeError("Only types can be raised (not instances)")
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# # and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
		raise SystemError("PyThreadState_SetAsyncExc failed")

class searchThread(threading.Thread):
	def __init__(self,targetId,WeiBoInstance,search_keylist):  
		threading.Thread.__init__(self)  
		#self.searcdict = searcdict
		self.weiboinstance=WeiBoInstance
		#self.waitingQuery=waitingQuery
		self.keylist=search_keylist
		#key=waitingQuery.get()
		#self.searcdict[key]=1
		#finddict[key]=1
		self.userid=targetId
		#self.thid=len(finddict)
		self.starttime=time.time()
		self.finish=0


	def run(self):
		self._get_my_tid()
		if self.userid!='':
			global cur_thread_num
			global logger
			try:
				cur_thread_num+=1
				downloadInstabce=WeiBoDownloader(self.weiboinstance)
				downloadInstabce.downloadWeibo(self.userid,False,keylist)
				self.finish=1
				pass
			except Exception, e:
				print e
				logger.info('[Error]=>'+str(e))
			finally:
				cur_thread_num-=1
				pass

			

	def _get_my_tid(self):
		"""determines this (self's) thread id"""
		#if not self.isAlive():
		#	raise threading.ThreadError("the thread is not active")
			# do we have it cached?
		if hasattr(self, "_thread_id"):
			return self._thread_id
		# no, look for it in the _active dict
		for tid, tobj in threading._active.items():
			if tobj is self:
				self._thread_id = tid
				return tid
		self._thread_id=-1
		return self._thread_id
	


def check(searchdict,waitingQuery,folder='Cough',param='cough_'):
	global cur_index_folder
	global cur_file_num
	for i in os.listdir(folder):
		if i.find(param)>=0:
			number=int(i[i.find('_')+1:])
			if cur_index_folder<number:
				cur_index_folder=number
	for j in range(cur_index_folder):
		cur_file_num=0
		for i in os.listdir(folder+'/'+param+str(j+1)):
			#uid=i[0:i.find('.')]
			#finddict[uid]=1
			cur_file_num+=1



	

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
				waitingQuery.put(i)

			fan_file=open(fans_filepath)
			load_num+=1
			if load_num%1000==0:
				print '[File]=>load %s files Finish of:%s'%(str(load_num),fans_folder)
			fanslines=fan_file.readlines()
			for j in fanslines:
				if j.find('uid:')>=0:
					uid=j[j.find(':')+1:j.find('\n')]
					if searchdict.has_key(uid)==False:
						searchdict[uid]=0
						waitingQuery.put(uid)
			fan_file.close()

	
 

 


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
	weiboinstance=WeiBoInstance('微博账号','微博密码')
	assert weiboinstance.login()==True,"Weibo Login Failed" 





	nothingtodo=time.time()
	logger = logging.getLogger()   
	#set loghandler   
	file = logging.FileHandler("test.log")   
	logger.addHandler(file)   
	#set formater   
	#formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")   
	formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")   
	file.setFormatter(formatter)    
	#set log level   
	logger.setLevel(logging.INFO) 






	keylist=['咳嗽','感冒','发热','流感']


	#downloadInstabce=WeiBoDownloader(weiboinstance)
	#downloadInstabce.downloadWeibo('2109298592',False,keylist)

	#sys.exit(0)

	searchdict={}
	finddict={}
	waitingQuery=Queue.Queue()
	check(searchdict,waitingQuery)

	#print('total %s find %s wait %s'%(str(len(searchdict)),str(len(finddict)),str(waitingQuery.qsize() )))
	#y=input("Input: ")

	lastnum=0
	max_thread_num=100
	cur_thread_num=0
	thread_list=[]

	start_time=time.time()
	total_num=len(searchdict)
	finishednum=getfinishnum()
	while True :

		if lastnum==total_num:
			break
		cur_num=len(finddict)
		if lastnum!=cur_num:
			lastnum=cur_num
			logstr= '[Job Count]=>'+str(lastnum)+' of '+str(total_num)+' finish'
			print logstr
			if cur_num>finishednum:
				logger.info(logstr)  
		
		if cur_thread_num>=max_thread_num:
			continue
		#
		#thread_list=[]
		
		targetid=waitingQuery.get()
		finddict[targetid]=1

		if cur_num<finishednum:
			continue

		sth=searchThread(targetid,weiboinstance,keylist)
		thread_list.append(sth) 
		sth.start()
		#sth.join()
	print 'search finish'



