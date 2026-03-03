import wx

class ShapedButton(wx.Button):
    def __init__(self, parent, parent_color, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.text = text

        self.SetBackgroundColour(parent_color)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.paint)

        self.SetMinSize((50, 50))

    def paint(self, e):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)

        gc.SetBrush(wx.Brush(wx.BLUE))
        w, h = self.GetSize()
        gc.DrawEllipse(0, 0, w, h)
        font = wx.Font(17, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        gc.SetFont(font, wx.WHITE) 
        text_width, text_height = gc.GetTextExtent(self.text)
        text_x = (w - text_width) / 2
        text_y = (h - text_height) / 2
        gc.DrawText(self.text, text_x, text_y)

class ShapedLabel(wx.Panel):
    def __init__(self, parent, parent_color, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.SetBackgroundColour(parent_color)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.text = text
        self.Bind(wx.EVT_SIZE, self.Onsize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnPaint(self, e):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        
        w, h = self.GetSize()
        gc.SetBrush(wx.Brush(wx.WHITE)) 
        gc.DrawRoundedRectangle(0, 0, w, h, 30)

        font = wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        gc.SetFont(font, wx.BLACK) 
        text_width, text_height = gc.GetTextExtent(self.text)
        text_x = (w+10 - text_width) / 2
        text_y = (h+10 - text_height) / 2
        gc.DrawText(self.text, text_x, text_y)
    
    def GetLabelText(self):
        return self.text

    def SetLabel(self, word):
        self.text = word
        self.Refresh()
    
    def Onsize(self, e):
        self.Refresh()
        e.Skip()

class ShapedPanel(wx.Panel):
    def __init__(self, parent, color, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.Onsize)
        self.SetBackgroundColour(color)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)

    def OnPaint(self, e):
        pdc = wx.AutoBufferedPaintDC(self)
        pdc.Clear()
        dc = wx.GraphicsContext.Create(pdc)

        w, h = self.GetSize()

        dc.SetBrush(wx.Brush(wx.Colour(50, 150, 50)))
        dc.SetPen(wx.TRANSPARENT_PEN) # Removes the default black border
        dc.DrawEllipse(0, 0, w, h)
    
    def Onsize(self, e):
        self.Refresh()
        e.Skip()
