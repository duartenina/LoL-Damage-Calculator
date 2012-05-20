import wx
import operator

from code.champ import *
from code.graph import *
from code.item  import *
from code.extra import *


""" wxStuff

    IDs:
        x0xx -> Frame
        x1xx -> StaticText
        x2xx -> Button
        x3xx -> Choice
        x4xx -> TextCtrl
        x5xx -> ListBox
        x6xx -> CheckBox
        
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

#IDs

#Dictionary with all objects' name and ID
ID = {}                                                                                            

#Counter to the last object of the same type and location
ID_type     = {'frame': 100, 'text': 200, 'button': 300, 'choice': 400, 'textcontrol': 500, 'listbox': 600, 'checkbox': 700}
ID_location = {'basic': 1000, 'champ': 2000, 'items': 3000, 'builds': 4000, 'graphs': 5000}
ID_counter  = {'basic': {}, 'champ': {}, 'items': {}, 'builds': {}, 'graphs': {}}

for location in ID_location:
    for type in ID_type:
        ID_counter[location][type] = ID_location[location] + ID_type[type]

# default button size
button_size = {'normal':(80,20), 'big':(160, 40)}

#Debug option
DEBUG = False

class Prog (wx.Frame):
    def __init__ (self):
        #************************* Basic Stuff (IDs 1xxx) *************************#
        wx.Frame.__init__(self, None, new_id('frame', 'basic', 'frame'), "LoL Damage Calculator", size = (800,600), style = wx.DEFAULT_FRAME_STYLE)
		#style = wx.CAPTION | wx.CLOSE_BOX)
        
        #self.CenterOnScreen()
        
        self.panel = wx.Panel (self, new_id('panel', 'basic', 'frame'))
        
        #************************* Champion (IDs 2xxx) *************************#
        
        
        self.choice_champ = wx.Choice(self.panel, new_id('choice_champ', 'champ', 'choice') , (10,10), (120, 25), get_champion_list())
        self.Bind(wx.EVT_CHOICE, self.pick_champ, self.choice_champ)
        
        self.tc_champ_stats = []
        
        for i in xrange(10):
            self.tc_champ_stats.append(self.create_champ_objects())
            if (i != 9):
                self.tc_champ_stats[i]['custom'].Bind(wx.EVT_CHAR, self.key_press)
                self.Bind(wx.EVT_TEXT, self.text_change, self.tc_champ_stats[i]['custom'])
            
        wx.StaticText(self.panel, new_id('t_champ_level', 'champ', 'text'), "Level:",                       (150,15))
        self.tc_champ_level = wx.TextCtrl(self.panel, new_id('tc_champ_level', 'champ', 'textcontrol'), "0", (190,14), (40, 20))
        self.tc_champ_level.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_champ_level)
        
        wx.StaticText(self.panel, new_id('t_time', 'champ', 'text'), "Time (1s to 60s):",      (250,15))
        self.tc_time = wx.TextCtrl(self.panel, new_id('tc_time', 'champ', 'textcontrol'), "5", (340,14), (40, 20))
        self.tc_time.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_time)
        
        self.choice_champ.SetSelection(0)
        self.pick_champ(None)
        
        #************************* Items (IDs 3xxx) *************************#
        
        wx.StaticText(self.panel, new_id('t_items', 'items', 'text'), "Items:", (10, 450))
        
        self.choice_item = []
        for i in xrange(5):
            self.choice_item.append(self.create_choice_item())
            self.Bind(wx.EVT_CHOICE, self.pick_item, self.choice_item[i])
       
        #************************* Builds (IDs 4xxx) *************************#
        
        wx.StaticText(self.panel, new_id('t_builds', 'builds', 'text'), "Builds:", (330, 450))
        self.lb_builds = wx.ListBox(self.panel, new_id('lb_builds', 'builds', 'listbox'), (330, 470), (350, 80), [], wx.LB_SINGLE)
        
        button = wx.Button(self.panel, new_id('b_builds_add', 'builds', 'button'), "Add",       (690, 470), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, new_id('b_builds_remove', 'builds', 'button'), "Remove", (690, 500), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, new_id('b_builds_clear', 'builds', 'button'), "Clear",   (690, 530), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        #************************* Graphs (IDs 5xxx) *************************#
        
        wx.StaticText(self.panel, new_id('t_armor', 'graphs', 'text'), "Graph until x Armor (min: 50, max: 500):", (400,15))
        self.tc_armor = wx.TextCtrl(self.panel, new_id('tc_armor', 'graphs', 'textcontrol'), "300",                (615,14), (40, 20))
        self.tc_armor.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_armor)
        
        button = wx.Button(self.panel, new_id('b_graphs_dps', 'graphs', 'button'), "DPS",          (600, 130), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, new_id('b_graphs_dpsgold', 'graphs', 'button'), "DPS/gold", (600, 180), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        self.cb_file = wx.CheckBox(self.panel, new_id('cb_file', 'graphs', 'checkbox'), "Save to file", (600, 230))
        #wx.StaticText(self.panel, new_id('t_file', 'graphs', 'text'), "File name:",                     (600, 250))
        self.tc_file = wx.TextCtrl(self.panel, new_id('tc_file', 'graphs', 'textcontrol'), "graph",     (600, 250), (150, 20))
        self.tc_file.SetMaxLength(20)
        self.tc_file.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_file)
        
    def create_champ_objects (self):
        id_base = ID_location['champ'] + ID_type['textcontrol']
        id      = ID_counter['champ']['textcontrol'] - id_base
    
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
            
        id_name = '_champ_' + name[id].lower().replace(' ', '_')

        ID['t' + id_name] = id + ID_location['champ'] + ID_type['text']
        wx.StaticText(self.panel, ID['t' + id_name], name[id] + ':', txt_pos)
        
        if (id != 9):
            ID['tc' + id_name + '_base'] = id_base + id
            tc_base = wx.TextCtrl(self.panel, ID['tc' + id_name + '_base'], "0", tc_ro_pos, (50, 20), style = wx.TE_READONLY)
            ID['tc' + id_name + '_custom'] = id_base + id + 10
            tc_custom = wx.TextCtrl(self.panel, ID['tc' + id_name + '_custom'], "0", tc_pos, (50, 20))
        else: 
            ID['tc' + id_name + '_base'] = id_base + id
            tc_base = wx.TextCtrl(self.panel, ID['tc' + id_name + '_base'], "Ranged", tc_ro_pos, (60, 20), style = wx.TE_READONLY)
            tc_custom = None
        
        ID_counter['champ']['text'] += 1
        ID_counter['champ']['textcontrol'] += 1
        if (id == 9):
            ID_counter['champ']['textcontrol'] += 9
        
        return {'base': tc_base, 'custom': tc_custom}
        
        
    def create_choice_item (self):
        id_base = ID_location['items'] + ID_type['choice']
        id      = ID_counter['items']['choice'] - id_base
    
        item_list = get_item_list()
        pos = {0: (150, 450), 1: (10, 490), 2: (150, 490), 3: (10, 530), 4: (150, 530)}
        
        choice_item = wx.Choice(self.panel, id_base + id, pos[id], (120, 25), item_list)
        choice_item.SetStringSelection("None")
        
        ID_counter['items']['choice'] += 1
        
        return choice_item
        
    #************************* Event Functions *************************#
        
    def click (self, event):
        if   (event.GetId() == ID['b_builds_add']):                 #"Add [Build]" Button
            self.build_add (event)
        elif (event.GetId() == ID['b_builds_remove']):              #"Remove [Build]" Button
            self.build_remove (event)
        elif (event.GetId() == ID['b_builds_clear']):               #"Clear" Button
            self.build_clear (event)
        elif (event.GetId() == ID['b_graphs_dps']):                 #"DPS" Button
            self.graph ('dps', event)
        elif (event.GetId() == ID['b_graphs_dpsgold']):             #"DPS/gold" Button
            self.graph ('dpspergold', event)           
    
    def text_change (self, event):
        id = event.GetId()
        if   (id == ID['tc_champ_level']):
            self.int_validate(self.tc_champ_level, 1, 18)
        elif (id == ID['tc_time']): 
            self.int_validate(self.tc_time, 1, 60)
        elif (id == ID['tc_armor']):
            self.int_validate(self.tc_armor, 50, 500)
    
    def key_press (self, event):
        self.tc_validate_key (event)
            
    #************************* Other Functions *************************#            
            
    def pick_champ (self, event):
        champ = get_champ(self.choice_champ.GetStringSelection())
        print "Champion chosen: %s" % (champ.name)
        
        cobj =  {0: champ.attack, 1: champ.attack_scaling, 2: champ.speed, 3: champ.speed_scaling, 4: champ.multiplier,                                    #index of champ_objects
                 5: champ.flat_penetration, 6: champ.percent_penetration, 7: champ.critical_chance, 8: champ.critical_damage, 9: champ.type}
        
        for i in xrange(10):
            self.tc_champ_stats[i]['base'].SetValue(str(cobj[i]))
        
        self.tc_champ_level.SetValue(str(champ.level))
    
    def pick_item (self, event):
        item_name = event.GetString()
        event_id  = event.GetId()
        
        print "Item chosen: %s" % (item_name)
    
    def tc_validate_key (self, event):
        id      = event.GetId()
        keycode = event.GetKeyCode()
        
        if (keycode in [wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_SHIFT, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_CONTROL, wx.WXK_END, wx.WXK_HOME]
			or event.ControlDown()):
            event.Skip()
        elif (keycode < 256):
            char = chr(keycode)
        
        if   ((id >= ID['tc_champ_attack_damage_custom']) and (id <= ID['tc_champ_critical_damage_custom'])):                                
            if (((keycode >= ord('0')) and (keycode <= ord('9'))) or (keycode == ord('.'))):
                event.Skip()
        elif (id in [ID['tc_champ_level'], ID['tc_time'], ID['tc_armor']]):                                     
            if ((keycode >= ord('0')) and (keycode <= ord('9'))):
                event.Skip()
        elif (id == ID['tc_file']):
            if (((keycode >= ord('0')) and (keycode <= ord('9'))) or
                ((keycode >= ord('a')) and (keycode <= ord('z'))) or
                ((keycode >= ord('A')) and (keycode <= ord('Z'))) or
                (keycode == ord('_'))):
                event.Skip()
                    
    def int_validate (self, tc, min, max):
        text = tc.GetValue()
        int_val = int(text)
        
        if   (int_val < min):
            tc.SetValue(str(min))
        elif (int_val > max):
            tc.SetValue(str(max))
        else:
            return True
        
        return False                    

    def build_add (self, event):
        if (self.lb_builds.GetCount() < 5):
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
        champ = get_champ(self.choice_champ.GetStringSelection())
        build_name += champ.name
        
        stats = {0: 'attack', 1: 'attack_scaling', 2: 'speed', 3: 'speed_scaling', 4: 'multiplier',
                5: 'flat_penetration', 6: 'percent_penetration', 7: 'critical_chance', 8: 'critical_damage'}
        
        extra = {}
        
        for i in xrange(9):
            extra[stats[i]] = float(self.tc_champ_stats[i]['custom'].GetValue())
        
        items = []
        n = 0
        for choice in self.choice_item:
            item_name = choice.GetStringSelection()
            if (item_name != "None"):
                item = get_item(item_name)
                items.append(item)
                if (n == 0):
                    build_name += "_"
                else:
                    build_name += "+"
                build_name += item.short
            n += 1
        
        time = int(self.tc_time.GetValue())
        build_name += "_" + str(time)
        
        build = {'champ': champ, 'extra': extra, 'items': items, 'time': time}
        
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
        
        if (self.cb_file.GetValue()):
            file = self.tc_file.GetValue()
            if (file == ""):
                file = "graph"
        else:
            file = None
        
        make_graph (type, armor, builds, file)
        

#Class end

def new_id (name, location, type):
    global ID
    
    id = ID_counter[location][type]
    ID_counter[location][type] += 1
    ID[name] = id
    
    return id

def run():
    
    app = wx.App(0)
    frame = Prog()

    frame.Show()

    app.MainLoop()
    
    if (DEBUG):
        f = open("ids.log","w")
    
        id_sorted = sorted(ID.iteritems(), key=operator.itemgetter(1))
    
        for id in id_sorted:
            f.write("%d: %s\n" % (id[1], id[0]))
    
        f.close()

if __name__ == '__main__':    
    run()