import wx

from itemdata import *

""" wxStuff

    IDs:
        0xx -> Frame
        1xx -> StaticText
        2xx -> Button
        3xx -> ComboBox
        4xx -> TextCtrl

    __init__(self, parent, id, title, pos, size, style, name)
    
    +--------------> x
    |
    |
    |      P (x,y)
    |
    v
    y
    
    Events:
        EVT_BUTTON
        EVT_TEXT
        EVT_COMBOBOX
    
    Event functions:
        event.GetString() -> name of the event (i.e. name of button, name of option in combobox, text in textctrl)
        event.Id()        -> id of the event
    
"""    

item_1 = "None"
item_2 = "None"
item_3 = "None"
item_4 = "None"
item_5 = "None"

class Prog (wx.Frame):
    def __init__ (self, id, title):
        wx.Frame.__init__(self, None, id, title,
                    size=(800,600),
                    style=wx.DEFAULT_FRAME_STYLE)
        
        panel = wx.Panel (self, -1)
        
        wx.StaticText(panel, -1, "This example uses the wx.ComboBox control.", (10, 10))
        
        button = wx.Button(panel, 210, "Pick Item", (180, 10))
        self.Bind(wx.EVT_BUTTON, self.click, button)
        button.SetSize((120,30))
        
        t1 = wx.TextCtrl(panel, 410, "Test it out and see",
                    (10, 30),(125, -1),
                    #style=wx.TE_READONLY
                    )
        self.Bind(wx.EVT_TEXT, self.text_change, t1)
        
        item_list = get_item_list()
        
        item_combo_box = wx.ComboBox(panel, 310, "None", 
                            (180, 40), (160, -1), 
                            item_list,
                            wx.CB_DROPDOWN
                            #| wx.CB_SORT
                            )

        self.Bind(wx.EVT_COMBOBOX, self.pick_item, item_combo_box)

        
    def click (self, event):
        print "click: %d and item: %s" % (event.Id, chosen_item)
        
        
    def pick_item (self, event):
        global chosen_item
        chosen_item = event.GetString()
        print "Item chosen: %s" % (event.GetString())

        
    def text_change (self, event):
        print "Text: %s" % (event.GetString)
        
        
app = wx.App(0)
frame = Prog(010, "Hi")

frame.Show()

app.MainLoop()
