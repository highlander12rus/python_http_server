import pxapi

resClass = pxapi.Responce()
options = {}
options['feature'] = 'popular'
resClass.setValues(options)
lol = resClass.getNextImage()

for i in range(1, 25):
 print "image length= {}".format(lol.getLength())
 lol = resClass.getNextImage()
print "end"
