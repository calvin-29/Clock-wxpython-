import wx
from .custom import ShapedButton, ShapedLabel, ShapedPanel
from .clock import RotatePanel
import pathlib

class Options(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, style=wx.WANTS_CHARS, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        color = wx.Colour(50, 150, 50)
        self.SetBackgroundColour(color)
        self.is_selected = False

        self.up_btn = ShapedButton(self, "˄")
        self.number = ShapedLabel(self, color, "00")
        self.down_btn = ShapedButton(self, "˅")

        self.sizer.Add(self.up_btn, 1, wx.CENTER|wx.UP|wx.RIGHT|wx.LEFT, 10)
        self.sizer.Add((0, 0), 1)
        self.sizer.Add(self.number, 2,  wx.CENTER|wx.EXPAND|wx.RIGHT|wx.LEFT, 10)
        self.sizer.Add((0, 0), 1)
        self.sizer.Add(self.down_btn, 1, wx.CENTER|wx.DOWN|wx.RIGHT|wx.LEFT, 10)

        self.up_btn.Bind(wx.EVT_LEFT_DOWN, lambda e: self.change_num("up"))
        self.down_btn.Bind(wx.EVT_LEFT_DOWN, lambda e: self.change_num("down"))

        self.SetSizer(self.sizer)
    
        self.Bind(wx.EVT_LEFT_DOWN, self.select)
        self.Bind(wx.EVT_ENTER_WINDOW, lambda e: self.hover("over"))
        self.Bind(wx.EVT_LEAVE_WINDOW, lambda e: self.hover("leave"))
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress) 
        
        self.SetSizer(self.sizer)

    def change_num(self, direction, change=False):
        if not change:
            num_str = self.number.GetLabelText()
            
            num = int(num_str)
            if direction == "up":
                num = (num + 1)%60
            elif direction == "down":
                num = (num - 1)%60
            
            self.number.SetLabel(f"{num:02}")
        else:
            self.children = [item.GetWindow() for item in self.GetContainingSizer().GetChildren() if item.GetWindow()]

            num = None
            for i in self.children:
                if i.is_selected:
                    i.is_selected = False
                    i.SetBackgroundColour(wx.Colour(50, 150, 50))
                    i.Refresh()
                    num = self.children.index(i)
                    break
            
            if num is None:
                return

            if direction == 'left':
                num = (num - 1)%len(self.children)
            elif direction == 'right':
                num = (num + 1)%len(self.children)
            self.children[num].is_selected = True
            self.children[num].SetFocusIgnoringChildren()
            self.children[num].SetBackgroundColour(wx.Colour(80, 80, 80))
            self.children[num].Refresh()

    @property
    def num(self):
        return int(self.number.GetLabelText())
    
    def select(self, e=None):
        self.children = [item.GetWindow() for item in self.GetContainingSizer().GetChildren() if item.GetWindow()]
        
        #clear former selection
        for i in self.children:
            if i.is_selected:
                i.SetBackgroundColour(wx.Colour(50, 150, 50))
                i.is_selected = False
                i.Refresh()

        self.is_selected = True
        self.SetFocusIgnoringChildren()
        self.SetBackgroundColour(wx.Colour(80, 80, 80))
        self.Refresh()
        if e: e.Skip()
    
    def onKeyPress(self, e):
        key = e.GetKeyCode()
        if key == wx.WXK_UP:    self.change_num("up")
        elif key == wx.WXK_DOWN:  self.change_num("down")
        elif key == wx.WXK_LEFT:  self.change_num("left", True)
        elif key == wx.WXK_RIGHT: self.change_num("right", True)
    
    def hover(self, mode):
        if mode == "over" and not self.is_selected:
            self.SetBackgroundColour(wx.Colour(60, 60, 60))
            self.Refresh()
        elif mode == "leave" and not self.is_selected:
            self.SetBackgroundColour(wx.Colour(50, 150, 50))
            self.Refresh()

class TimerSelection(ShapedPanel):
    def __init__(self, parent):
        super().__init__(parent, parent.GetBackgroundColour())

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.options_sizer = wx.BoxSizer()
        self.hr = Options(self)
        self.min = Options(self)
        self.sec = Options(self)
        
        self.options_sizer.Add((0, 0), 1)
        self.options_sizer.Add(self.hr, 1, wx.EXPAND|wx.ALL, 10)
        self.options_sizer.Add(self.min, 1, wx.EXPAND|wx.ALL, 10)
        self.options_sizer.Add(self.sec, 1, wx.EXPAND|wx.ALL, 10)
        self.options_sizer.Add((0, 0), 1)

        self.play_btn = ShapedButton(self, "►")
        self.play_btn.Bind(wx.EVT_LEFT_DOWN, self.start_timer)
        self.sizer.Add((0,0), 1)
        self.sizer.Add(self.options_sizer, 0, wx.EXPAND)
        self.sizer.Add((0, 0), 2)
        self.sizer.Add(self.play_btn, 0, wx.CENTER)
        self.sizer.Add((0,0), 1)

        self.SetSizer(self.sizer)
    
    def start_timer(self, e):
        num = self.hr.num * 3600 + self.min.num * 60 + self.sec.num
        if num > 4:
            self.Parent.timer(num)
        else:
            wx.MessageBox("Timer can not be less than 5 seconds", "Time Setting", style=wx.CENTRE)

class TimerClock(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        def play_f(e):
            self.clock.timer.Start(1000)
            self.pause_btn.Enable()
            self.start_btn.Disable()
        
        def pause_f(e):
            self.clock.timer.Stop()
            self.start_btn.Enable()
            self.pause_btn.Disable()

        def reset(e): 
            self.clock.timer.Stop()
            self.Parent.timerSelection.hr.number.SetLabel("00")
            self.Parent.timerSelection.min.number.SetLabel("00")
            self.Parent.timerSelection.sec.number.SetLabel("00")
            self.clock.set_num(0)
            self.clock.stop_sound()
            self.Parent.reset()

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

        self.clock = RotatePanel(self)

        self.pause_btn = wx.BitmapButton(self, -1, pause, style=wx.BORDER_NONE)
        self.pause_btn.Bind(wx.EVT_BUTTON, pause_f)
        self.pause_btn.SetBackgroundColour(self.clock.GetBackgroundColour())
        self.pause_btn.SetToolTip("Pause")

        self.reset_btn = wx.BitmapButton(self, -1, reset_b, style=wx.BORDER_NONE)
        self.reset_btn.Bind(wx.EVT_BUTTON, reset)
        self.reset_btn.SetBackgroundColour(self.clock.GetBackgroundColour())
        self.reset_btn.SetToolTip("Reset")

        self.start_btn = wx.BitmapButton(self, -1, play, style=wx.BORDER_NONE)
        self.start_btn.Bind(wx.EVT_BUTTON, play_f)
        self.start_btn.SetBackgroundColour(self.clock.GetBackgroundColour())
        self.start_btn.SetToolTip("Play")

        self.start_btn.Disable()
        
        self.btn_sizer = wx.BoxSizer()
        self.btn_sizer.Add((0, 0), 1)
        self.btn_sizer.Add(self.pause_btn, 0)
        self.btn_sizer.Add((0, 0), 1)
        self.btn_sizer.Add(self.reset_btn, 0)
        self.btn_sizer.Add((0, 0), 1)
        self.btn_sizer.Add(self.start_btn, 0)
        self.btn_sizer.Add((0, 0), 1)

        self.sizer.Add(self.clock, 8, wx.CENTER|wx.EXPAND)
        self.sizer.Add(self.btn_sizer, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
    
    def set_num(self, num):
        self.clock.set_num(num)
        self.clock.start("")

class Timer(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetBackgroundColour(parent.GetBackgroundColour())

        self.timerSelection = TimerSelection(self)
        self.timerClock = TimerClock(self)

        self.sizer.Add(self.timerSelection, 1, wx.EXPAND)
        self.sizer.Add(self.timerClock, 1, wx.EXPAND)
        self.timerClock.Hide()

        self.SetSizer(self.sizer)
    
    def timer(self, num):
        self.timerSelection.Hide()
        self.timerClock.Show()
        self.timerClock.set_num(num)
        self.Layout()
    
    def reset(self):
        self.timerClock.Hide()
        self.timerSelection.Show()
