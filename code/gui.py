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
        5xx -> ListBox

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
button_size = (80,20)


class Prog (wx.Frame):
    def __init__ (self):
        #************************* Basic Stuff (IDs x1x) *************************#
        wx.Frame.__init__(self, None, 010, "LoL Damage Calculator",
                    size = (800,600),
                    style = wx.DEFAULT_FRAME_STYLE)
                    
        self.CenterOnScreen()
        
        panel = wx.Panel (self, 011)
        
        #************************* Champion (IDs x2x) *************************#
        
        self.tc_items = wx.TextCtrl(panel, 421, "Build: ", (280, 190), (160, 90), style = wx.TE_READONLY)
        wx.StaticText(panel, 111, "This example uses the wx.ComboBox control.", (10, 10))
        
        t1 = wx.TextCtrl(panel, 410, "Test it out and see", (10, 40), (125, -1))
        self.Bind(wx.EVT_TEXT, self.text_change, t1)
        
        #************************* Items (IDs x3x) *************************#
        
        wx.StaticText(panel, 131, "Items:", (10, 450))
        
        cb_item = []
        for i in xrange(5):
            cb_item.append(self.create_cb_item(panel, i+1))
            self.Bind(wx.EVT_COMBOBOX, self.pick_item, cb_item[i])
       
        #************************* Builds (IDs x4x) *************************#
        
        wx.StaticText(panel, 141, "Builds:", (330, 450))
        self.lb_builds = wx.ListBox(panel, 541, (330, 470), (350, 80), [], wx.LB_SINGLE)
        
        button = wx.Button(panel, 241, "Add",    (690, 470), button_size)
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(panel, 242, "Remove", (690, 500), button_size)
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(panel, 243, "Clear",  (690, 530), button_size)
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
    def create_cb_item (self, panel, id):
        item_list = get_item_list()
        pos = {1: (150, 450), 2: (10, 490), 3: (150, 490), 4: (10, 530), 5: (150, 530)}
        
        cb_item = wx.ComboBox(panel, 310 + id, "None", pos[id], (120, 25), item_list, wx.CB_DROPDOWN)       
        
    def click (self, event):
        if   (event.GetId() == 241):
            self.build_add (event)
        elif (event.GetId() == 242):
            self.build_remove (event)
        elif (event.GetId() == 243):
            self.build_clear (event)
        
    def pick_item (self, event):
        global item
        
        item_name = event.GetString()
        event_id  = event.GetId() - 310
        
        items[event_id-1] = item_name
        print "Item chosen: %s, ID: %d" % (item_name, event_id)
        self.build_change (event)

        
    def text_change (self, event):
        print "Text: %s" % (event.GetString())
        
    def build_add (self, event):
        if (self.lb_builds.GetCount() < 5):
            self.lb_builds.Insert(get_build(), self.lb_builds.GetCount(), get_build())
            print "Build added: %s" % (get_build())
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
        
    def build_remove (self, event):
        if (self.lb_builds.GetCount() > 0):
            print "Build removed"   
            self.lb_builds.Delete(self.lb_builds.GetSelection())
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
        
    def build_clear (self, event):
        print "All builds removed"
        self.lb_builds.Clear()
        
    def build_change (self, event):
        self.tc_items.SetValue("Build: %s" % (get_build()))

      
def get_build ():
    build = ""
    for item in items:
        if (item != "None"):
            build += item + " "
            
    if (build == ""):
        build = "Empty"
    
    return build
        

def run():
    
    app = wx.App(0)
    frame = Prog()

    frame.Show()

    app.MainLoop()


    
run()