# Embedded file name: /usr/lib/enigma2/python/Components/ResourceManager.py


class ResourceManager:

    def __init__(self):
        self.resourceList = {}

    def addResource(self, name, resource):
        print '[ResourceManager] adding Resource', name
        self.resourceList[name] = resource
        print '[ResourceManager] resources:', self.resourceList

    def getResource(self, name):
        if not self.hasResource(name):
            return None
        else:
            return self.resourceList[name]

    def hasResource(self, name):
        return self.resourceList.has_key(name)

    def removeResource(self, name):
        if self.hasResource(name):
            del self.resourceList[name]


resourcemanager = ResourceManager()