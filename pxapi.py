#module for responce 500px
import urllib
import json         

class Photo500mb:
     def __init__(self, urllib2Responce):
         self.body = urllib2Responce.read()
         if Responce.DEBUG:
             print 'start Photo500mb constructor'
         
         for head in urllib2Responce.info().headers:
            if head.find('Content-Type') != -1:
                 self.typeMime = head
            if head.find('Content-Length') != -1:
                 self.lengtByte = head
         #urllib2Responce.close()
                 
     def getBody(self):
        return self.body

     def getLength(self):
        return self.lengtByte

     def getMimeType(self):
         return self.typeMime
         
          

class Responce:
    CONSUMER_KEY = "Bb6rApYNRMd0753N38zXS4vGJ46qEIW7aRSHjG3O"
    URL_API = "https://api.500px.com/v1/photos"
    DEBUG = True
    def __init__(self):
        self.imageCache = []
        self.values = {}
        self.values['consumer_key'] = self.CONSUMER_KEY
        self.page = 1;
        self.values['page'] = self.page
        
    #public
    def setValues(self, values):
        self.values = values
        self.values['consumer_key'] = self.CONSUMER_KEY
        self.values['page'] = self.page
        
    #public
    def setPageNumber(self, pageNum):
        self.page = pageNum
        
    #generate parameters in responce
    #hashParamets - key - parameters | value
    #return string request
    def generateParameters(self):
        self.values['page'] = self.page 
        data = urllib.urlencode(self.values)
        query_string = '?{}'.format(data)
        req = ''.join((self.URL_API, query_string))
        return req
    
    def addCache(self, jsonObj):
        for photo in jsonObj['photos']:
            self.imageCache.append(photo['image_url'])
        

    def jsonLoading(self):
        url = self.generateParameters()
        if self.DEBUG:
             print 'jsonLoading url={}'.format(url) 
        f = urllib.urlopen(url)
        responce = f.read()
        f.close()
        if self.DEBUG:
             print 'jsonLoading responce={}'.format(responce) 
        jsonObj = json.loads(responce)
        self.addCache(jsonObj)
        self.page += 1
        if self.DEBUG:
             print 'jsonLoading page={}'.format(self.page) 

    #public       
    def getNextImage (self):
        if len(self.imageCache) < 1:
            self.jsonLoading()
        urlope = urllib.urlopen(self.imageCache.pop())
        return Photo500mb(urlope)
        
