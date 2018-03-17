import os
import sys
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
from urlparse import urljoin
import argparse
import random
from termcolor import colored

def genrandomname(url):
       completestr = 'azertyuiopmlkjhgfdsqwxcvbn0123456789'
       parsed = urlparse(url)
       randomstr = ''
       j = 0
       while j < 10:
              i = random.randint(0, len(completestr) - 1)
              randomstr += completestr[i]
              j += 1
       randomname = parsed.netloc + '_' + randomstr
       return randomname

def touch(path):
       os.mknod(path)

def addLine(f, l):
       with open(f, 'r') as of:
              c = of.read()
       if len(c) > 0:
              c += '\n' + l
       else:
              c += l
       with open(f, 'w') as of:
              of.write(c)

def canbeadded(url):
       rx = True
       j = 0
       limit = len(expaths)
       while j < limit:
              path = expaths[j]
              if len(path) < len(url):
                     i = 0
                     test = True
                     while i < len(path):
                            if path[i] != url[i]:
                                   test = False
                            i = i + 1
                     if test == True:
                            rx = False
              j = j + 1
       return rx
def trueurl(url):
       char = '#'
       if char in url:
              ps = url.split(char)
              rx = ps[0]
       else:
              rx = url
       return rx
def InScope(url):
       parsed = urlparse(url)
       if parsed.netloc == netlocation:
              return True
       else:
              return False
def isinternal(url):
       parsed = urlparse(url)
       if parsed.scheme == '':
              return True
       else:
              return False
def getstatuscode(url):
       r = requests.get(url, headers = headers, allow_redirects=False)
       statuscode = str(r.status_code)
       return statuscode
def extractx(url):
       parsed = urlparse(url)
       basepath1 = parsed.scheme + '://' + parsed.netloc + '/'
       pathx = parsed.path
       pathy = pathx.split('/')
       ex = pathy[len(pathy) - 1]
       basepath2 = parsed.scheme + '://' + parsed.netloc + pathx
       basepath2 = basepath2.replace(ex, "")
       r = requests.get(url, headers = headers)
       html_doc = r.content
       soupx = BeautifulSoup(html_doc, 'html.parser')
       out = []
       for a in soupx.findAll('a'):
              atostring = a.encode('utf-8')
              if 'href' in atostring:
                     try:
                            href = a.attrs['href']
                     except Exception:
                            sdjfosidf = 0
                     hreftostring = href.encode('utf-8')
                     IsAbsolute = False
                     if isinternal(hreftostring) == True:
                            if len(hreftostring) > 0:
                                   if hreftostring != '/':
                                          if hreftostring != '//':
                                                 while hreftostring[0] == '/':
                                                        IsAbsolute = True
                                                        hreftostring = hreftostring[1:]
                                                 if IsAbsolute == True:
                                                        hreftostring = urljoin(basepath1, hreftostring)
                                                 else:
                                                        hreftostring = urljoin(basepath2, hreftostring)
                     if InScope(hreftostring) == True:
                            hreftostring = trueurl(hreftostring)
                            out.append(hreftostring)
       for form in soupx.findAll('form'):
              formtostring = form.encode('utf-8')
              if 'action' in formtostring:
                     action = form.attrs['action']
                     actiontostring = action.encode('utf-8')
                     IsAbsolute = False
                     if isinternal(actiontostring) == True:
                         if len(hreftostring) > 0:
                            if actiontostring != '/':
                                   if actiontostring != '//':
                                          while actiontostring[0] == '/':
                                                 IsAbsolute = True
                                                 actiontostring = actiontostring[1:]
                                          if IsAbsolute == True:
                                                 actiontostring = urljoin(basepath1, actiontostring)
                                          else:
                                                 actiontostring = urljoin(basepath2, actiontostring)
                     if InScope(actiontostring) == True:
                            actiontostring = trueurl(actiontostring)
                            out.append(actiontostring)
       count = len(out)
       j = 0
       limit = 0
       out2 = []
       while j < count:
              ee = out[j]
              i = 0
              duplicate = False
              while i < limit:
                     if ee == out2[i]:
                            duplicate = True
                     i = i + 1
              if duplicate == False:
                     out2.append(ee)
              limit = len(out2)
              j = j + 1
       return out2
                     
def tab2tab(entry):
       l = len(entry)
       i = 0
       back = []
       while i < l:
              x = extractx(entry[i])
              ll = len(x)
              j = 0
              while j < ll:
                     back.append(x[j])
                     j = j + 1
              i = i + 1
       returnx = []
       limit = 0
       k = 0
       count = len(back)
       while k < count:
              duplicate = False
              ee = back[k]
              kk = 0
              while kk < limit:
                     if ee == returnx[kk]:
                            duplicate = True
                     kk = kk + 1
              if duplicate == False:
                     returnx.append(ee)
              limit = len(returnx)
              k = k + 1
       return returnx

def crawlx(go, level):
       global crawled
       imge = []
       if level < depth:
              if len(go) > 0:
                     gocount = len(go)
                     k = 0
                     while k < gocount:
                            scode = getstatuscode(go[k])
                            if int(scode) >= 200 and int(scode) < 300:
                                    if int(scode) == 200:
                                           addLine(file200, go[k])
                                    scode = colored(scode, 'green')
                            elif int(scode) >= 300 and int(scode) < 400:
                                    if int(scode) == 301:
                                           addLine(file301, go[k])
                                    if int(scode) == 302:
                                           addLine(file302, go[k])
                                    scode = colored(scode, 'yellow')
                            elif int(scode) >= 400 and int(scode) < 500:
                                    if int(scode) == 404:
                                           addLine(file404, go[k])
                                    scode = colored(scode, 'red')
                            string = "['" + colored(go[k], 'blue') + "', '" + scode + "']"
                            addLine(gfile, string)
                            crawled.append(go[k])
                            print string
                            k = k + 1
                     count = len(crawled)
                     back = tab2tab(go)
                     backcount = len(back)
                     i = 0
                     while i < backcount:
                            new = True
                            j = 0
                            while j < count:
                                   if back[i] == crawled[j]:
                                          new = False
                                   j = j + 1
                            if new == True:
                                   imge.append(back[i])
                            i = i + 1
                     level = level + 1
                     crawlx(imge, level)
              else:
                     end_message1 = 'FINISHED'
                     print end_message1
       else:
              end_message2 = 'MAX DEPTH'
              print end_message2

description = ''
parser = argparse.ArgumentParser(description=description)
parser.add_argument('-u','--url', help='start url', required=True)
parser.add_argument('-n','--name', help='the target name', default='')
parser.add_argument('-d','--depth', help='the depth/level', default=10)
args = vars(parser.parse_args())

url = args['url']
targetname = args['name']
if len(targetname) == 0:
      targetname = genrandomname(url)
depth = args['depth']
depth = int(depth)
useragents = []
with open('user-agents.txt', 'r') as uas:
         for ua in uas:
                  ua = ua.strip()
                  useragents.append(ua)
#useragent = 'Mozilla/5.0 (X11; Linux i686; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4'
useragent = useragents[random.randint(0, len(useragents) - 1)]
headers = {
         'User-Agent': useragent
}
gfile = 'targets/' + targetname + '/all.txt'
file200 = 'targets/' + targetname + '/200.txt'
file404 = 'targets/' + targetname + '/404.txt'
file301 = 'targets/' + targetname + '/301.txt'
file302 = 'targets/' + targetname + '/302.txt'
if not os.path.exists('targets'):
       os.makedirs('targets')
directory = 'targets/' + targetname
if os.path.isdir(directory) == False:
       os.makedirs(directory)
else:
       try:
              os.remove(gfile)
              os.remove(file200)
              os.remove(file404)
              os.remove(file301)
              os.remove(file302)
       except Exception:
              pass

parsed = urlparse(url)
netlocation = parsed.netloc

touch(gfile)
touch(file200)
touch(file404)
touch(file301)
touch(file302)
go = []
go.append(url)
crawled = []
try:
       crawlx(go, 0)
except KeyboardInterrupt:
       print 'terminated by the user ..'
