
import wx
from .custom import ToggleSlider, ShapedButton, ShapedLabel
from wx.lib.scrolledpanel import ScrolledPanel
from datetime import datetime as dt
import pygame
import os

class AlarmOption(wx.Panel):
    def __init__(self, parent, time, freq):
        super().__init__(parent, style=wx.BORDER_THEME)
        self.SetBackgroundColour(wx.Colour(220, 200, 250))
        self.SetMinSize((300, 70))

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        font = wx.Font(15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial")
        font2 = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_NORMAL, False, "Consolas")

        time = wx.StaticText(self, -1, time)
        time.SetFont(font)
        freq = wx.StaticText(self, -1, freq)
        freq.SetFont(font2)
        self.toggle = ToggleSlider(self, wx.Colour(220, 200, 250))

        self.time_toggle = wx.BoxSizer()
        self.time_toggle.Add(time, 1, wx.ALL, 10)
        self.time_toggle.Add((0, 0), 1)
        self.time_toggle.Add(self.toggle, 0, wx.ALL, 10)

        self.sizer.Add(self.time_toggle, 1, wx.EXPAND)
        self.sizer.Add(freq, 1, wx.EXPAND|wx.LEFT, 10)

        self.SetSizer(self.sizer)

class Options(wx.Panel):
    def __init__(self, parent, color, time, text="00", *args, **kwargs):
        super().__init__(parent, style=wx.WANTS_CHARS, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.SetBackgroundColour(color)
        self.is_selected = False
        self.time = time

        self.up_btn = ShapedButton(self, "˄")
        self.number = ShapedLabel(self, color, text, 20)
        self.down_btn = ShapedButton(self, "˅")

        self.sizer.Add(self.up_btn, 1, wx.CENTER|wx.ALL, 10)
        self.sizer.Add((0, 0), 1)
        self.sizer.Add(self.number, 2,  wx.CENTER|wx.EXPAND|wx.ALL, 10)
        self.sizer.Add((0, 0), 1)
        self.sizer.Add(self.down_btn, 1, wx.CENTER|wx.ALL, 10)

        self.up_btn.Bind(wx.EVT_LEFT_DOWN, lambda e: self.change_num("up"))
        self.down_btn.Bind(wx.EVT_LEFT_DOWN, lambda e: self.change_num("down"))

        self.Bind(wx.EVT_LEFT_DOWN, self.select)
        self.Bind(wx.EVT_ENTER_WINDOW, lambda e: self.hover("over"))
        self.Bind(wx.EVT_LEAVE_WINDOW, lambda e: self.hover("leave"))
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyPress)

        self.SetSizer(self.sizer)
    
    @property
    def num(self):
        return self.number.GetLabelText()
    
    def change_num(self, direction, change=False):
        if not change:
            num_str = self.number.GetLabelText()
            
            # Handle AM/PM
            if not num_str.isdigit() and not change:
                self.number.SetLabel("PM" if num_str == "AM" else "AM")
                return

            num = int(num_str)
            if direction == "up":
                if self.time == 'hr':
                    num = 1 if num >= 12 else num + 1
                elif self.time == 'min':
                    num = 0 if num >= 59 else num + 1
            elif direction == "down":
                if self.time == 'hr':
                    num = 12 if num <= 1 else num - 1
                elif self.time == 'min':
                    num = 59 if num <= 0 else num - 1
            
            self.number.SetLabel(f"{num:02}")
        else:
            self.children = [item.GetWindow() for item in self.GetContainingSizer().GetChildren() if item.GetWindow()]

            num = None
            for i in self.children:
                if i.is_selected:
                    i.is_selected = False
                    i.SetBackgroundColour(self.Parent.GetBackgroundColour())
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
        return self.number.GetLabelText()
    
    def select(self, e=None):
        self.children = [item.GetWindow() for item in self.GetContainingSizer().GetChildren() if item.GetWindow()]
        
        #clear former selection
        for i in self.children:
            if i.is_selected:
                i.SetBackgroundColour(self.Parent.GetBackgroundColour())
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
        pass
        if mode == "over" and not self.is_selected:
            self.SetBackgroundColour(wx.Colour(60, 60, 60))
            self.Refresh()
        elif mode == "leave" and not self.is_selected:
            self.SetBackgroundColour(self.Parent.GetBackgroundColour())
            self.Refresh()

class AddDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, size=parent.GetSize())
        self.CentreOnParent()
        
        color = "#1A1818"
        self.SetBackgroundColour(color)
        self.freq_day = set()

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.options_sizer = wx.BoxSizer()
        self.hr = Options(self, color, "hr")
        self.min = Options(self, color, "min")
        self.mer = Options(self, color, "", "AM")

        self.options_sizer.Add((0,0), 1)        
        self.options_sizer.Add(self.hr, 5, wx.EXPAND|wx.LEFT|wx.UP|wx.BOTTOM, 5)
        self.options_sizer.Add((0,0), 1)
        self.options_sizer.Add(self.min, 5, wx.EXPAND|wx.LEFT|wx.UP|wx.BOTTOM, 5)
        self.options_sizer.Add((0,0), 1)
        self.options_sizer.Add(self.mer, 5, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.UP|wx.BOTTOM, 5)
        self.options_sizer.Add((0,0), 1)

        self.freq = wx.BoxSizer()
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, 
                           wx.FONTWEIGHT_BOLD, faceName="Arial")
        self.normal = {1:'Sun', 2:'Mon', 3:'Tue', 4:'Wed', 5:'Thu', 6:'Fri', 7:'Sat'}
        for i in self.normal.values():
            text = wx.StaticText(self, -1, i, style=wx.BORDER_THEME|wx.TE_CENTER)
            text.SetForegroundColour(wx.WHITE)
            text.Bind(wx.EVT_LEFT_UP, self.Select)
            text.SetFont(font)
            self.freq.Add(text, 1, wx.ALL, 5)

        self.ringtone = wx.BoxSizer()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        sound_path = os.path.join(BASE_DIR, "sound", "alarm.mp3")
        self.file_path = wx.TextCtrl(self, -1, sound_path)
        font2 = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_LIGHT, 0, "Consolas")
        self.file_path.SetFont(font2)
        browse = wx.Button(self, -1, "Browse")
        browse.SetFont(font2)
        browse.Bind(wx.EVT_BUTTON, self.Browse)
        self.ringtone.Add(self.file_path, 4, wx.RIGHT, 5)
        self.ringtone.Add(browse, 1)

        self.name_sizer = wx.BoxSizer()
        self.label = wx.StaticText(self, -1, "Label: ", style=wx.TE_CENTER)
        self.label.SetFont(font2)
        self.label.SetForegroundColour(wx.WHITE)
        self.name = wx.TextCtrl(self, -1)
        self.name.SetFont(font2)
        self.name_sizer.Add(self.label, 1)
        self.name_sizer.Add(self.name, 3)
        
        self.enter = ShapedButton(self, "Enter")
        self.enter.Bind(wx.EVT_BUTTON, self.submit)
        self.enter.SetMinSize((100, 50))

        self.sizer.Add(self.options_sizer, 6, wx.EXPAND|wx.UP|wx.DOWN, 20)
        self.sizer.Add(self.freq, 0, wx.LEFT|wx.RIGHT|wx.DOWN|wx.EXPAND, 10)
        self.sizer.Add(self.ringtone, 0, wx.LEFT|wx.RIGHT|wx.DOWN|wx.EXPAND, 10)
        self.sizer.Add(self.name_sizer, 0, wx.LEFT|wx.RIGHT|wx.DOWN|wx.EXPAND, 10)
        self.sizer.Add(self.enter, 0, wx.CENTER|wx.DOWN, 10)

        self.SetSizer(self.sizer)
    
    def Select(self, e):
        # Get the widget directly from the event
        clicked_widget = e.GetEventObject()
        
        # Store the day
        self.freq_day.add(clicked_widget.GetLabel())
        
        # Update the UI
        clicked_widget.SetBackgroundColour(wx.GREEN)
        clicked_widget.Refresh() # Ensure the color update draws immediately
    
    def Browse(self, e):
        with wx.FileDialog(self, "Open sound file", wildcard="Music Files |*.mp3;*.wav",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  
            
            self.file_path.SetValue(fileDialog.GetPath())
    
    def submit(self, e=None):
        self.data = {
            'music': self.file_path.GetValue(),
            'time': f"{self.hr.num}:{self.min.num} {self.mer.num}",
            'freq': self.arrange(self.freq_day),
            'name': self.name.GetValue(),
        }
        if self.IsModal():
            self.EndModal(wx.ID_OK)
    
    def OnClose(self, e):
        self.EndModal(wx.ID_CANCEL)
        
    def arrange(self, given):
        # function to arrange the frequency in correct wk day order
        new = []
        for i in given:
            for j, k in self.normal.items():
                if k == i:
                    new.append(j)
        return [self.normal[i] for i in sorted(new)]


class Alarm(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetDoubleBuffered(True)

        self.time_list = []

        self.scroll_area = ScrolledPanel(self)
        self.scroll_sizer = wx.BoxSizer(wx.VERTICAL)

        self.scroll_area.SetSizer(self.scroll_sizer)
        self.scroll_area.SetupScrolling()

        self.add_btn = ShapedButton(self, "+")
        self.add_btn.SetSize((40, 40))
        self.add_btn.Bind(wx.EVT_BUTTON, self.add)
        
        self.timer = wx.Timer()
        self.timer.Bind(wx.EVT_TIMER, self.OnTimer)
        self.timer.Start(1000)

        self.Bind(wx.EVT_SIZE, self.OnSizer)
        self.scroll_area.Bind(wx.EVT_SCROLLWIN, self.OnScrollUpdate)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sound_path = os.path.join(BASE_DIR,"sound", "alarm.mp3")
        
        if self.okFile(sound_path):
            self.sound = pygame.mixer.Sound(sound_path)
        self.alarm_played = False

        self.Centre()

    def OnScrollUpdate(self, e):
        self.add_btn.Refresh(eraseBackground=False)
        e.Skip()

    def OnTimer(self, e):
        now = dt.now().strftime("%I:%M %p")
        day = dt.now().strftime("%a")

        for i in self.time_list:
            if i[2] == "Once":
                if i[0] == now and i[1].toggle.selected and not pygame.mixer.get_busy() and not self.alarm_played:
                    if hasattr(self, "sound"):
                        self.sound.play()
                    self.alarm_played = True
                elif not i[1].toggle.selected:
                    if hasattr(self, "sound"):
                        self.sound.stop()
            else:
                for k in i[2]:
                    if i[0] == now and i[1].toggle.selected and k == day and not pygame.mixer.get_busy():
                        if hasattr(self, "sound"):
                            self.sound.play()
                        self.alarm_played = True
                    elif not i[1].toggle.selected:
                        if hasattr(self, "sound"):
                            self.sound.stop()

    def OnSizer(self, e):
        self.Layout()

        w, h = self.GetClientSize()
        bw, bh = self.add_btn.GetSize()

        self.scroll_area.SetSize(0, 0, w, h)

        self.add_btn.SetPosition((w//2-bw//2, h-bh-50))
        self.add_btn.Raise()

        e.Skip()

    def okFile(self, file):
        try:
            self.sound = pygame.mixer.Sound(file)
        except Exception:
            return False
        else: 
            return True
    
    def add(self, e):
        dlg = AddDialog(self)
        res = dlg.ShowModal()

        if res == wx.ID_OK:
            freq = ",".join(dlg.data['freq']) if dlg.data['freq'] else "Once"
            time_str = dlg.data['time']
            if self.okFile(dlg.data['music']):
                self.sound = pygame.mixer.Sound(dlg.data['music'])

            # Create the UI element for the alarm
            new_alarm = AlarmOption(self.scroll_area, time_str, freq)
            self.time_list.append([time_str, new_alarm, freq.split(',') if freq != "Once" else freq])
            self.scroll_sizer.Add(new_alarm, 0, wx.EXPAND | wx.ALL, 5)
            
            self.scroll_area.Layout()
            self.scroll_area.SetupScrolling()
