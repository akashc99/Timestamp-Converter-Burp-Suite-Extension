import datetime
from burp import IBurpExtender, ITab
from java.io import PrintWriter
from java.lang import RuntimeException
from javax.swing import JPanel, JLabel, JTextField, JButton, JScrollPane, JTextArea

class TimestampConverterTab(ITab):
    def __init__(self, extender):
        self._extender = extender
        self._txtPayload1 = JTextField(20)
        self._txtPayload2 = JTextField(20)
        self._btnConvert = JButton("Convert", actionPerformed=self.convert)
        self._btnClear = JButton("Clear", actionPerformed=self.clear)
        self._txtResult = JTextArea(10,40)
        self._txtResult.setEditable(False)
        
        panel = JPanel()
        panel.add(JLabel("Payload 1:"))
        panel.add(self._txtPayload1)
        panel.add(JLabel("Payload 2:"))
        panel.add(self._txtPayload2)
        panel.add(self._btnConvert)
        panel.add(self._btnClear)
        scrollPane = JScrollPane(self._txtResult)
        panel.add(scrollPane)
        self.component = panel

    def getTabCaption(self):
        return "Timestamp Converter"

    def getUiComponent(self):
        return self.component

    def convert(self, event):
        try:
            payload1 = self._txtPayload1.getText()
            payload2 = self._txtPayload2.getText()
            payload1_time = datetime.datetime.fromtimestamp(int(payload1)).strftime('%Y-%m-%d %H:%M:%S')
            payload2_time = datetime.datetime.fromtimestamp(int(payload2)).strftime('%Y-%m-%d %H:%M:%S')
            self._txtResult.setText("Payload 1: " + payload1_time + "\nPayload 2: " + payload2_time)
        except Exception as e:
            self._extender._callbacks.printError(str(e))
    
    def clear(self, event):
        self._txtResult.setText("")

class BurpExtender(IBurpExtender):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Timestamp Converter")
        callbacks.addSuiteTab(TimestampConverterTab(self))
