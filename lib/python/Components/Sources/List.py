# Embedded file name: /usr/lib/enigma2/python/Components/Sources/List.py
from Source import Source
from Components.Element import cached

class List(Source, object):

    def __init__(self, list = None, enableWrapAround = False, item_height = 25, fonts = None):
        if not list:
            list = []
        if not fonts:
            fonts = []
        Source.__init__(self)
        self.__list = list
        self.onSelectionChanged = []
        self.item_height = item_height
        self.fonts = fonts
        self.disable_callbacks = False
        self.enableWrapAround = enableWrapAround
        self.__style = 'default'

    def setList(self, list):
        self.__list = list
        self.changed((self.CHANGED_ALL,))

    list = property(lambda self: self.__list, setList)

    def entry_changed(self, index):
        if not self.disable_callbacks:
            self.downstream_elements.entry_changed(index)

    def modifyEntry(self, index, data):
        self.__list[index] = data
        self.entry_changed(index)

    def count(self):
        return len(self.__list)

    def selectionChanged(self, index):
        if self.disable_callbacks:
            return
        for x in self.downstream_elements:
            if x is not self.master:
                x.index = index

        for x in self.onSelectionChanged:
            x()

    @cached
    def getCurrent(self):
        return self.master is not None and self.master.current

    current = property(getCurrent)

    def setIndex(self, index):
        if self.master is not None:
            self.master.index = index
            self.selectionChanged(index)
        return

    @cached
    def getIndex(self):
        if self.master is not None:
            return self.master.index
        else:
            return
            return

    setCurrentIndex = setIndex
    index = property(getIndex, setIndex)

    def selectNext(self):
        if self.getIndex() + 1 >= self.count():
            if self.enableWrapAround:
                self.index = 0
        else:
            self.index += 1
        self.setIndex(self.index)

    def selectPrevious(self):
        if self.getIndex() - 1 < 0:
            if self.enableWrapAround:
                self.index = self.count() - 1
        else:
            self.index -= 1
        self.setIndex(self.index)

    @cached
    def getStyle(self):
        return self.__style

    def setStyle(self, style):
        if self.__style != style:
            self.__style = style
            self.changed((self.CHANGED_SPECIFIC, 'style'))

    style = property(getStyle, setStyle)

    def updateList(self, list):
        old_index = self.index
        self.disable_callbacks = True
        self.list = list
        self.index = old_index
        self.disable_callbacks = False