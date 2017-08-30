# Fabfile to take a spider, split it into equal sizes, run the spider on a list of specified hosts, the collect back the scraped information

from fabric.api import *
from fabric.context_manager import cd
import subprocess
import tarfile

env.hosts

with open("hosts.txt") as lines:
	env.hosts = lines.readlines()

map(str.strip, env.hosts)
print env.hosts

def sayHi():
	run("echo HI!")

def buildWorkerPayload():
	print 'Copying payload...'
	subprocess.Popen("rsync -av --exclude=*/*.json --exclude=*/*.txt --exclude=*/*.pyc ../virtuance_scraper .")
	print 'Creating payload TAR...'
	out = tarfile.open('payload.tar', mode='w')
	try:
		out.add(virtuance_scraper)
	finally:
		out.close()

def initScrapy():
	with cd('/root'):
		sudo("iptables-save > ipt.bak")
		sudo("iptables -F"
		sudo("pip install scrapy")
		put("payload.tar","/root/")
		sudo("tar -xf payload.tar")

def runScrapy():
	with cd('/root'):
		sudo("scrapy crawl virtuance_all_tours -a s=%d -a e=%d",start,end)

	
