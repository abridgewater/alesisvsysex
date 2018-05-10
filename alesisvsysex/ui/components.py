from PyQt5.QtWidgets import *
from alesisvsysex.protocol.types import AbstractEnumValue, IntValue
from alesisvsysex.protocol.model import AlesisV, CompoundComponent, BasicComponent
from alesisvsysex.ui.values import *

class BasicWidget (QGroupBox):
    
    def __init__(self, parent, name, component_key):
        super().__init__(name, parent)
        self.componentName = name
        self.componentKey = component_key
        self.children = []
        self.childNames = []
        self.createChildren()
        self.initLayout()

    def addChild(self, fieldName, fieldValue):
        self.childNames.append(fieldName)
        self.children.append(fieldValue)

    def createChildren(self):
        for field, cls, _ in self.getModel()._PARAMS:
            fieldName = QLabel(field)
            if issubclass(cls, IntValue):
                fieldValue = IntegerSelector(self, field)
            elif issubclass(cls, AbstractEnumValue):
                fieldValue = EnumSelector(self, field)
            self.addChild(fieldName, fieldValue)

    def initLayout(self):
        layout = QFormLayout()
        for fieldName, fieldValue in zip(self.childNames, self.children):
            layout.addRow(fieldName, fieldValue)
        self.setLayout(layout)
        
    def updateState(self):
        for c in self.children:
            c.updateState()
    
    def getModel(self):
        return getattr(self.parent().getModel(), self.componentKey)

class CompoundWidget (QGroupBox):
    
    def __init__(self, parent, name, component_key):
        if name is not None:
            super().__init__(name, parent)
        else:
            super().__init__(parent)
        self.componentName = name
        self.componentKey = component_key
        self.children = []
        self.createChildren()
        self.initLayout()

    def addChild(self, widget):
        self.children.append(widget)

    def createChildren(self):
        for name, _, __ in self.getModel()._COMPONENTS:
            model = self.getModel()._components[name]
            if isinstance(model, BasicComponent):
                widget = BasicWidget(self, name, name)
            elif isinstance(model, CompoundComponent):
                widget = CompoundWidget(self, name, name)
            self.addChild(widget)

    def initLayout(self):
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        for widget in self.children:
            layout.addWidget(widget)
        self.setLayout(layout)

    def updateState(self):
        for c in self.children:
            c.updateState()

    def getModel(self):
        return getattr(self.parent().getModel(), self.componentKey)

