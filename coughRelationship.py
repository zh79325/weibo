# -*- coding: utf-8 -*- 
import os,sys
from WeiBoFans import *


class AnalsearchThread(threading.Thread):
	def __init__(self, target,fansDict):  
		threading.Thread.__init__(self)  
		self.userid=target
		self.fansDict=fansDict

	def run(self):
		global cur_thread_num
		try:
			self._get_my_tid()
			uid=self.userid
			fans=getUserFansList(uid,self)
			if len(fans)>0:
				self.fansDict[uid]=fans
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


def SearchFans():
	finddict={}
	valueDict={}
	cur_index_folder=1
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
			if cur_file_num%1000==0:
				print  '[File] Finish Reading  %s Data From %s'%(str(cur_file_num),cough_folder)
			datttimefile=open(cough_folder+'/'+i,'r')
			datetimeLines=datttimefile.readlines()
			datttimefile.close()
			finddict[uid]=1
			valueDict[uid]=len(datetimeLines)
	global cur_thread_num
	max_thread_num=1000
	fansDict={}
	finishnum=0
	WeiBoLogIn()
	getIndexes()
	print 'Start Anal'
	for (key,value) in finddict.items():
		while cur_thread_num>max_thread_num:
			pass
		thread=AnalsearchThread(key,fansDict)
		thread.start()
		finishnum+=1
		if finishnum%1000==0:
			print '[Anal Log] %d of %d Finished'%(finishnum,len(finddict))
	while cur_thread_num>0:
		pass
	return fansDict,valueDict




def outputgexf(NodeDict,valueDict):
	fansDict=NodeDict
	filename='Cough.gexf';
	file=open(filename,'w')
	writestr="""<?xml version="1.0" encoding="UTF-8"?>
	<gexf xmlns:viz="http:///www.gexf.net/1.1draft/viz" version="1.1" xmlns="http://www.gexf.net/1.1draft">
		<meta lastmodifieddate="2010-03-31+18:43">
			<creator>Gephi 0.7</creator>
		</meta>
		<graph defaultedgetype="directed" idtype="string" type="static">
			<attributes class="node" mode="static">
				<attribute id="modularity_class" title="Modularity Class" type="integer"/>
			</attributes>
			<nodes count="%s">
	%s
			</nodes>
			<edges count="%s">
	%s
			</edges>
		</graph>
	</gexf>
	"""
	nodetemplate="""			<node id="%s" label="%s">
					<attvalues>
						<attvalue for="modularity_class" value="0"/>
					</attvalues>
					<viz:size value="%s"/>
					<viz:color b="%s" g="%s" r="%s"/>
				</node>"""
	edgetemplate="""			<edge id="%s" source="%s" target="%s"/>\n"""
	nodestr=''
	edgestr=''


	edgeIndex=0
	nodesIndex={}
	nodeIndex=0
	maxSize=0
	minSize=100000000
	for (key,value) in fansDict.items():
		size=valueDict[key]
		if size>maxSize:
			maxSize=size
		if size<minSize:
			minSize=size
	max_dispalysize=100.0
	min_displaysize=10.0
	k=(max_dispalysize-min_displaysize)/(maxSize-minSize)

	for (key,value) in fansDict.items():
		nodesIndex[key]=nodeIndex
		nodestr+=nodetemplate%(str(nodeIndex),key,str(k*(valueDict[key]-minSize)+min_displaysize),'100','100','100')
		nodeIndex+=1
		
	print 'len fansDict %d len NodeDict %d'%(len(fansDict),len(NodeDict))

	for (key,value) in fansDict.items():
		for j in value:
			if fansDict.has_key(j.userid):
				edgestr+=edgetemplate%(str(edgeIndex),str(nodesIndex[key]),str(nodesIndex[j.userid]))
				edgeIndex+=1

	file.write(writestr%(str(nodeIndex),nodestr,str(edgeIndex),edgestr))
	file.close()


if __name__ =='__main__':
	cur_thread_num=0
	finddict,valueDict=SearchFans()
	outputgexf(finddict,valueDict)