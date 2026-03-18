import wx
from wx.lib.scrolledpanel import ScrolledPanel
import pathlib

class LapRecord(wx.Panel):
    lap = 1

    def __init__(self, parent, time, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.SetBackgroundColour(wx.BLACK)

        self.sizer = wx.BoxSizer()
        self.font = wx.Font(17, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, faceName="Verdana")

        self.count_lbl = wx.StaticText(self, label=f"Lap {self.lap}")
        self.count_lbl.SetFont(self.font)
        self.count_lbl.SetForegroundColour(wx.WHITE)

        self.time = wx.StaticText(self, label=f"{time}", style=wx.ALIGN_RIGHT)
        self.time.SetFont(self.font)
        self.time.SetForegroundColour(wx.WHITE)

        self.sizer.Add(self.count_lbl, 1, wx.EXPAND)
        self.sizer.Add(self.time, 1, wx.EXPAND)

        self.SetSizer(self.sizer)

class StopWatch(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour("#363232")

        self.num = 0
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.font = wx.Font(50, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, faceName="JetBrains Mono")

        # Create label
        self.label = wx.StaticText(self, label="00:00.00", style=wx.ALIGN_CENTER)
        self.label.SetForegroundColour(wx.WHITE)
        self.label.SetFont(self.font)
        
        # create panel for lap record
        self.lap_record = ScrolledPanel(self)
        self.lap_record.SetBackgroundColour(wx.BLACK)
        self.lap_sizer = wx.BoxSizer(wx.VERTICAL)

        self.lap_record.SetSizer(self.lap_sizer)
        self.lap_record.SetupScrolling()

        #create buttons
        self.btn_sizer = wx.BoxSizer()
        main_path = pathlib.Path(__file__).resolve()
        
        pause_icon = str(main_path.parent.parent/'images'/'pause2.png')
        img = wx.Image(pause_icon, wx.BITMAP_TYPE_ANY)
        img = img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH)
        pause = wx.Bitmap(img)

        play_icon = str(main_path.parent.parent/'images'/'play2.png')
        img = wx.Image(play_icon, wx.BITMAP_TYPE_ANY)
        img = img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH)
        play = wx.Bitmap(img)

        reset_icon = str(main_path.parent.parent/'images'/'reset2.png')
        img = wx.Image(reset_icon, wx.BITMAP_TYPE_ANY)
        img = img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH)
        reset_b = wx.Bitmap(img)

        img = wx.Image(reset_icon, wx.BITMAP_TYPE_ANY)
        img = img.Scale(40, 40, wx.IMAGE_QUALITY_HIGH)
        img = img.Rotate180()
        lap_b = wx.Bitmap(img)

        self.pause_btn = wx.BitmapButton(self, -1, pause, style=wx.BORDER_NONE)
        self.pause_btn.Bind(wx.EVT_BUTTON, self.pause_f)
        self.pause_btn.SetToolTip("Pause")

        self.reset_btn = wx.BitmapButton(self, -1, reset_b, style=wx.BORDER_NONE)
        self.reset_btn.Bind(wx.EVT_BUTTON, self.reset)
        self.reset_btn.SetToolTip("Reset")
        
        self.lap_btn = wx.BitmapButton(self, -1, lap_b, style=wx.BORDER_NONE)
        self.lap_btn.Bind(wx.EVT_BUTTON, self.lap)
        self.lap_btn.SetToolTip("Lap")

        self.start_btn = wx.BitmapButton(self, -1, play, style=wx.BORDER_NONE)
        self.start_btn.Bind(wx.EVT_BUTTON, self.play_f)
        self.start_btn.SetToolTip("Play")

        self.reset_btn.Disable()
        self.lap_btn.Disable()
        self.pause_btn.Hide()

        self.btn_sizer.Add(self.reset_btn, 1, wx.EXPAND)
        self.btn_sizer.Add(self.pause_btn, 1, wx.EXPAND)
        self.btn_sizer.Add(self.start_btn, 1, wx.EXPAND)
        self.btn_sizer.Add(self.lap_btn, 1, wx.EXPAND)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)

        self.main_sizer.Add(self.label, 1, wx.EXPAND)
        self.main_sizer.Add(self.lap_record, 4, wx.EXPAND)
        self.main_sizer.Add(self.btn_sizer, 1, wx.EXPAND)
        self.SetSizer(self.main_sizer)

    def OnTimer(self, e):
        self.num += 1
        
        msec = self.num % 100
        sec = (self.num // 100) % 60
        min = (self.num // 6000) % 60

        self.label.SetLabel(f"{min:02}:{sec:02}.{msec:02}")
        self.Layout()
    
    def play_f(self, e):
        self.timer.Start(10)
        self.pause_btn.Show()
        self.start_btn.Hide()
        self.lap_btn.Enable()
        self.reset_btn.Disable()
        
    def pause_f(self, e):
        self.timer.Stop()
        self.pause_btn.Hide()
        self.start_btn.Show()
        self.lap_btn.Disable()
        self.reset_btn.Enable()

    def reset(self, e): 
        self.timer.Stop()
        self.label.SetLabel("00:00.00")
        self.lap_btn.Disable()
        self.lap_record.DestroyChildren()
        self.reset_btn.Disable()
        self.main_sizer.Layout()
        self.num = 0
        LapRecord.lap = 1
    
    def lap(self, e):
        self.lap_sizer.Add(LapRecord(self.lap_record, self.label.GetLabel()), 0, wx.EXPAND|wx.ALL, 10)
        LapRecord.lap += 1
