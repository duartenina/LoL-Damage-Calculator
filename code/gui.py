import wx

from code.champ import *
from code.graph import *
from code.item  import *
from code.extra import *

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

items = ['None','None','None','None','None']


class Prog (wx.Frame):
    def __init__ (self, id, title):
        wx.Frame.__init__(self, None, id, title,
                    size=(800,600),
                    style=wx.DEFAULT_FRAME_STYLE)
        
        panel = wx.Panel (self, -1)
        
        wx.StaticText(panel, -1, "This example uses the wx.ComboBox control.", (10, 10))
        
        button = wx.Button(panel, 210, "Pick Item",
                        (280, 10), (150,40))
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        t1 = wx.TextCtrl(panel, 410, "Test it out and see",
                    (10, 40),(125, -1),
                    #style=wx.TE_READONLY
                    )
        self.Bind(wx.EVT_TEXT, self.text_change, t1)
        
        item_list = get_item_list()
        
        cb_item_1 = wx.ComboBox(panel, 311, "None", 
                            (280,40), (160, -1), 
                            item_list,
                            wx.CB_DROPDOWN
                            #| wx.CB_SORT
                            )
        self.Bind(wx.EVT_COMBOBOX, self.pick_item, cb_item_1)
        
        cb_item_2 = wx.ComboBox(panel, 312, "None", 
                            (280,70), (160, -1), 
                            item_list,
                            wx.CB_DROPDOWN
                            #| wx.CB_SORT
                            )
        self.Bind(wx.EVT_COMBOBOX, self.pick_item, cb_item_2)
        
        cb_item_3 = wx.ComboBox(panel, 313, "None", 
                            (280,100), (160, -1), 
                            item_list,
                            wx.CB_DROPDOWN
                            #| wx.CB_SORT
                            )
        self.Bind(wx.EVT_COMBOBOX, self.pick_item, cb_item_3)
        
        cb_item_4 = wx.ComboBox(panel, 314, "None", 
                            (280,130), (160, -1), 
                            item_list,
                            wx.CB_DROPDOWN
                            #| wx.CB_SORT
                            )
        self.Bind(wx.EVT_COMBOBOX, self.pick_item, cb_item_4)
        
        cb_item_5 = wx.ComboBox(panel, 315, "None", 
                            (280,160), (160, -1), 
                            item_list,
                            wx.CB_DROPDOWN
                            #| wx.CB_SORT
                            )
        self.Bind(wx.EVT_COMBOBOX, self.pick_item, cb_item_5)
        
        wx.StaticText(panel, 120, "Build:", (10, 10))
        
        self.tc_items = wx.TextCtrl(panel, 420, "Build: ",
                    (280, 190),(160, 90),
                    style=wx.TE_MULTILINE|wx.TE_READONLY
                    )

        #self.panel = panel
        
        
    def click (self, event):
        print "Build: %s" % (get_build())
        self.build_change (event)
        
    def pick_item (self, event):
        global item
        
        item_name = event.GetString()
        event_id  = event.GetId() - 310
        
        items[event_id-1] = item_name
        print "Item chosen: %s, ID: %d" % (item_name, event_id)
        self.build_change (event)

        
    def text_change (self, event):
        print "Text: %s" % (event.GetString())
        
    def build_change (self, event):
        self.tc_items.SetValue("Build: %s" % (get_build()))
        
        
def get_build ():
    build = ""
    for item in items:
        if (item != "None"): build += item + " "
    
    return build
        
        
app = wx.App(0)
frame = Prog(010, "Hi")

frame.Show()

app.MainLoop()
