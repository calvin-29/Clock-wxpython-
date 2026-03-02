import wx
from .custom import ShapedButton, ShapedLabel, ShapedPanel

class Options(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(wx.BLACK)

        self.up_btn = ShapedButton(self, wx.BLACK, "˄")
        self.number = ShapedLabel(self, wx.BLACK, "00")
        self.down_btn = ShapedButton(self, wx.BLACK, "˅")

        self.sizer.Add(self.up_btn, 1, wx.CENTER)
        self.sizer.Add((0, 0), 1)
        self.sizer.Add(self.number, 2,  wx.CENTER|wx.EXPAND)
        self.sizer.Add((0, 0), 1)
        self.sizer.Add(self.down_btn, 1, wx.CENTER)

        self.up_btn.Bind(wx.EVT_LEFT_DOWN, lambda e: self.change_num("up"))
        self.down_btn.Bind(wx.EVT_LEFT_DOWN, lambda e: self.change_num("down"))

        self.SetSizer(self.sizer)
    
    def change_num(self, type):
        num = self.number.GetLabelText()
        if type == "up":
            if int(num) + 1 < 60:
                num = f"{int(num) + 1:02}"
        else:
            if int(num) - 1 > -1:
                num = f"{int(num) - 1:02}"
        self.number.SetLabel(num)
    
    @property
    def num(self):
        return int(self.number.GetLabelText())

class Timer(ShapedPanel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, wx.BLACK, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        # Main Sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.options_sizer = wx.BoxSizer()
        hr = Options(self)
        min = Options(self)
        sec = Options(self)
        
        self.options_sizer.Add((0,0), 1)
        self.options_sizer.Add(hr, 1, wx.EXPAND|wx.ALL, 10)
        self.options_sizer.Add(min, 1, wx.EXPAND|wx.ALL, 10)
        self.options_sizer.Add(sec, 1, wx.EXPAND|wx.ALL, 10)
        self.options_sizer.Add((0,0), 1)
        self.play_btn = ShapedButton(self, wx.BLACK, "►")

        self.sizer.Add((0,0), 1)
        self.sizer.Add(self.options_sizer, 1, wx.EXPAND|wx.CENTER)
        self.sizer.Add(self.play_btn, 0, wx.CENTER|wx.UP, 30)
        self.sizer.Add((0,0), 1)

        self.SetSizer(self.sizer)
        self.Layout()
