# -*- coding: utf-8 -*- 
import os,sys
from WeiBoFans import *
"""
<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.gexf.net/1.2draft http://www.gexf.net/1.2draft/gexf.xsd" version="1.2">
    <meta lastmodifieddate="2009-03-20">
        <creator>Gephi.org</creator>
        <description>A Web network</description>
    </meta>
    <graph defaultedgetype="directed">
        <attributes class="node">
            <attribute id="0" title="url" type="string"/>
            <attribute id="1" title="indegree" type="float"/>
            <attribute id="2" title="frog" type="boolean">
                <default>true</default>
            </attribute>
        </attributes>
        <nodes>
            <node id="0" label="Gephi">
                <attvalues>
                    <attvalue for="0" value="http://gephi.org"/>
                    <attvalue for="1" value="1"/>
                </attvalues>
            </node>
            <node id="1" label="Webatlas">
                <attvalues>
                    <attvalue for="0" value="http://webatlas.fr"/>
                    <attvalue for="1" value="2"/>
                </attvalues>
            </node>
            <node id="2" label="RTGI">
                <attvalues>
                    <attvalue for="0" value="http://rtgi.fr"/>
                    <attvalue for="1" value="1"/>
                </attvalues>
            </node>
            <node id="3" label="BarabasiLab">
                <attvalues>
                    <attvalue for="0" value="http://barabasilab.com"/>
                    <attvalue for="1" value="1"/>
                    <attvalue for="2" value="false"/>
                </attvalues>
            </node>
        </nodes>
        <edges>
            <edge id="0" source="0" target="1"/>
            <edge id="1" source="0" target="2"/>
            <edge id="2" source="1" target="0"/>
            <edge id="3" source="2" target="1"/>
            <edge id="4" source="0" target="3"/>
        </edges>
    </graph>
</gexf>
"""
def GetdataofUser(uid):
	print 'Searching Fans of %s'%uid
	folder1='fansdata_1'
	folder2='fansdata_2'
	folder3='fansdata_3'
	filepath=''
	tmpfilepath=folder1+'/'+uid+'/fans/weibo_fans.html'
	if os.path.exists(tmpfilepath):
		filepath=tmpfilepath
	tmpfilepath=folder2+'/'+uid+'/fans/weibo_fans.html'
	if  os.path.exists(tmpfilepath):
		filepath=tmpfilepath
	tmpfilepath=folder3+'/'+uid+'/fans/weibo_fans.html'
	if  os.path.exists(tmpfilepath):
		filepath=tmpfilepath
	if filepath=='':
		return []
	fans=[]
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

def SearchFans(uid):
	fans=GetdataofUser(uid)
	fansDict={uid:fans}
	for i in fans:
		subfans=GetdataofUser(i.userid)
		fansDict[i.userid]=subfans
	return fansDict




def outputgexf(targetid,targetdict,dictList,keylist):
	fansDict={}
	filename=''
	for (key,value) in targetdict.items():
		fansDict[key]=value
	if dictList==None:
		filename=targetid+'.gexf';
	else:
		for tempdict in dictList:
			for (key,value) in tempdict.items():
				if not fansDict.has_key(key):
					fansDict[key]=value
		filename=targetid+'_'+str(len(dictList))+'.gexf';
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
		size=len(value)
		if size>maxSize:
			maxSize=size
		if size<minSize:
			minSize=size
	max_dispalysize=100.0
	min_displaysize=10.0
	k=(max_dispalysize-min_displaysize)/(maxSize-minSize)

	for (key,value) in fansDict.items():
		nodesIndex[key]=nodeIndex
		if dictList==None:
			nodestr+=nodetemplate%(str(nodeIndex),key,str(k*(len(value)-minSize)+min_displaysize),'100','100','100')
			nodeIndex+=1
			continue
		else:
			if key==targetid:
				nodestr+=nodetemplate%(str(nodeIndex),key,str(k*(len(value)-minSize)+min_displaysize),'0','0','0')
				nodeIndex+=1
				continue
			find=0
			for tempkey in keylist:
				if key==tempkey:
					nodestr+=nodetemplate%(str(nodeIndex),key,str(k*(len(value)-minSize)+min_displaysize),'0','0','0')
					find=1
					break
			if find==1:
				nodeIndex+=1
				continue
			if targetdict.has_key(key):
				find=0
				for tmpdict in dictList:
					if tmpdict.has_key(key):
						nodestr+=nodetemplate%(str(nodeIndex),key,str(k*(len(value)-minSize)+min_displaysize),'255','0','0')
						find=1
						break
				if find==0:
					nodestr+=nodetemplate%(str(nodeIndex),key,str(k*(len(value)-minSize)+min_displaysize),'0','255','255')
				nodeIndex+=1
				continue
			else:
				nodestr+=nodetemplate%(str(nodeIndex),key,str(k*(len(value)-minSize)+min_displaysize),'100','100','100')
				nodeIndex+=1
		

	for (key,value) in fansDict.items():
		for j in value:
			if fansDict.has_key(j.userid):
				edgestr+=edgetemplate%(str(edgeIndex),str(nodesIndex[key]),str(nodesIndex[j.userid]))
				edgeIndex+=1

	file.write(writestr%(str(nodeIndex),nodestr,str(edgeIndex),edgestr))
	file.close()


targetdict={}
targetid='1684211790'
targetdict=SearchFans(targetid)
dictList=[]
keylist=['234518711','1570205385','1032968490','1848347701']
tmpkeylist=[]
outputgexf(targetid,targetdict,None,None)
for key in keylist:
	tmpdict=SearchFans(key)
	dictList.append(tmpdict)
	tmpkeylist.append(key)
	outputgexf(targetid,targetdict,dictList,tmpkeylist)


