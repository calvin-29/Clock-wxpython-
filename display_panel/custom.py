import wx

class ShapedButton(wx.Button):
    def __init__(self, parent, text, *args, **kwargs):
        super().__init__(parent, *args, **kwargs, style=wx.NO_BORDER|wx.TRANSPARENT_WINDOW)
        self.text = text

        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.paint)

        self.SetMinSize((50, 50))

    def paint(self, e):
        dc = wx.PaintDC(self)
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
    def __init__(self, parent, parent_color, text, fontsize=50, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.SetBackgroundColour(parent_color)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.text = text
        self.fontsize = fontsize
        self.Bind(wx.EVT_SIZE, self.Onsize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
    
    def OnPaint(self, e):
        dc = wx.AutoBufferedPaintDC(self)
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        
        w, h = self.GetSize()
        gc.SetBrush(wx.Brush(wx.WHITE)) 
        gc.DrawRoundedRectangle(0, 0, w, h, 30)

        font = wx.Font(self.fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        gc.SetFont(font, wx.BLACK) 
        text_width, text_height = gc.GetTextExtent(self.text)
        text_x = (w - text_width) / 2
        text_y = (h - text_height) / 2
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

class ToggleSlider(wx.Button):
    def __init__(self, parent, color):
        super().__init__(parent)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.SetBackgroundColour(color)
        self.SetMinSize((35, 20))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_BUTTON, self.OnClick)

        self.selected = True
    
    def OnPaint(self, e):
        pc = wx.AutoBufferedPaintDC(self)
        pc.Clear()
        gdc = wx.GraphicsContext.Create(pc)

        w, h = self.GetSize()
        x = 0
        color = ""
        
        if self.selected:
            x = w-(h-3)
            color = wx.BLUE
        else:
            x = 2
            color = wx.LIGHT_GREY

        gdc.SetBrush(wx.Brush(color))
        gdc.SetPen(wx.TRANSPARENT_PEN)
        gdc.DrawRoundedRectangle(0, 0, w, h, 10)

        # the roller
        gdc.SetBrush(wx.Brush(wx.WHITE))
        gdc.SetPen(wx.TRANSPARENT_PEN)
        gdc.DrawEllipse(x, 2, h-4, h-4)

    def OnClick(self, e):
        if self.selected:
            self.selected = False
        else:
            self.selected = True
        self.Refresh()

    def OnSize(self, e):
        self.Refresh()
        e.Skip()
    
    def GetState(self, e):
        return self.selected
