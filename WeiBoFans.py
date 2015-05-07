# -*- coding: utf-8 -*- 
from WeiBoLogin import *
import re
import threading 
import os
import Queue



class weibouser(object):
	"""docstring for weibouser"""
	def __init__(self,uid='',uname='',nfans=0,nfollow=0,nweibo=0):
		self.userid=uid
		self.fansnum=nfans
		self.weibonum=nweibo
		self.follow=nfollow
		self.name=uname



	def __str__(self):
		t_str='<fan>\n'
		t_str+='uid:'+self.userid+'\nname:'+self.name+'\nfans:'+str(self.fansnum)+'\nfollow:'+str(self.follow)+'\nweibo:'+str(self.weibonum)+'\n'
		t_str+='</fan>\n'
		return t_str
		
class WeiBoFans(object):
	"""docstring for WeiBoFans"""
	def __init__(self, WeiBoInstance,thread=None):
		self.weiboinstance=WeiBoInstance
		self.savefile=None
		self.fanlist=[]
		#self.weiboinstance.login()
		self.thread=thread

	def getfans(self,targetid,timeout=60):

		self.targetid=targetid
		
		targeturl='http://weibo.com/u/'+targetid
		#print 'starting get fans: id=>'+targetid
		#print targeturl
		target=weibouser()
		targetdata=self.weiboinstance.resuestpage(targeturl,timeout).content
		weibo_num_str=re.findall(r'<strong\snode-type=.{2}weibo.{2}>\d+',targetdata)
		follow_num_str=re.findall(r'<strong node-type=.{2}follow.{2}>\d+',targetdata)
		fans_num_str=re.findall(r'<strong node-type=.{2}fans.{2}>\d+',targetdata)
		name_str=re.findall(r'CONFIG.{2}onick.{2} = .{1}.{1,60}.{1};',targetdata)
		if len(weibo_num_str)==0:
			return
		#print 'create++++++++++++++'+targetid+'+++++++++++++++++'
		target.weibonum=int(weibo_num_str[0][weibo_num_str[0].rfind('>')+1:])
		target.fansnum=int(fans_num_str[0][fans_num_str[0].rfind('>')+1:])
		target.follow=int(follow_num_str[0][follow_num_str[0].rfind('>')+1:])
		target.name=name_str[0][name_str[0].find('=')+3:name_str[0].find(';')-1]
		target.userid=targetid

		fanspagenum=int(target.fansnum/20)+1

		for i in range(fanspagenum):
			if self.thread!=None:
				print '[Fans Log]=>Thread<%s>: Page %s/%s of %s'%(str(self.thread._get_my_tid()),str(i+1),str(fanspagenum),self.targetid)
			else:
				print '[Fans Log]=>Page %s/%s of %s'%(str(i+1),str(fanspagenum),self.targetid)
			fans_page_url='http://weibo.com/'+targetid+'/fans?page=&page='+str(i+1)
			fansdatapage=self.weiboinstance.resuestpage(fans_page_url,timeout).content

			#\"\/u\/
			fans_name_list=re.findall(r'id=\d+\\" href=\\"\\/.{1,40}\\" class=.{2}W_f14 S_func1.{2}>.{1,60}<.{2}a>',fansdatapage)
			fans_follow_list=re.findall(r'<a target=.{2}_blank.{2} href=\\"\\/\d+.{2}follow.{2} >\d+<.{2}a>',fansdatapage)
			fansof_fans_list=re.findall(r'<a target=.{2}_blank.{2} href=\\"\\/\d+.{2}fans.{2} >\d+<.{2}a>',fansdatapage)
			fan_weibo_list=re.findall(r'微博 <a target=.{2}_blank.{2} href=\\"\\/.{1,40}\\" >\d+<.{2}a>',fansdatapage)
			
			#fans_name_list=re.findall(r'href=.{4}u.{2}\d.{2} class=.{2}W_f14 S_func1.{2}>.{1,60}<.{2}a>',fansdatapage)
			num_of_data= len(fan_weibo_list)
			#print 'get fans:'+str(len(fans_name_list))
			#print 'get follow:'+str(len(fans_follow_list))
			#print 'get fansofdan:'+str(len(fansof_fans_list))
			#print 'get weibo:'+str(len(fan_weibo_list))
			for i in range(num_of_data):
				#print fans_name_list[i]
				fan=weibouser()
				fan_id_str=re.findall(r'id=\d+',fans_name_list[i])[0]
				fan.userid=fan_id_str[fan_id_str.find('=')+1:]
				fan.name=re.findall(r'>.{1,60}<',fans_name_list[i])[0]
				fan.name=fan.name[fan.name.find('>')+1:fan.name.find('<')]
				fan.follow=re.findall(r'>\d+<',fans_follow_list[i])[0]
				fan.follow=fan.follow[fan.follow.find('>')+1:fan.follow.find('<')]
				fan.fansnum=re.findall(r'>\d+<',fansof_fans_list[i])[0]
				fan.fansnum=fan.fansnum[fan.fansnum.find('>')+1:fan.fansnum.find('<')]
				fan.weibonum=re.findall(r'>\d+<',fan_weibo_list[i])[0]
				fan.weibonum=fan.weibonum[fan.weibonum.find('>')+1:fan.weibonum.find('<')]
				self.fanlist.append(fan)
				self.saveDatafile(str(fan))
				#print fan
		if self.thread!=None:
			print('[Fans Log]=>Thread<%s>:Get fans of UID<%s> finished'%(str(self.thread._get_my_tid()),self.targetid))
		else:
			print('[Fans Log]=>Get fans of UID<%s> finished'%(self.targetid))


	def saveDatafile(self,data):
		global cur_folder_filenum
		global cur_folder_index
		if cur_folder_filenum>=10000:
			cur_folder_filenum=0
			cur_folder_index+=1
		folder_name='Fan/fansdata_'+str(cur_folder_index)
		if os.path.exists(folder_name)==False:
			os.mkdir(folder_name)
		folder_name+=('/'+self.targetid)
		if os.path.exists(folder_name)==False:
			os.mkdir(folder_name)
		folder_name+=('/fans')
		if os.path.exists(folder_name)==False:
			os.mkdir(folder_name)
			cur_folder_filenum+=1


		


		filename=folder_name+'/weibo_fans.html'
		if self.savefile==None:
			self.savefile=open(filename, 'w')
			print '[Save] %s'%filename
		self.savefile.write(data)
		

	def __del__(self):
		if self.savefile!=None:
			self.savefile.close()
			#print '++++++++++>'+self.target+' handle finish'
		self.fanlist=[]



class searchThread(threading.Thread):
	def __init__(self, waitingQuery,finishDict,WeiBoInstance):  
		threading.Thread.__init__(self)  
		self.weiboinstance=WeiBoInstance
		self.max_search_num=max_search_num
		self.waitingQuery=waitingQuery
		key=waitingQuery.get()
		self.finishDict=finishDict
		self.finishDict[key]=1
		self.userid=key


	def run(self):
		global cur_thread_num
		try:
			self._get_my_tid()
			cur_thread_num+=1
			downloadInstabce=WeiBoFans(self.weiboinstance,self)
			downloadInstabce.getfans(self.userid)
			fanlist=downloadInstabce.fanlist
			for i in fanlist:
				if self.finishDict.has_key(i.userid)==False:
					self.waitingQuery.put(i.userid)
			pass
		except Exception, e:
			print e
		finally:
			cur_thread_num-=1

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
		raise AssertionError("could not determine the thread's id")

last_num=0

 
weiboinstance=None
def getIndexes():
	global cur_folder_index
	global cur_folder_filenum
	cur_folder_index=1
	for i in os.listdir('Fan'):
		number=int(i[i.find('_')+1:])
		if cur_folder_index<number:
			cur_folder_index=number
	cur_folder_filenum=0

	cur_folder_filenum=0
	fans_folder='Fan/fansdata_'+str(cur_folder_index)
	for i in os.listdir(fans_folder):
		fans_filepath=fans_folder+'/'+i+'/fans/weibo_fans.html'
		if not os.path.exists(fans_filepath):
			os.rmdir(fans_folder+'/'+i+'/fans')
			if os.path.exists(fans_folder+'/'+i):
				os.rmdir(fans_folder+'/'+i)
			continue
		cur_folder_filenum+=1
	print 'Folder %d Fie %d'%(cur_folder_index,cur_folder_filenum)
	return cur_folder_index,cur_folder_filenum


def check(waitingQuery,finishDict):
	global cur_folder_index
	global cur_folder_filenum
	cur_folder_index,cur_folder_filenum=getIndexes()
	for k in range(cur_folder_index):
		load_num=0
		cur_folder_filenum=0
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
			cur_folder_filenum+=1
			finishDict[i]=1
			if load_num%1000==0:
				print '[File]=>load %s files Finish of:%s'%(str(load_num),fans_folder)
			fanslines=fan_file.readlines()
			for j in fanslines:
				if j.find('uid:')>=0:
					uid=j[j.find(':')+1:j.find('\n')]
					if finishDict.has_key(uid)==False:
						finishDict[uid]=0
						waitingQuery.put(uid)
			fan_file.close()

def getUserFansList(userid,thread=None):
	global cur_folder_index
	global cur_folder_filenum
	#if cur_folder_index==1:
	#cur_folder_index,cur_folder_filenum=getIndexes()
	filepath=''
	for i in range(cur_folder_index):
		folder_name='Fan/fansdata_'+str(i+1)
		fans_filepath=folder_name+'/'+userid+'/fans/weibo_fans.html'
		if os.path.exists(fans_filepath):
			filepath=fans_filepath
			break
	fans=[]
	if filepath!='':
		file=open(filepath,'r')
		lines=file.readlines()
		for i in range(len(lines)):
			if i%7==0:
				if i+7>=len(lines):
					break
				uidLine=lines[i+1]
				unameLine=lines[i+2]
				nfansLine=lines[i+3]
				nfollowLine=lines[i+4]
				nweiboLine=lines[i+5]
				uid=uidLine[uidLine.find(':')+1:uidLine.find('\n')]
				uname=unameLine[unameLine.find(':')+1:unameLine.find('\n')]
				nfans=int(nfansLine[nfansLine.find(':')+1:nfansLine.find('\n')])
				nfollow=int(nfollowLine[nfollowLine.find(':')+1:nfollowLine.find('\n')])
				nweibo=int(nweiboLine[nweiboLine.find(':')+1:nweiboLine.find('\n')])
				fan=weibouser(uid,uname,nfans,nfollow,nweibo)
				fans.append(fan)
		file.close()
		return fans
	else:
		return []

		global weiboinstance
		if weiboinstance==None:
			weiboinstance=WeiBoInstance('zh79325@163.com','a08122419')
			assert weiboinstance.login()==True,"Weibo Login Failed"
		downloadInstabce=WeiBoFans(weiboinstance,thread)
		downloadInstabce.getfans(userid)
		fans=downloadInstabce.fanlist
		return fans

def WeiBoLogIn():
	global weiboinstance
	if weiboinstance==None:
		weiboinstance=WeiBoInstance('微博账号','微博密码')
		assert weiboinstance.login()==True,"Weibo Login Failed"
	return True

if __name__ =='__main__':
	cur_folder_index=1
	cur_folder_filenum=0
	searchdict={}
	waitingQuery=Queue.Queue()
	waitingQuery.put('1848347701')
	waitingQuery2=Queue.Queue()
	finishDict={}
	print 'Start Check...'
	check(waitingQuery2,finishDict)
	print 'Check Finish...'

	weiboinstance=WeiBoInstance('zh79325@163.com','a08122419')
	assert weiboinstance.login()==True,"Weibo Login Failed" 
	#downloadInstabce=WeiBoFans(weiboinstance)



	#searchdict={'1684211790':0}
	max_search_num=100000
	max_thread_num=30
	cur_thread_num=0
	finishnum=0
	while len(finishDict)<max_search_num:
		if cur_thread_num>=max_thread_num:
			continue
		if waitingQuery.empty():
			continue
		sth=searchThread(waitingQuery,finishDict,weiboinstance)
		sth.start()
		finishnum+=1
		if finishnum%100==0:
			print'|||||||||||||||||||||%s||||||||||||||||||||||'%str(finishnum)
	print 'Finish Search'
	#	pass
	#downloadInstabce.getfans('3399705192')


