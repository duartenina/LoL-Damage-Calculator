import wx

from code.champ import *
from code.graph import *
from code.item  import *
from code.extra import *


""" wxStuff

    IDs:
        0xxx -> Frame
        1xxx -> StaticText
        2xxx -> Button
        3xxx -> Choice
        4xxx -> TextCtrl
        5xxx -> ListBox

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

# default button size
button_size = {'normal':(80,20), 'big':(160, 40)}


class Prog (wx.Frame):
    def __init__ (self):
        #************************* Basic Stuff (IDs x1xx) *************************#
        wx.Frame.__init__(self, None, 0100, "LoL Damage Calculator", size = (800,600), style = wx.CAPTION | wx.CLOSE_BOX)

        self.CenterOnScreen()
        
        self.panel = wx.Panel (self, 0101)
        
        #************************* Champion (IDs x2xx) *************************#
        
        self.choice_champ = wx.Choice(self.panel, 3200, (10,10), (120, 25), get_champion_list())
        self.Bind(wx.EVT_CHOICE, self.pick_champ, self.choice_champ)
        
        self.champ_objects = []
        
        for i in xrange(10):
            self.champ_objects.append(self.create_champ_objects(i))
            if (i != 9):
                self.champ_objects[i]['custom'].Bind(wx.EVT_CHAR, self.text_change)
            
        wx.StaticText(self.panel, 1220, "Level:",           (150,15))
        self.tc_champ_level = wx.TextCtrl(self.panel, 4220, "0", (190,14), (40, 20))
        self.tc_champ_level.Bind(wx.EVT_CHAR, self.text_change)
        
        wx.StaticText(self.panel, 1221, "Time (1s to 60s):",     (250,15))
        self.tc_time = wx.TextCtrl(self.panel, 4221, "5", (340,14), (40, 20))
        self.tc_time.Bind(wx.EVT_CHAR, self.text_change)
        
        self.choice_champ.SetSelection(0)
        self.pick_champ(None)
        
        #************************* Items (IDs x3xx) *************************#
        
        wx.StaticText(self.panel, 1301, "Items:", (10, 450))
        
        self.choice_item = []
        for i in xrange(5):
            self.choice_item.append(self.create_choice_item(i+1))
            self.Bind(wx.EVT_CHOICE, self.pick_item, self.choice_item[i])
       
        #************************* Builds (IDs x4xx) *************************#
        
        wx.StaticText(self.panel, 1401, "Builds:", (330, 450))
        self.lb_builds = wx.ListBox(self.panel, 541, (330, 470), (350, 80), [], wx.LB_SINGLE)
        
        button = wx.Button(self.panel, 2401, "Add",    (690, 470), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, 2402, "Remove", (690, 500), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, 2403, "Clear",  (690, 530), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        #************************* Graphs (IDs x5xx) *************************#
        
        wx.StaticText(self.panel, 1501, "Graph until x Armor (min: 50, max: 500):", (400,15))
        self.tc_armor = wx.TextCtrl(self.panel, 4501, "300",                        (615,14), (40, 20))
        self.tc_armor.Bind(wx.EVT_CHAR, self.text_change)
        
        button = wx.Button(self.panel, 2501, "DPS",      (600, 130), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, 2502, "DPS/gold", (600, 180), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
    def create_champ_objects (self, id):
        name = {0: 'Attack Damage', 1: 'Attack Scaling', 2: 'Attack Speed', 3: 'Speed Scaling', 4: 'Multiplier',
                5: 'Flat Penetration', 6: 'Percent Penetration', 7: 'Critical Chance', 8: 'Critical Damage', 9: 'Type'}
        
        y_base   = 140
        y_per_id = 40
        
        if (id < 5):
            txt_pos   = (010, y_base + id*y_per_id)
            tc_ro_pos = (100, y_base + id*y_per_id)
            tc_pos    = (160, y_base + id*y_per_id)
        else:
            txt_pos   = (220, y_base + (id-5)*y_per_id)
            tc_ro_pos = (330, y_base + (id-5)*y_per_id)
            tc_pos    = (390, y_base + (id-5)*y_per_id)

    
        wx.StaticText(self.panel, 1200 + id, name[id] + ':', txt_pos)
        if (id != 9):
            tc_base = wx.TextCtrl(self.panel, 4200 + id, "0", tc_ro_pos, (50, 20), style = wx.TE_READONLY)
            tc_custom = wx.TextCtrl(self.panel, 4210 + id, "0", tc_pos, (50, 20))
        else: 
            tc_base = wx.TextCtrl(self.panel, 4200 + id, "Ranged", tc_ro_pos, (60, 20), style = wx.TE_READONLY)
            tc_custom = None
        
        return {'base': tc_base, 'custom': tc_custom}
        
        
    def create_choice_item (self, id):
        item_list = get_item_list()
        pos = {1: (150, 450), 2: (10, 490), 3: (150, 490), 4: (10, 530), 5: (150, 530)}
        
        choice_item = wx.Choice(self.panel, 3300 + id, pos[id], (120, 25), item_list)
        choice_item.SetStringSelection("None")
        
        return choice_item
        
    #************************* Event Functions *************************#
        
    def click (self, event):
        if   (event.GetId() == 2401):           #"Add [Build]" Button
            self.build_add (event)
        elif (event.GetId() == 2402):           #"Remove [Build]" Button
            self.build_remove (event)
        elif (event.GetId() == 2403):           #"Clear" Button
            self.build_clear (event)
        elif (event.GetId() == 2501):           #"DPS" Button
            self.graph ('dps', event)
        elif (event.GetId() == 2502):           #"DPS/gold" Button
            self.graph ('dpspergold', event)           

    def text_change (self, event):
        id = event.GetId()
        if   ((id >= 4210) and (id <= 4220)):   #Champion Stats
            self.tc_validate (id, event)
        elif (id == 4221):                      #Time
            self.tc_validate (id, event)
        elif (id == 4501):                      #Armor
            self.tc_validate (id, event)        
            
    #************************* Other Functions *************************#            
            
    def pick_champ (self, event):
        champ = get_champ(self.choice_champ.GetStringSelection(), load_champs())
        print "Champion chosen: %s" % (champ.name)
        
        cobj =  {0: champ.attack, 1: champ.attack_scaling, 2: champ.speed, 3: champ.speed_scaling, 4: champ.multiplier,                                    #index of champ_objects
                 5: champ.flat_penetration, 6: champ.percent_penetration, 7: champ.critical_chance, 8: champ.critical_damage, 9: champ.type}
        
        for i in xrange(10):
            self.champ_objects[i]['base'].SetValue(str(cobj[i]))
        
        self.tc_champ_level.SetValue(str(champ.level))
    
    def pick_item (self, event):
        global item
        
        item_name = event.GetString()
        event_id  = event.GetId() - 3100
        
        print "Item chosen: %s, ID: %d" % (item_name, event_id)
    
    def tc_validate (self, id, event):
        keycode = event.GetKeyCode()
        
        if (keycode in [wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_SHIFT, wx.WXK_LEFT, wx.WXK_RIGHT]):
            event.Skip()
        elif (keycode < 256):
            char = chr(keycode)
        
        if   ((id >= 4210) and (id < 4220)):                                #Champion Stats (Float)
            if (((keycode >= ord('0')) and (keycode <= ord('9'))) or (keycode == ord('.'))):
                event.Skip()
        elif (id == 4220):                                                  #Level (Int)
            if ((keycode >= ord('0')) and (keycode <= ord('9'))):
                if (self.int_validate(char, 1, 18, self.tc_champ_level)):
                    event.Skip()
        elif (id == 4221):                                                  #Time (Int)
            if ((keycode >= ord('0')) and (keycode <= ord('9'))):
                if (self.int_validate(char, 1, 60, self.tc_time)):
                    event.Skip()
        elif (id == 4501):                                                  #Armor
            if ((keycode >= ord('0')) and (keycode <= ord('9'))):
                if (self.int_validate(char, 50, 500, self.tc_armor)):
                    event.Skip()          
                    
    def int_validate (self, char, min, max, tc):
        text = tc.GetValue() + char
        int_val = int(text)
        
        if   (int_val < min):
            tc.SetValue(str(min))
        elif (int_val > max):
            tc.SetValue(str(max))
        else:
            return True
        
        return False                    

    def build_add (self, event):
        if (self.lb_builds.GetCount() < 6):
            build = self.get_build()
            self.lb_builds.Insert(build['name'], self.lb_builds.GetCount(), build['data'])
            print "Build added: %s" % (build['name'])
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
        
    def build_remove (self, event):
        if (self.lb_builds.GetCount() > 0):
            print "Build removed"   
            self.lb_builds.Delete(self.lb_builds.GetSelection())
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
        
    def build_clear (self, event):
        print "All builds removed"
        self.lb_builds.Clear()
        
    def get_build (self):
        build_name = ""
        champ = get_champ(self.choice_champ.GetStringSelection(), load_champs())
        build_name += champ.name
        
        items = []
        n = 0
        for choice in self.choice_item:
            item_name = choice.GetStringSelection()
            if (item_name != "None"):
                item = get_item(item_name, load_items())
                items.append(item)
                if (n == 0):
                    build_name += "_"
                else:
                    build_name += "+"
                build_name += item.short
            n += 1
        
        time = int(self.tc_time.GetValue())
        build_name += "_" + str(time)
        
        build = {'champ': champ, 'items': items, 'time': time}
        
        return {'name': build_name, 'data': build}
        
    def graph (self, type, event):
        lb = self.lb_builds
        n  = lb.GetCount()
        
        if (n == 0):
            message = wx.MessageBox('Not enough builds to graph.', 'Error', wx.OK | wx.ICON_ERROR)
            return None
        
        builds = []
        
        for i in xrange(n):
            builds.append(lb.GetClientData(i))
            
        if (type == 'dpspergold'):
            for i in xrange(n):
                if (builds[i]['items'] == []):
                    message = wx.MessageBox('Impossible to graph DPS/gold with no items.', 'Error', wx.OK | wx.ICON_ERROR)
                    return None
                
        
        armor = int(self.tc_armor.GetValue())
        
        make_graph (type, armor, builds)
        

#Class end



def run():
    
    app = wx.App(0)
    frame = Prog()

    frame.Show()

    app.MainLoop()


if __name__ == '__main__':    
    run()