import wx
from display_panel.clock import DigitalClockPanel, AnalogClockPanel
from display_panel.timer import Timer
from display_panel.alarm import Alarm
from display_panel.stop import StopWatch
import pygame

pygame.mixer.init()

class ClockApp(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Create the main sizer
        self.m_sizer =  wx.BoxSizer()
        
        # create the two main panels(nav and display)
        self.nav_panel = wx.Panel(self, id=-1)
        self.display_panel = wx.Panel(self, id=-1)

        # create nav panel sizer and add nav panel options
        self.nav_panel_sizer = wx.BoxSizer(wx.VERTICAL)     
        
        self.c_btn = wx.StaticText(self.nav_panel, id=-1, label="Clock", style=wx.TE_CENTER)
        self.t_btn = wx.StaticText(self.nav_panel, id=-1, label="Timer", style=wx.TE_CENTER)
        self.a_btn = wx.StaticText(self.nav_panel, id=-1, label="Alarm Clock", style=wx.TE_CENTER)
        self.s_btn = wx.StaticText(self.nav_panel, id=-1, label="Stop Watch", style=wx.TE_CENTER)

        # list of options
        self.btn_list = [self.c_btn, self.t_btn, self.a_btn, self.s_btn]

        # create display panel sizer and add display panel options
        self.display_panel_sizer = wx.BoxSizer(wx.VERTICAL) 
        
        # create clock panel and its options
        self.clock = wx.Panel(self.display_panel)
        self.clock.SetName("clock")
        self.clock_sizer = wx.BoxSizer(wx.VERTICAL)

        self.digital_clock = DigitalClockPanel(self.clock)
        self.analog_clock = AnalogClockPanel(self.clock)

        self.clock_sizer.Add(self.digital_clock, 1, wx.EXPAND | wx.DOWN, 5)
        self.clock_sizer.Add(self.analog_clock, 1, wx.EXPAND | wx.UP, 5)

        self.clock.SetSizer(self.clock_sizer)

        # create timer panel and its options
        self.timer = wx.Panel(self.display_panel)
        self.timer.SetName("timer")

        self.timer_sizer = wx.BoxSizer(wx.VERTICAL)
        self.timer.SetBackgroundColour("#363232")
        self.timer_clock = Timer(self.timer)
        
        self.timer_sizer.Add(self.timer_clock, 1, wx.EXPAND | wx.CENTER)
        self.timer.SetSizer(self.timer_sizer)

        # create alarm panel and its options
        self.alarm = wx.Panel(self.display_panel)
        self.alarm.SetName("alarm clock")

        self.alarm_sizer = wx.BoxSizer(wx.VERTICAL)
        self.alarm.SetBackgroundColour("#363232")
        self.alarm_clock = Alarm(self.alarm)
        
        self.alarm_sizer.Add(self.alarm_clock, 1, wx.EXPAND | wx.CENTER)
        self.alarm.SetSizer(self.alarm_sizer)
        
        # create stop watch panel and its options
        self.stopwatch = wx.Panel(self.display_panel)
        self.stopwatch.SetName("stop watch")

        self.stopwatch_sizer = wx.BoxSizer(wx.VERTICAL)
        self.stopwatch.SetBackgroundColour("#363232")
        self.stopwatch_clock = StopWatch(self.stopwatch)
        
        self.stopwatch_sizer.Add(self.stopwatch_clock, 1, wx.EXPAND | wx.CENTER)
        self.stopwatch.SetSizer(self.stopwatch_sizer)

        # Add all panels to list for easy sorting
        self.windows = [self.clock, self.timer, self.alarm, self.stopwatch]

        # check rezizing windows
        self.Bind(wx.EVT_SIZE, self.resize)

        # set UI
        self.initUI()

    def initUI(self):
        # add title and size
        self.SetTitle("Clock")
        self.SetMinSize((800, 600))
        self.SetSize(900, 700)

        # style nav panel options and add thier functions
        for i in self.btn_list:
            i.SetBackgroundColour("black")
            i.SetForegroundColour("white")
            i.SetFont(wx.Font(15, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_MAX,
                             wx.FONTWEIGHT_EXTRAHEAVY, faceName="Consolas"))
            name = i.GetLabelText().lower()
            i.Bind(wx.EVT_LEFT_DOWN, lambda e: self.switch(e, name))

        # nav layout set
        self.nav_panel_sizer.Add(self.c_btn, 0, wx.EXPAND | wx.ALL, 5)
        self.nav_panel_sizer.Add(self.t_btn, 0, wx.EXPAND | wx.ALL, 5)
        self.nav_panel_sizer.Add(self.a_btn, 0, wx.EXPAND | wx.ALL, 5)
        self.nav_panel_sizer.Add(self.s_btn, 0, wx.EXPAND | wx.ALL, 5)
        self.nav_panel.SetSizer(self.nav_panel_sizer)

        #display layout set
        self.display_panel_sizer.Add(self.clock, 1, wx.EXPAND | wx.ALL, 5)
        self.display_panel_sizer.Add(self.timer, 1, wx.EXPAND | wx.ALL, 5)
        self.display_panel_sizer.Add(self.alarm, 1, wx.EXPAND | wx.ALL, 5)
        self.display_panel_sizer.Add(self.stopwatch, 1, wx.EXPAND | wx.ALL, 5)
        self.display_panel.SetSizer(self.display_panel_sizer)

        # add panel to main sizer
        self.m_sizer.Add(self.nav_panel, 2, wx.EXPAND | wx.ALL, border=5)
        self.m_sizer.Add(self.display_panel, 5, wx.EXPAND | wx.ALL, border=5)
        
        # set the sizer
        self.SetSizer(self.m_sizer)

        # hide the other sizers except clock
        self.switch()

        #center the window
        self.Centre()
    
    def resize(self, e):
        e.Skip()
    
    def switch(self, e=None, name="clock"):
        """To switch between tabs"""
        if e:
            name = e.GetEventObject().GetLabel().lower()
        
        for i in self.windows:
            if i.GetName() == name:
                i.Show()
            else:
                i.Hide()
        
        self.Layout()

if __name__ == "__main__":
    app = wx.App(False)
    window = ClockApp(None)
    window.Show()
    app.MainLoop()
