import wx
from datetime import datetime
import math
import pygame

pygame.mixer.init()

class AnalogClockPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SUNKEN_BORDER)
        self.SetBackgroundColour("#1A1818")
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        # 1. Start a Timer that triggers every 1000ms (1 second)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(1000)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnTimer(self, event):
        self.Refresh() # This forces OnPaint to run again

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        now = datetime.now()

        # Move to center
        w, h = self.GetSize()
        center_x, center_y = w/2, h/2
        radius = min(w, h) / 2 - 10 

        gc.Translate(center_x, center_y)
        gc.SetBrush(wx.Brush(wx.BLACK))
        gc.DrawEllipse(-radius, -radius, radius*2, radius*2)

        # --- HOUR MARKS (The 12 Ticks) ---
        for i in range(60):
            is_hour = (i % 5 == 0)
            gc.SetPen(wx.Pen(wx.WHITE, 3 if is_hour else 2))
            
            gc.PushState()
            gc.Rotate(math.radians(i * 6))
            
            # Ticks start at the edge and go inward
            tick_start = -radius
            tick_length = 10 if is_hour else 7
            gc.StrokeLine(0, tick_start, 0, tick_start + tick_length)
            gc.PopState()

        # --- HOUR HAND ---
        gc.PushState() # SAVE: Paper is straight
        # 360 degrees / 12 hours = 30 degrees per hour
        hour_angle = now.hour * 30 
        gc.Rotate(math.radians(hour_angle))
        
        gc.SetPen(wx.Pen(wx.YELLOW, 6)) # Thick hand
        gc.StrokeLine(0, 0, 0, -(radius*0.5))    # Short hand
        gc.PopState()  # LOAD: Paper snaps back to straight!

        # --- MINUTE HAND ---
        gc.PushState() # SAVE again
        # 360 degrees / 60 minutes = 6 degrees per minute
        min_angle = now.minute * 6
        gc.Rotate(math.radians(min_angle))
        
        gc.SetPen(wx.Pen(wx.BLUE, 4))  # Medium hand
        gc.StrokeLine(0, 0, 0, -(radius*0.7))    # Long hand
        gc.PopState()  # LOAD again

        # --- SECOND HAND ---
        gc.PushState() # SAVE again
        # 360 degrees / 60 minutes = 6 degrees per minute
        min_angle = now.second * 6
        gc.Rotate(math.radians(min_angle))
        
        gc.SetPen(wx.Pen(wx.GREEN, 2))  # Medium hand
        gc.StrokeLine(0, 0, 0, -(radius*0.9))    # Long hand
        gc.PopState()  # LOAD again

        # screw to hold hands together to make it look better
        gc.SetBrush(wx.Brush(wx.BLACK))
        gc.SetPen(wx.Pen(wx.WHITE, 3))
        gc.DrawEllipse(-10, -10, 20, 20)

class DigitalClockPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetBackgroundColour("#1A1818")

        #create sizer and label and style it
        self.sizer = wx.BoxSizer()
        self.digital_display = wx.StaticText(self, -1, "", style=wx.TE_CENTER)

        self.font = wx.Font(25, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_MAX,
                             wx.FONTWEIGHT_EXTRAHEAVY, faceName="Consolas")
        self.digital_display.SetFont(self.font)
        self.digital_display.SetForegroundColour("white")

        # set digital clock panel layout
        self.sizer.Add(self.digital_display, 1, wx.ALL | wx.CENTER, 5)
        self.SetSizer(self.sizer)

        # create timer to change the label text, bind it and start it
        self.timer = wx.Timer(self, id=-1)
        self.Bind(wx.EVT_TIMER, self.start, self.timer)
        self.timer.Start(1000)
    
    def start(self, e):
        now = datetime.now()
        formatted_time = now.strftime("%H : %M : %S")
        self.digital_display.SetLabel(formatted_time)
        self.Layout()

class RotatePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.total = 0
        self.number = 0
        self.alarm_played = False

        # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        # sound_path = os.path.join(BASE_DIR, "alarm.mp3")
        self.sound = pygame.mixer.Sound(r"C:\Users\CalvinCU\Music\MONTAGEM TORMENTA (Slowed) [KTxxJEB4f0Y].mp3")

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetBackgroundColour(wx.Colour(50, 50, 50))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, lambda e: self.Refresh())

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    def OnTimer(self, e):
        if self.number > 0:
            self.number -= 1
        elif self.number == 0 and not self.alarm_played:
            self.sound.play()
            self.alarm_played = True

        self.Refresh()

    def OnPaint(self, e):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)

        w, h = self.GetSize()
        radius = min(w, h) / 2 - 20

        gc.Translate(w/2, h/2)

        gc.SetPen(wx.Pen(wx.Colour(70,70,70), 12))
        gc.DrawEllipse(-radius, -radius, radius*2, radius*2)

        if not self.total:
            return
        
        progress = (self.total - self.number) / self.total
        angle_deg = progress * 360

        start_rad = math.radians(-90)
        end_rad = math.radians(-90+angle_deg)

        gc.SetPen(wx.Pen(wx.Colour(90,200,70), 12))
        if angle_deg != 360:
            path = gc.CreatePath()
            path.AddArc(0, 0, radius, start_rad, end_rad, False)
            gc.StrokePath(path)

        gc.PushState()
        gc.SetBrush(wx.Brush(wx.Colour(90,200,70)))
        gc.Rotate(-(math.radians(self.number*(360/self.total))))
        gc.DrawEllipse(0, -(radius)-10, 20, 20)
        gc.PopState()

        gc.SetFont(
            wx.Font(16, wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD),
            wx.Colour(150, 150, 150)
        )

        hr, minu = divmod(self.number, 3600)
        minu, sec = divmod(minu, 60)
        text = f"{hr:02} : {minu:02} : {sec:02}"
        tw, th = gc.GetTextExtent(text)
        gc.DrawText(text, -tw/2, -th/2)
    
    def start(self, e):
        self.timer.Start(1000)
    
    def set_num(self, seconds):
        self.total = seconds
        self.number = seconds
    
    def stop_sound(self):
        self.sound.stop()
        self.alarm_played = False
