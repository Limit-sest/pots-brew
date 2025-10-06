import dataset

db = dataset.connect('sqlite:///cache.db')
cache = db['cache']


# First db setup
# cache.insert(dict(name='River Water', emoji='💧'))
# cache.insert(dict(name='Magical Leaves', emoji='🍃'))
# cache.insert(dict(name='Condensed Light', emoji='💫'))

discovered = cache.find(id=[1,2,3])

for i in discovered:
  print (i['name'])