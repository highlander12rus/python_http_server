#module for responce 500px
import urllib2
import json         

class Photo500mb:
     def __init__(self, urllib2Responce):
         self.body = urllib2Responce.read()
         
         for head in urllib2Responce.info().headers:
            if head.find('Content-Type') != -1:
                 self.lengtByte = head
            if head.find('Content-Length') != -1:
                 self.typeMime = head
         urllib2Responce.close()
                 
     def getBody(self):
        return self.body

     def getLength(self):
        return int(self.lengtByte)

     def getMimeType(self):
         return self.typeMime
         
          

class Responce:
    CONSUMER_KEY = "Bb6rApYNRMd0753N38zXS4vGJ46qEIW7aRSHjG3O"
    URL_API = "https://api.500px.com/v1/photos"
    
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
        data = urllib.urlencode(self.values)
        req = urllib2.Request(self.URL_API, data)
        return req
    
    def addCache(self, jsonObj):
        for photo in jsonObj['photos']:
            self.imageCache.append(photo['image_url'])
        

    def jsonLoading(self):
        url = self.generateParameters()
        with urllib2.urlopen() as f:
            responce = f.read()
            jsonObj = json.loads(responce)

    #public       
    def getNextImage (self):
        if len(self.imageCache) == 0:
            self.jsonLoading()
        self.page += 1
        urlope = urllib2.urlopen(self.imageCache.pop())
        return Photo500mb(urlope)
        
