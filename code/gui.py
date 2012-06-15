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
ID_location = {'basic': 1000, 'champ': 2000, 'items': 3000, 'builds': 4000, 'graphs': 5000, 'optimal': 6000}
ID_counter  = {'basic': {}, 'champ': {}, 'items': {}, 'builds': {}, 'graphs': {}, 'optimal': {}}

for location in ID_location:
    for type in ID_type:
        ID_counter[location][type] = ID_location[location] + ID_type[type]

# default button size
button_size = {'normal':(80,20), 'big':(160, 40)}

class Prog (wx.Frame):
    """
    Class that implements the main window
    """
    
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
                self.tc_champ_stats[i]['extra'].Bind(wx.EVT_CHAR, self.key_press)
                self.Bind(wx.EVT_TEXT, self.text_change, self.tc_champ_stats[i]['extra'])
        
        wx.StaticText(self.panel, new_id('t_champ_level', 'champ', 'text'), "Level:",                       (150,15))
        self.tc_champ_level = wx.TextCtrl(self.panel, new_id('tc_champ_level', 'champ', 'textcontrol'), "0", (190,14), (40, 20))
        self.tc_champ_level.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_champ_level)
        
        wx.StaticText(self.panel, new_id('t_time', 'champ', 'text'), "Time (1s to 60s):",      (250,15))
        self.tc_time = wx.TextCtrl(self.panel, new_id('tc_time', 'champ', 'textcontrol'), "5", (340,14), (40, 20))
        self.tc_time.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_time)
        
        #************************* Items (IDs 3xxx) *************************#
        
        wx.StaticText(self.panel, new_id('t_tiers', 'items', 'text'), "Tiers:", (10, 350))
        self.cb_tier_1 = wx.CheckBox(self.panel, new_id('cb_tier_1', 'items', 'checkbox'), "Basic",     (10, 370))
        self.Bind(wx.EVT_CHECKBOX, self.tier_change, self.cb_tier_1)
        self.cb_tier_2 = wx.CheckBox(self.panel, new_id('cb_tier_2', 'items', 'checkbox'), "Advanced",  (10, 390))
        self.Bind(wx.EVT_CHECKBOX, self.tier_change, self.cb_tier_2)
        self.cb_tier_3 = wx.CheckBox(self.panel, new_id('cb_tier_3', 'items', 'checkbox'), "Legendary", (10, 410))
        self.Bind(wx.EVT_CHECKBOX, self.tier_change, self.cb_tier_3)

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
        
        wx.StaticText(self.panel, new_id('t_dps_min', 'graphs', 'text'), "Minimum DPS:",              (10,81))
        self.tc_dps_min = wx.TextCtrl(self.panel, new_id('tc_dps_min', 'graphs', 'textcontrol'), "0", (95,80), (40, 20), style = wx.TE_READONLY)
        
        wx.StaticText(self.panel, new_id('t_dps_avg', 'graphs', 'text'), "Average DPS:",              (200,81))
        self.tc_dps_avg = wx.TextCtrl(self.panel, new_id('tc_dps_avg', 'graphs', 'textcontrol'), "0", (285,80), (40, 20), style = wx.TE_READONLY)
        
        wx.StaticText(self.panel, new_id('t_dps_max', 'graphs', 'text'), "Maximum DPS:",              (390,81))
        self.tc_dps_max = wx.TextCtrl(self.panel, new_id('tc_dps_max', 'graphs', 'textcontrol'), "0", (475,80), (40, 20), style = wx.TE_READONLY)
        
        wx.StaticText(self.panel, new_id('t_armor', 'graphs', 'text'), "Graph until x Armor (min: 50, max: 500):", (400,15))
        self.tc_armor = wx.TextCtrl(self.panel, new_id('tc_armor', 'graphs', 'textcontrol'), "300",                (615,14), (40, 20))
        self.tc_armor.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_armor)
        
        button = wx.Button(self.panel, new_id('b_graphs_dps', 'graphs', 'button'), "DPS",          (600, 130), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, new_id('b_graphs_dpsgold', 'graphs', 'button'), "DPS/gold", (600, 180), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        self.cb_file = wx.CheckBox(self.panel, new_id('cb_file', 'graphs', 'checkbox'), "Save graph to file:", (600, 80))
        self.tc_file = wx.TextCtrl(self.panel, new_id('tc_file', 'graphs', 'textcontrol'), "graph",            (620, 100), (140, 20))
        self.tc_file.SetMaxLength(20)
        self.tc_file.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_file)
        
        #************************* Optimal Build (IDs 6xxx) *************************#
        
        wx.StaticText(self.panel, new_id('t_budget', 'optimal', 'text'), "Budget:",                                 (220, 350))
        
        wx.StaticText(self.panel, new_id('t_budget_min', 'optimal', 'text'), "Minimum:",                            (220, 376))
        self.tc_budget_min = wx.TextCtrl(self.panel, new_id('tc_budget_min', 'optimal', 'textcontrol'), "0",        (280, 375), (50, 20))
        self.tc_budget_min.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_budget_min)
        
        wx.StaticText(self.panel, new_id('t_budget_max', 'optimal', 'text'), "Maximum:",                            (220, 401))
        self.tc_budget_max = wx.TextCtrl(self.panel, new_id('tc_budget_max', 'optimal', 'textcontrol'), "25000",    (280, 400), (50, 20))
        self.tc_budget_max.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_budget_max)
        
        wx.StaticText(self.panel, new_id('t_n_items', 'optimal', 'text'), "Number of items:",                       (360, 350))
        self.choice_n_items = wx.Choice(self.panel, new_id('choice_n_items', 'optimal', 'choice'),                  (360, 375), (50, 20), ['1','2','3','4','5'])
        
        button = wx.Button(self.panel, new_id('b_graphs_dps_optimal', 'optimal', 'button'), "Optimal DPS",          (600, 250), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, new_id('b_graphs_dpsgold_optimal', 'optimal', 'button'), "Optimal DPS/gold", (600, 300), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        wx.StaticText(self.panel, new_id('t_armor_val', 'optimal', 'text'), "Current Armor:",                       (615, 351))
        self.tc_armor_val = wx.TextCtrl(self.panel, new_id('tc_armor_val', 'optimal', 'textcontrol'), "0",          (700, 350), (40, 20), style = wx.TE_READONLY)
        
        #************************* Defaults *************************#
        self.choice_champ.SetSelection(0)
        self.pick_champ(None)
        self.cb_tier_1.SetValue(1)
        self.cb_tier_2.SetValue(1)
        self.cb_tier_3.SetValue(1)
        self.choice_n_items.SetStringSelection('2')
        
        
    def create_champ_objects (self):
        """
        Creates the objects for the various champ stats
        """
        
        id_base = ID_location['champ'] + ID_type['textcontrol']
        id      = ID_counter['champ']['textcontrol'] - id_base
        
        name = {0: 'Attack Damage', 1: 'Attack Scaling', 2: 'Attack Speed', 3: 'Speed Scaling', 4: 'Multiplier',
                5: 'Flat Penetration', 6: 'Percent Penetration', 7: 'Critical Chance', 8: 'Critical Damage', 9: 'Type'}
        
        y_base   = 140
        y_per_id = 40
        tc_size  = (45, 20)
        
        if (id < 5):
            txt_pos   = (010, y_base + id*y_per_id)
            tc_ro_pos = (100, y_base + id*y_per_id)
            tc_ex_pos = (150, y_base + id*y_per_id)
            tc_pos    = (200, y_base + id*y_per_id)
        else:
            txt_pos   = (260, y_base + (id-5)*y_per_id)
            tc_ro_pos = (370, y_base + (id-5)*y_per_id)
            tc_ex_pos = (420, y_base + (id-5)*y_per_id)
            tc_pos    = (470, y_base + (id-5)*y_per_id)
        
        if   (id == 0):
            ID['t_stat_champ_1'] = ID_location['champ'] + ID_type['text'] + 15
            wx.StaticText(self.panel, ID['t_stat_champ_1'], "Champ", (100, 120))
            ID['t_stat_item_1'] = ID_location['champ'] + ID_type['text'] + 16
            wx.StaticText(self.panel, ID['t_stat_item_1'], "Items", (157, 120))
            ID['t_stat_extra_1'] = ID_location['champ'] + ID_type['text'] + 17
            wx.StaticText(self.panel, ID['t_stat_extra_1'], "Extra", (205, 120))
        elif (id == 5):
            ID['t_stat_champ_2'] = ID_location['champ'] + ID_type['text'] + 18
            wx.StaticText(self.panel, ID['t_stat_champ_1'], "Champ", (370, 120))
            ID['t_stat_item_2'] = ID_location['champ'] + ID_type['text'] + 19
            wx.StaticText(self.panel, ID['t_stat_item_1'], "Items", (427, 120))
            ID['t_stat_extra_2'] = ID_location['champ'] + ID_type['text'] + 20
            wx.StaticText(self.panel, ID['t_stat_extra_1'], "Extra", (475, 120))
        
        id_name = '_champ_' + name[id].lower().replace(' ', '_')

        ID['t' + id_name] = id + ID_location['champ'] + ID_type['text']
        wx.StaticText(self.panel, ID['t' + id_name], name[id] + ':', txt_pos)
        
        if (id != 9):
            ID['tc' + id_name + '_base'] = id_base + id
            tc_base = wx.TextCtrl(self.panel, ID['tc' + id_name + '_base'], "0", tc_ro_pos, tc_size, style = wx.TE_READONLY)
            ID['tc' + id_name + '_item'] = id_base + id + 10
            tc_item = wx.TextCtrl(self.panel, ID['tc' + id_name + '_item'], "0", tc_ex_pos, tc_size, style = wx.TE_READONLY)
            ID['tc' + id_name + '_extra'] = id_base + id + 20
            tc_extra = wx.TextCtrl(self.panel, ID['tc' + id_name + '_extra'], "0", tc_pos, tc_size)
        else: 
            ID['tc' + id_name + '_base'] = id_base + id
            tc_base  = wx.TextCtrl(self.panel, ID['tc' + id_name + '_base'], "Ranged", tc_ro_pos, (60, 20), style = wx.TE_READONLY)
            tc_item  = None
            tc_extra = None
        
        ID_counter['champ']['text'] += 1
        ID_counter['champ']['textcontrol'] += 1
        if (id == 9):
            ID_counter['champ']['textcontrol'] += 19
        
        return {'base': tc_base, 'item': tc_item, 'extra': tc_extra}
        
        
    def create_choice_item (self):
        """
        Creates the choices for the 5 items
        """
    
        id_base = ID_location['items'] + ID_type['choice']
        id      = ID_counter['items']['choice'] - id_base
    
        item_list = get_item_list()
        pos = {0: (150, 450), 1: (10, 490), 2: (150, 490), 3: (10, 530), 4: (150, 530)}
        
        choice_item = wx.Choice(self.panel, id_base + id, pos[id], (120, 25), item_list)
        choice_item.SetStringSelection("None")
        
        ID_counter['items']['choice'] += 1
        ID['tc_choice_' + str(id)] = id_base + id
        
        return choice_item
        
    #************************* Event Functions *************************#
        
    def click (self, event):
        """
        Button click redirect
        """
    
        id = event.GetId()
        
        if   (id == ID['b_builds_add']):                 #"Add [Build]" Button
            self.build_add (event)
        elif (id == ID['b_builds_remove']):              #"Remove [Build]" Button
            self.build_remove (event)
        elif (id == ID['b_builds_clear']):               #"Clear" Button
            self.build_clear (event)
        elif (id == ID['b_graphs_dps']):                 #"DPS" Button
            self.graph ('dps', event)
        elif (id == ID['b_graphs_dpsgold']):             #"DPS/gold" Button
            self.graph ('dpspergold', event)           
        elif (id == ID['b_graphs_dps_optimal']):                 #"DPS" Button
            self.calc_optimal_builds ('dps', event)
        elif (id == ID['b_graphs_dpsgold_optimal']):             #"DPS/gold" Button
            self.calc_optimal_builds ('dpspergold', event)
    
    def text_change (self, event):
        """
        Text change redirect
        """
        
        id = event.GetId()
        if   (id == ID['tc_champ_level']):
            self.int_validate(self.tc_champ_level, 1, 18)
        elif (id == ID['tc_time']): 
            self.int_validate(self.tc_time, 1, 60)
        elif (id == ID['tc_armor']):
            self.int_validate(self.tc_armor, 50, 500)
        elif (id == ID['tc_budget_min']):
            self.int_validate(self.tc_budget_min, 0, 25000)
        elif (id == ID['tc_budget_max']):
            self.int_validate(self.tc_budget_max, 0, 25000)
        
        self.update_stats()
    
    def key_press (self, event):
        """
        Key press redirect
        """
        
        self.tc_validate_key (event)
        
    def tier_change (self, event):
        tiers = {}
        tiers['None']      = 1
        tiers['Basic']     = int(self.cb_tier_1.GetValue())
        tiers['Advanced']  = int(self.cb_tier_2.GetValue())
        tiers['Legendary'] = int(self.cb_tier_3.GetValue())
        
        items     = filter_items_tiers(tiers)
        item_list = get_item_list(items)
        
        for i in xrange(5):
            self.choice_item[i].Clear()
            self.choice_item[i].AppendItems(item_list)
            self.choice_item[i].SetStringSelection("None")
        
    #************************* Other Functions *************************#            
            
    def pick_champ (self, event):
        """
        Update stats after changing the champ in choice_champ
        """
        
        champ = get_champ(self.choice_champ.GetStringSelection())
        print "Champion chosen: %s" % (champ.name)
        
        self.update_stats()
        self.tc_champ_stats[9]['base'] = champ.type
        self.tc_champ_level.SetValue(str(champ.level))
    
    def pick_item (self, event):
        """
        Update stats after changing an item
        """
        
        item_name = event.GetString()
        event_id  = event.GetId()
        
        self.update_stats()
        
        print "Item chosen: %s" % (item_name)
    
    def update_stats (self):
        """
        Update stats after a change in the build
        """
        
        stats = {0: 'attack', 1: 'attack_scaling', 2: 'speed', 3: 'speed_scaling', 4: 'multiplier',
                5: 'flat_penetration', 6: 'percent_penetration', 7: 'critical_chance', 8: 'critical_damage'}
        
        champ = get_champ(self.choice_champ.GetStringSelection())
        
        extra = {}
        for i in xrange(9):
            extra[stats[i]] = float(self.tc_champ_stats[i]['extra'].GetValue())
        extra['level'] = int(self.tc_champ_level.GetValue())
        
        items = []
        for choice in self.choice_item:
            item_name = choice.GetStringSelection()
            if (item_name != "None"):
                item = get_item(item_name)
                items.append(item)
        
        time = int(self.tc_time.GetValue())
        armor = int(self.tc_armor.GetValue())
        
        for stat in stats:
            value = champ[stats[stat]]
            self.tc_champ_stats[stat]['base'].SetValue(str(value))
            value = 0
            
            b  = 0
            gb = 0
            ie = 0
            lw = 0
            
            for item in items:
                if (((stats[stat] == 'flat_penetration')    and (item.short.lower() == "b")  and (b  != 0)) or
                    ((stats[stat] == 'flat_penetration')    and (item.short.lower() == "gb") and (gb != 0)) or
                    ((stats[stat] == 'critical_damage')     and (item.short.lower() == "ie") and (ie != 0)) or
                    ((stats[stat] == 'percent_penetration') and (item.short.lower() == "lw") and (lw != 0))):
                    continue
                
                value += item[stats[stat]]
                if (DEBUG): print item.short + ":", stats[stat], "=", item[stats[stat]]
                
                if (item.short.lower() == "b"):  b  = 1
                if (item.short.lower() == "ie"): ie = 1
                if (item.short.lower() == "gb"): gb = 1
                if (item.short.lower() == "lw"): lw = 1
            
            if (stats[stat] == 'critical_chance') and (value > 1):
                value = 1
            
            self.tc_champ_stats[stat]['item'].SetValue(str(value))
            
        self.tc_dps_min.SetValue(str(int(calc_dps(armor, champ, extra, items, time))))
        self.tc_dps_avg.SetValue(str(int(calc_dps(armor/2, champ, extra, items, time))))
        self.tc_dps_max.SetValue(str(int(calc_dps(0, champ, extra, items, time))))
        
    def tc_validate_key (self, event):
        """
        Validate Key (prevent, for example, letters in number-only textcontrols)
        """
        
        id      = event.GetId()
        keycode = event.GetKeyCode()
        
        if (keycode in [wx.WXK_BACK, wx.WXK_DELETE, wx.WXK_SHIFT, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_CONTROL, wx.WXK_END, wx.WXK_HOME]
			or event.ControlDown()):
            event.Skip()
        
        if   ((id >= ID['tc_champ_attack_damage_extra']) and (id <= ID['tc_champ_critical_damage_extra'])):                                
            if (((keycode >= ord('0')) and (keycode <= ord('9'))) or (keycode == ord('.'))):
                event.Skip()
        elif (id in [ID['tc_champ_level'], ID['tc_time'], ID['tc_armor'], ID['tc_budget_min'], ID['tc_budget_max']]):                                     
            if ((keycode >= ord('0')) and (keycode <= ord('9'))):
                event.Skip()
        elif (id == ID['tc_file']):
            if (((keycode >= ord('0')) and (keycode <= ord('9'))) or
                ((keycode >= ord('a')) and (keycode <= ord('z'))) or
                ((keycode >= ord('A')) and (keycode <= ord('Z'))) or
                (keycode == ord('_'))):
                event.Skip()
                    
    def int_validate (self, tc, min, max):
        """
        Check if the new value is within the limits
        """
        
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
        """
        Add a build to the list
        """
        
        if (self.lb_builds.GetCount() < 5):
            build = self.get_build()
            self.lb_builds.Insert(build['name'], self.lb_builds.GetCount(), build['data'])
            print "Build added: %s" % (build['name'])
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
        
    def build_remove (self, event):
        """
        Remove the build from the list
        """
        
        if (self.lb_builds.GetCount() > 0):
            print "Build removed"   
            self.lb_builds.Delete(self.lb_builds.GetSelection())
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
        
    def build_clear (self, event):
        """
        Clear all builds from the list
        """
        
        print "All builds removed"
        self.lb_builds.Clear()
        
    def get_build (self):
        """
        Get build from stats
        """
    
        build_name = ""
        champ = get_champ(self.choice_champ.GetStringSelection())
        build_name += champ.name
        
        stats = {0: 'attack', 1: 'attack_scaling', 2: 'speed', 3: 'speed_scaling', 4: 'multiplier',
                5: 'flat_penetration', 6: 'percent_penetration', 7: 'critical_chance', 8: 'critical_damage'}
        
        extra = {}
        for i in xrange(9):
            extra[stats[i]] = float(self.tc_champ_stats[i]['extra'].GetValue())
        extra['level'] = int(self.tc_champ_level.GetValue())
        
        build_name += "_l=" + str(extra['level'])
        
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
        build_name += "_t=" + str(time)
        
        build = {'champ': champ, 'extra': extra, 'items': items, 'time': time}
        
        return {'name': build_name, 'data': build}
        
    def graph (self, type, event):
        """
        Graph the builds
        """
        
        lb = self.lb_builds
        n  = lb.GetCount()
        
        armor = int(self.tc_armor.GetValue())
        
        if (self.cb_file.GetValue()):
            file = self.tc_file.GetValue()
            if (file == ""):
                file = "graph"
        else:
            file = None
        
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
        
        make_graph (type, armor, builds, file)
        
    def calc_optimal_builds (self, type, event):
        """
        Calculate the optimal build for each armor in the range of armors
        """
        
        tiers = {}
        tiers['None']      = 0
        tiers['Basic']     = int(self.cb_tier_1.GetValue())
        tiers['Advanced']  = int(self.cb_tier_2.GetValue())
        tiers['Legendary'] = int(self.cb_tier_3.GetValue())
        
        armor_max = int(self.tc_armor.GetValue()) + 1
        
        min_price = int(self.tc_budget_min.GetValue())
        max_price = int(self.tc_budget_max.GetValue())
        n_items   = int(self.choice_n_items.GetStringSelection())
        
        if (min_price > max_price):
            temp      = max_price
            max_price = min_price
            min_price = temp
            
        build        = self.get_build()['data']
        champ        = build['champ']
        preset_items = build['items']
        extra        = build['extra']
        time         = build['time']
        
        n_items -= len(preset_items)
        if (n_items < 1):
            message = wx.MessageBox('Number of chosen items is equal or larger than number of items to calculate.', 'Error', wx.OK | wx.ICON_ERROR)
            return None
        
        all_labels = []
        builds     = []
        
        n = 0
        self.lb_builds.Clear()
        for armor in xrange(armor_max):
            wx.Yield()
            self.tc_armor_val.SetValue(str(armor))
            old_dps   = 0
            champ_dps = calc_dps(armor, champ, extra, [], time)
            
            for items in comb_rep (filter_items_tiers(tiers), n_items):
                new_items = list(preset_items) + list(items)
                
                total_price = 0
                for item in new_items:
                    total_price += item.price
                    
                if ((total_price < min_price) or (total_price > max_price)):
                    continue
                
                dps = calc_dps(armor, champ, extra, new_items, time)
                if (type == 'dpspergold') and not (total_price == 0):
                    dps -= champ_dps
                    dps /= total_price
                if (dps > old_dps):
                    optimal_items = new_items
                    old_dps = dps
            
            #optimal_items = self.optimal_build (armor, champ, extra, preset_items, time, n_items, tiers, min_price, max_price)
            
            new_label = get_label(champ, extra['level'], optimal_items, time)
            
            if not (new_label in all_labels):
                build = {'champ': champ, 'extra': extra, 'items': optimal_items, 'time': time}
                builds.append(build)
                self.lb_builds.Insert(new_label, n, build)
                all_labels.append(new_label)
                n += 1
                if (n > 8): break
        
        #self.tc_armor_val.SetValue('0')
    
    def optimal_build (self, armor, champ, extra, preset_items, time, n_items, tiers, min_price, max_price):
        
                
        return optimal_items

#Class end

def new_id (name, location, type):
    """
    Create new ID from type, location and last ID of the same type and location
    """
    
    id = ID_counter[location][type]
    ID_counter[location][type] += 1
    ID[name] = id
    
    return id

def run():
    """
    GUI Main
    """
    
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
    wait()