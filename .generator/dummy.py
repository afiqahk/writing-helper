import yaml
import pathlib
import pprint
pp = pprint.PrettyPrinter(indent=4)

doc = ".template"
chapter = "abc"

path = pathlib.Path() / doc / "_toc.yaml"
print(path)
with open(path, 'r') as f:
    toc = yaml.load(f, Loader=yaml.FullLoader)

pp.pprint(toc)
print()
toc = toc["chapters"]
pp.pprint(toc)
print()

res = next((sub for sub in toc if sub['title'] == chapter), None)
print(res)
print()

import itertools

class dummy:
    def __init__(self, a):
        self.a = a
        self.counter = 0
        return

    def read(self):
        res = self.a[self.counter:self.counter+1]
        if not res:
            raise Exception("Finished iterating")
        self.counter +=1
        return res[0]

d = dummy(res['parts'])
print(d.read())
print(d.read())
print(d.read())