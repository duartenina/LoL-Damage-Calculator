import wx
import operator

from code.champ import *
from code.graph import *
from code.item  import *
from code.extra import *

#************************* Global Variables *************************#

VERSION = 3.0

#IDs

#Dictionary with all objects' name and ID
ID = {}                                                                                            

#Counter to the last object of the same type and location
ID_type     = {'frame': 100, 'text': 200, 'button': 300, 'choice': 400, 'textcontrol': 500, 'listbox': 600, 'checkbox': 700, 'gauge': 800, 'timer': 900}
ID_location = {'basic': 1000, 'champ': 2000, 'items': 3000, 'builds': 4000, 'graphs': 5000, 'optimal': 6000, 'optimal_path': 7000}
ID_counter  = {'basic': {}, 'champ': {}, 'items': {}, 'builds': {}, 'graphs': {}, 'optimal': {}, 'optimal_path': {}}

for location in ID_location:
    for type in ID_type:
        ID_counter[location][type] = ID_location[location] + ID_type[type]

# default button size
button_size = {'normal':(80,20), 'big':(140, 40)}

#********************************************************************#

class Prog (wx.Frame):
    """
    Class that implements the main window
    """
    
    def __init__ (self):
        #************************* Basic Stuff (IDs 1xxx) *************************#
        wx.Frame.__init__(self, None, new_id('frame', 'basic', 'frame'), "LoL Damage Calculator v" + str(VERSION), size = (800,600), style = wx.DEFAULT_FRAME_STYLE)
		#style = wx.CAPTION | wx.CLOSE_BOX)
        
        #self.CenterOnScreen()
        
        self.panel = wx.Panel (self, new_id('panel', 'basic', 'frame'))
        
        #************************* Champion (IDs 2xxx) *************************#
        
        wx.StaticBox(self.panel, new_id('box_champ', 'champ', 'frame'), "Champion Stats", (5, 40), (520, 180))
        
        self.choice_champ = wx.Choice(self.panel, new_id('choice_champ', 'champ', 'choice') , (10,10), (120, 25), get_champion_list())
        self.Bind(wx.EVT_CHOICE, self.pick_champ, self.choice_champ)
        
        self.tc_champ_stats = []
        
        for i in xrange(10):
            self.tc_champ_stats.append(self.create_champ_objects(i))
            self.tc_champ_stats[i]['extra'].Bind(wx.EVT_CHAR, self.key_press)
            self.Bind(wx.EVT_TEXT, self.text_change, self.tc_champ_stats[i]['extra'])
        
        wx.StaticText(self.panel, new_id('t_champ_level', 'champ', 'text'), "Level:",                        (150,15))
        self.tc_champ_level = wx.TextCtrl(self.panel, new_id('tc_champ_level', 'champ', 'textcontrol'), "0", (190,14), (40, 20))
        self.tc_champ_level.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_champ_level)
        
        wx.StaticText(self.panel, new_id('t_time', 'champ', 'text'), "Time (1s to 60s):",      (250,15))
        self.tc_time = wx.TextCtrl(self.panel, new_id('tc_time', 'champ', 'textcontrol'), "5", (340,14), (40, 20))
        self.tc_time.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_time)
        
        wx.StaticText(self.panel, new_id('t_boost', 'champ', 'text'), 'Boosts:',                                           (215, 240))
        
        self.cb_boost_item = wx.CheckBox(self.panel, new_id('cb_boost_item', 'champ', 'checkbox'), 'Item Actives',         (215, 266))
        self.Bind(wx.EVT_CHECKBOX, self.change_option, self.cb_boost_item)
        self.cb_boost_champ = wx.CheckBox(self.panel, new_id('cb_boost_champ', 'champ', 'checkbox'), 'Champion Abilities', (215, 290))
        self.Bind(wx.EVT_CHECKBOX, self.change_option, self.cb_boost_champ)
        
        #************************* Items (IDs 3xxx) *************************#
        
        wx.StaticText(self.panel, new_id('t_tiers', 'items', 'text'), "Tiers:",                         (340, 240))
        self.cb_tier_1 = wx.CheckBox(self.panel, new_id('cb_tier_1', 'items', 'checkbox'), "Basic",     (340, 260))
        self.Bind(wx.EVT_CHECKBOX, self.tier_change, self.cb_tier_1)
        self.cb_tier_2 = wx.CheckBox(self.panel, new_id('cb_tier_2', 'items', 'checkbox'), "Advanced",  (340, 280))
        self.Bind(wx.EVT_CHECKBOX, self.tier_change, self.cb_tier_2)
        self.cb_tier_3 = wx.CheckBox(self.panel, new_id('cb_tier_3', 'items', 'checkbox'), "Legendary", (340, 300))
        self.Bind(wx.EVT_CHECKBOX, self.tier_change, self.cb_tier_3)

        wx.StaticBox(self.panel, new_id('box_items', 'items', 'frame'), "Items", (530, 40), (250, 110))
        
        self.choice_item = []
        for i in xrange(6):
            self.choice_item.append(self.create_choice_item(i))
            self.Bind(wx.EVT_CHOICE, self.pick_item, self.choice_item[i])
        
        #************************* Builds (IDs 4xxx) *************************#
        
        wx.StaticText(self.panel, new_id('t_builds', 'builds', 'text'), "Builds:", (330, 450))
        self.lb_builds = wx.ListBox(self.panel, new_id('lb_builds', 'builds', 'listbox'), (330, 470), (350, 80), [], wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.update_build, self.lb_builds)
        
        button = wx.Button(self.panel, new_id('b_builds_add', 'builds', 'button'), "Add",       (690, 470), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, new_id('b_builds_remove', 'builds', 'button'), "Remove", (690, 500), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        button = wx.Button(self.panel, new_id('b_builds_clear', 'builds', 'button'), "Clear",   (690, 530), button_size['normal'])
        self.Bind(wx.EVT_BUTTON, self.click, button)
        
        #************************* Graphs (IDs 5xxx) *************************#
        
        wx.StaticBox(self.panel, new_id('box_dps', 'graphs', 'frame'), "DPS",                         (5, 320), (325, 50))    
        
        wx.StaticText(self.panel, new_id('t_dps_min', 'graphs', 'text'), "Minimum:",                  (10, 341))
        self.tc_dps_min = wx.TextCtrl(self.panel, new_id('tc_dps_min', 'graphs', 'textcontrol'), "0", (70, 340), (40, 20), style = wx.TE_READONLY)
        
        wx.StaticText(self.panel, new_id('t_dps_avg', 'graphs', 'text'), "Average:",                  (120, 341))
        self.tc_dps_avg = wx.TextCtrl(self.panel, new_id('tc_dps_avg', 'graphs', 'textcontrol'), "0", (170, 340), (40, 20), style = wx.TE_READONLY)
        
        wx.StaticText(self.panel, new_id('t_dps_max', 'graphs', 'text'), "Maximum:",                  (220, 341))
        self.tc_dps_max = wx.TextCtrl(self.panel, new_id('tc_dps_max', 'graphs', 'textcontrol'), "0", (280, 340), (40, 20), style = wx.TE_READONLY)
        
        
        wx.StaticText(self.panel, new_id('t_armor', 'graphs', 'text'), "Armor:",                            (95, 240))
        
        wx.StaticText(self.panel, new_id('t_armor_min', 'graphs', 'text'), "Minimum:",                      (95, 266))
        self.tc_armor_min = wx.TextCtrl(self.panel, new_id('tc_armor_min', 'graphs', 'textcontrol'), "0",   (155, 265), (50, 20))
        self.tc_armor_min.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_armor_min)
        
        wx.StaticText(self.panel, new_id('t_armor_max', 'graphs', 'text'), "Maximum:",                      (95, 291))
        self.tc_armor_max = wx.TextCtrl(self.panel, new_id('tc_armor_max', 'graphs', 'textcontrol'), "300", (155, 290), (50, 20))
        self.tc_armor_max.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_armor_max)
        
        
        wx.StaticText(self.panel, new_id('t_item_option', 'graphs', 'text'), "Calc Option:",                                 (10, 240))
        
        self.radio_calc_dps = wx.RadioButton(self.panel, new_id('radio_calc_dps', 'graphs', 'checkbox'), "DPS",              (10, 265), style = wx.RB_GROUP)
        self.radio_calc_dpsgold = wx.RadioButton(self.panel, new_id('radio_calc_dpsgold', 'graphs', 'checkbox'), "DPS/gold", (10, 290))
        
        
        self.b_graphs = wx.Button(self.panel, new_id('b_graphs', 'graphs', 'button'), "Graph",            (10, 455), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, self.b_graphs)
        
        self.cb_file = wx.CheckBox(self.panel, new_id('cb_file', 'graphs', 'checkbox'), "Save graph to file:",    (10, 500))
        self.tc_file = wx.TextCtrl(self.panel, new_id('tc_file', 'graphs', 'textcontrol'), "graph",               (10, 520), (140, 20))
        self.tc_file.SetMaxLength(20)
        self.tc_file.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_file)
        
        #************************* Optimal Build (IDs 6xxx) *************************#
        
        wx.StaticBox(self.panel, new_id('box_optimal', 'optimal', 'frame'), "Options", (005, 220), (775, 100))
        
        wx.StaticText(self.panel, new_id('t_item_option', 'optimal', 'text'), "Optimal build:",                           (460, 240))
        
        self.radio_item_more = wx.RadioButton(self.panel, new_id('radio_item_more', 'optimal', 'checkbox'), "More items", (460, 265), style = wx.RB_GROUP)
        self.radio_item_fast = wx.RadioButton(self.panel, new_id('radio_item_fast', 'optimal', 'checkbox'), "Faster",     (460, 290))
        
        wx.StaticText(self.panel, new_id('t_budget', 'optimal', 'text'), "Budget:",                              (660, 240))
        
        wx.StaticText(self.panel, new_id('t_budget_min', 'optimal', 'text'), "Minimum:",                         (660, 266))
        self.tc_budget_min = wx.TextCtrl(self.panel, new_id('tc_budget_min', 'optimal', 'textcontrol'), "0",     (720, 265), (50, 20))
        self.tc_budget_min.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_budget_min)
        
        wx.StaticText(self.panel, new_id('t_budget_max', 'optimal', 'text'), "Maximum:",                         (660, 291))
        self.tc_budget_max = wx.TextCtrl(self.panel, new_id('tc_budget_max', 'optimal', 'textcontrol'), "25000", (720, 290), (50, 20))
        self.tc_budget_max.Bind(wx.EVT_CHAR, self.key_press)
        self.Bind(wx.EVT_TEXT, self.text_change, self.tc_budget_max)
        
        wx.StaticText(self.panel, new_id('t_n_items', 'optimal', 'text'), "Number of items:", (550, 240))
        
        self.radio_item_num = []
        for i in xrange(6):
            self.radio_item_num.append(self.create_radio_item(i))
        
        self.b_optimal_build = wx.Button(self.panel, new_id('b_optimal_build', 'optimal', 'button'), "Optimal Build", (340, 327), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, self.b_optimal_build)
        
        self.t_armor_val = wx.StaticText(self.panel, new_id('t_armor_val', 'optimal', 'text'), "Current Armor:", (490, 351))
        self.tc_armor_val = wx.TextCtrl(self.panel, new_id('tc_armor_val', 'optimal', 'textcontrol'), "0",       (575, 350), (40, 20), style = wx.TE_READONLY)

        self.gauge_armor_val = wx.Gauge(self.panel, new_id('gauge_armor_val', 'optimal', 'gauge'), 1000,         (490, 330), (125, 15))
        self.timer_armor_val = wx.Timer(self, new_id('timer_armor_val', 'optimal', 'timer'))
        self.Bind(wx.EVT_TIMER, self.on_timer)
        
        #wx.StaticLine(self.panel, new_id('line_optimal', 'optimal', 'frame'), (622, 325), (2, 60), style=wx.LI_VERTICAL)
        
        #************************* Optimal Build Path (IDs 7xxx) *************************#
        
        wx.StaticLine(self.panel, new_id('line_optimal_path', 'optimal_path', 'frame'), (625, 325), (2, 60), style=wx.LI_VERTICAL)
        
        wx.StaticBox(self.panel, new_id('box_optimal_path', 'optimal_path', 'frame'), "Optimal Build Path", (005, 370), (770, 80))
        
        wx.StaticText(self.panel, new_id('t_slots_option', 'optimal_path', 'text'), "Method:",                                                (15, 385))
        
        self.radio_method_best_dps = wx.RadioButton(self.panel, new_id('radio_method_best_dps', 'optimal_path', 'checkbox'), "Best DPS/item", (15, 405), style = wx.RB_GROUP)
        #self.radio_slots_fast = wx.RadioButton(self.panel, new_id('radio_slots_fast', 'optimal_path', 'checkbox'), "Faster",     (460, 440))
        
        wx.StaticText(self.panel, new_id('t_n_slots', 'optimal_path', 'text'), "Number of Slots:", (120, 385))
        
        self.radio_slots_num = []
        for i in xrange(6):
            self.radio_slots_num.append(self.create_radio_slots(i))
        
        wx.StaticText(self.panel, new_id('t_optimal_path', 'optimal_path', 'text'), "Path:", (220, 385))
        self.tc_optimal_path = wx.TextCtrl(self.panel, new_id('t_optimal_path', 'optimal_path', 'textcontrol'), "", (220, 410), (545, 30), style = wx.TE_READONLY)
        
        self.b_optimal_path = wx.Button(self.panel, new_id('b_optimal_path', 'optimal_path', 'button'), "Optimal Path", (635, 327), button_size['big'])
        self.Bind(wx.EVT_BUTTON, self.click, self.b_optimal_path)
        
        #************************* Defaults *************************#
        self.choice_champ.SetSelection(0)
        self.pick_champ(None)
        self.cb_tier_1.SetValue(0)
        self.cb_tier_2.SetValue(1)
        self.cb_tier_3.SetValue(1)
        self.cb_boost_item.SetValue(1)
        self.cb_boost_champ.SetValue(1)
        self.tier_change(None)
        self.radio_item_num[3].SetValue(1)
        self.radio_item_fast.SetValue(1)
        self.b_graphs.Disable()
        self.update_stats()
        self.b_optimal_path.Disable()
        self.radio_slots_num[5].SetValue(1)
        
    def create_champ_objects (self, i):
        """
        Creates the objects for the various champ stats
        """
        
        name = {0: 'Attack Damage', 1: 'Attack Scaling', 2: 'Attack Speed', 3: 'Speed Scaling', 4: 'Multiplier',
                5: 'Flat Penetration', 6: 'Percent Penetration', 7: 'Critical Chance', 8: 'Critical Damage', 9: 'Type'}
        
        y_base  = 75
        dy      = 30
        tc_size = (45, 20)
        
        if (i < 5):
            txt_pos   = (015, y_base + i*dy)
            tc_ro_pos = (105, y_base + i*dy)
            tc_ex_pos = (155, y_base + i*dy)
            tc_pos    = (205, y_base + i*dy)
        else:
            txt_pos   = (260, y_base + (i-5)*dy)
            tc_ro_pos = (370, y_base + (i-5)*dy)
            tc_ex_pos = (420, y_base + (i-5)*dy)
            tc_pos    = (470, y_base + (i-5)*dy)
        
        if   (i == 0):
            ID['t_stat_champ_1'] = ID_location['champ'] + ID_type['text'] + 15
            wx.StaticText(self.panel, new_id('t_stat_champ_1', 'champ', 'textcontrol'), "Champ", (100, 55))
            ID['t_stat_item_1'] = ID_location['champ'] + ID_type['text'] + 16
            wx.StaticText(self.panel, new_id('t_stat_item_1', 'champ', 'textcontrol'), "Items",  (157, 55))
            ID['t_stat_extra_1'] = ID_location['champ'] + ID_type['text'] + 17
            wx.StaticText(self.panel, new_id('t_stat_extra_1', 'champ', 'textcontrol'), "Extra", (205, 55))
        elif (i == 5):
            ID['t_stat_champ_2'] = ID_location['champ'] + ID_type['text'] + 18
            wx.StaticText(self.panel, new_id('t_stat_champ_2', 'champ', 'textcontrol'), "Champ", (370, 55))
            ID['t_stat_item_2'] = ID_location['champ'] + ID_type['text'] + 19
            wx.StaticText(self.panel, new_id('t_stat_item_2', 'champ', 'textcontrol'), "Items",  (427, 55))
            ID['t_stat_extra_2'] = ID_location['champ'] + ID_type['text'] + 20
            wx.StaticText(self.panel, new_id('t_stat_extra_2', 'champ', 'textcontrol'), "Extra", (475, 55))
        
        id_name = '_champ_' + name[i].lower().replace(' ', '_')

        wx.StaticText(self.panel, new_id('t' + id_name, 'champ', 'textcontrol'), name[i] + ':', txt_pos)
        
        if (i != 9):
            tc_base = wx.TextCtrl(self.panel, new_id('tc' + id_name + '_base', 'champ', 'textcontrol'), "0", tc_ro_pos, tc_size, style = wx.TE_READONLY)
            tc_item = wx.TextCtrl(self.panel, new_id('tc' + id_name + '_item', 'champ', 'textcontrol'), "0", tc_ex_pos, tc_size, style = wx.TE_READONLY)
            tc_extra = wx.TextCtrl(self.panel, new_id('tc' + id_name + '_extra', 'champ', 'textcontrol'), "0", tc_pos, tc_size)
        else: 
            tc_base = wx.TextCtrl(self.panel, new_id('tc' + id_name + '_base', 'champ', 'textcontrol'), "Ranged", tc_ro_pos, (60, 20), style = wx.TE_READONLY)
            tc_item = wx.TextCtrl(self.panel, new_id('tc' + id_name + '_item', 'champ', 'textcontrol'), "0", tc_ex_pos, tc_size, style = wx.TE_READONLY)
            tc_item.Hide()
            tc_extra = wx.TextCtrl(self.panel, new_id('tc' + id_name + '_extra', 'champ', 'textcontrol'), "0", tc_pos, tc_size)
            tc_extra.Hide()
        
        return {'base': tc_base, 'item': tc_item, 'extra': tc_extra}
        
    def create_choice_item (self, i):
        """
        Creates the choices for the 5 items
        """
    
        pos = ((i%2)*125 + 535, (i/2)*30 + 60)
        
        choice_item = wx.Choice(self.panel, new_id('tc_choice_' + str(i), 'items', 'choice'), pos, (110, 25), ["None"])
        choice_item.SetStringSelection("None")
        
        return choice_item
    
    def create_radio_item (self, i):
        """
        Creates the radio items for the number of items
        """
        
        pos = ((i%3)*30 + 550, (i/3)*24 + 266)
        
        if (i == 0):
            style = wx.RB_GROUP
        else:
            style = 0
            
        radio_item = wx.RadioButton(self.panel, new_id('radio_item_num_' + str(i), 'optimal', 'checkbox'), str(i+1), pos, style=style)
        
        return radio_item
    
    def create_radio_slots (self, i):
        """
        Creates the radio items for the number of slots
        """
        
        pos = ((i%3)*30 + 120, (i/3)*20 + 405)
        
        if (i == 0):
            style = wx.RB_GROUP
        else:
            style = 0
            
        radio_item = wx.RadioButton(self.panel, new_id('radio_slots_num_' + str(i), 'optimal_path', 'checkbox'), str(i+1), pos, style=style)
        
        return radio_item
    
    #************************* Event Functions *************************#
        
    def click (self, event):
        """
        Button click redirect
        """
    
        id = event.GetId()
        
        if   (id == ID['b_builds_add']):                            
            self.build_add (event)
        elif (id == ID['b_builds_remove']):                         
            self.build_remove (event)
        elif (id == ID['b_builds_clear']):                          
            self.build_clear (event)
        elif (id == ID['b_graphs']):  
            self.graph (event)           
        elif (id == ID['b_optimal_build']): 
            self.calc_optimal_builds (event)
        elif (id == ID['b_optimal_path']):
            self.calc_optimal_path (event)
    
    def text_change (self, event):
        """
        Text change redirect
        """
        
        id = event.GetId()
        if   (id == ID['tc_champ_level']):
            self.int_validate(self.tc_champ_level, 1, 18)
        elif (id == ID['tc_time']): 
            self.int_validate(self.tc_time, 1, 60)
        elif (id == ID['tc_armor_min']):
            self.int_validate(self.tc_armor_min, 0, 500)
            self.compare_value(self.tc_armor_min, self.tc_armor_max)
        elif (id == ID['tc_armor_max']):
            self.int_validate(self.tc_armor_max, 0, 500)
            self.compare_value(self.tc_armor_min, self.tc_armor_max)
        elif (id == ID['tc_budget_min']):
            self.int_validate(self.tc_budget_min, 0, 25000)
            self.compare_value(self.tc_budget_min, self.tc_budget_max)
        elif (id == ID['tc_budget_max']):
            self.int_validate(self.tc_budget_max, 0, 25000)
            self.compare_value(self.tc_budget_min, self.tc_budget_max)
        
        self.update_stats()
    
    def key_press (self, event):
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
        elif (id in [ID['tc_champ_level'], ID['tc_time'], ID['tc_armor_min'], ID['tc_armor_max'], ID['tc_budget_min'], ID['tc_budget_max']]):                                     
            if ((keycode >= ord('0')) and (keycode <= ord('9'))):
                event.Skip()
        elif (id == ID['tc_file']):
            if (((keycode >= ord('0')) and (keycode <= ord('9'))) or
                ((keycode >= ord('a')) and (keycode <= ord('z'))) or
                ((keycode >= ord('A')) and (keycode <= ord('Z'))) or
                (keycode == ord('_'))):
                event.Skip()
        
    def tier_change (self, event):
        """
        Update items after changing the visible tiers
        """
        
        tiers = {}
        tiers['None']      = 1
        tiers['Basic']     = to_int(self.cb_tier_1.GetValue())
        tiers['Advanced']  = to_int(self.cb_tier_2.GetValue())
        tiers['Legendary'] = to_int(self.cb_tier_3.GetValue())
        
        items     = filter_items_tiers(tiers)
        item_list = get_item_list(items)
        
        for i in xrange(5):
            self.choice_item[i].Clear()
            self.choice_item[i].AppendItems(item_list)
            self.choice_item[i].SetStringSelection("None")
            
    def on_timer (self, event):
        """
        Timer events
        """
    
        id = event.GetId()
        
        if   (id == ID['timer_armor_val']):
            self.tc_armor_val.SetValue('0')
            self.gauge_armor_val.SetValue(0)
            self.timer_armor_val.Stop()
            
    def change_option (self, event):
        """
        Update stats when any DPS option is changed
        """
        
        self.update_stats()

    #************************* Other Functions *************************#            

    def pick_champ (self, event):
        """
        Update stats after changing the champ in choice_champ
        """
        
        champ = get_champ(self.choice_champ.GetStringSelection())
        print "Champion chosen: %s" % (champ.name)
        
        self.update_stats()
        self.tc_champ_stats[9]['base'].SetValue(champ.type)
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
                5: 'flat_penetration', 6: 'percent_penetration', 7: 'critical_chance', 8: 'critical_damage', 9: 'type'}
        
        champ = get_champ(self.choice_champ.GetStringSelection())
        
        extra = {}
        for i in xrange(9):
            extra[stats[i]] = to_float(self.tc_champ_stats[i]['extra'].GetValue())
        extra['level'] = to_int(self.tc_champ_level.GetValue())
        
        items = []
        for choice in self.choice_item:
            item_name = choice.GetStringSelection()
            if (item_name != "None"):
                item = get_item(item_name)
                items.append(item)
        
        time  = to_int(self.tc_time.GetValue())
        armor = {'min': to_int(self.tc_armor_min.GetValue()), 'max': to_int(self.tc_armor_max.GetValue())}
        
        boost = {'item': to_int(self.cb_boost_item.GetValue()), 'champ': to_int(self.cb_boost_champ.GetValue())}
        
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
            
            if (stats[stat] == 'speed') and (value > 2.5):
                value = 2.5
            if (stats[stat] == 'critical_chance') and (value > 1):
                value = 1
            
            self.tc_champ_stats[stat]['item'].SetValue(str(value))
            
        self.tc_dps_min.SetValue(str(to_int(calc_dps(armor['max'], champ, extra, items, time, boost))))
        self.tc_dps_avg.SetValue(str(to_int(calc_dps((armor['max'] + armor['min'])/2, champ, extra, items, time, boost))))
        self.tc_dps_max.SetValue(str(to_int(calc_dps(armor['min'], champ, extra, items, time, boost))))
        
        if (len(items) > 0):
            self.b_optimal_path.Enable()
        else:
            self.b_optimal_path.Disable()
        
    def int_validate (self, tc, min, max):
        """
        Check if the new value is within the limits
        """
        
        text = tc.GetValue()
        int_val = to_int(text)
        
        if   (int_val < min):
            tc.SetValue(str(min))
        elif (int_val > max):
            tc.SetValue(str(max))
        else:
            return True
        
        return False                    
    
    def compare_value (self, tc_min, tc_max):
        """
        Check (and correct) a pair of textcontrols' order
        """
    
        min = to_int(tc_min.GetValue())
        max = to_int(tc_max.GetValue())
        if (min > max):
            temp = min
            min  = max
            max  = temp
            tc_min.SetValue(str(min))
            tc_max.SetValue(str(max))
        
    def build_add (self, event):
        """
        Add a build to the list
        """
        
        if (self.lb_builds.GetCount() < 8):
            build = self.get_build()
            self.lb_builds.Insert(build['name'], self.lb_builds.GetCount(), build['data'])
            print "Build added: %s" % (build['name'])
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
            
        if not (self.b_graphs.IsEnabled()):
            self.b_graphs.Enable()
        
    def build_remove (self, event):
        """
        Remove the build from the list
        """
        
        if (self.lb_builds.GetCount() > 0):
            print "Build removed"   
            self.lb_builds.Delete(self.lb_builds.GetSelection())
            self.lb_builds.SetSelection(self.lb_builds.GetCount() - 1)
        
        if (self.lb_builds.GetCount() == 0):
            self.b_graphs.Disable()
            
    def build_clear (self, event):
        """
        Clear all builds from the list
        """
        
        if (self.lb_builds.GetCount() > 0):
            print "All builds removed"
            self.lb_builds.Clear()
            self.b_graphs.Disable()
        
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
            extra[stats[i]] = to_float(self.tc_champ_stats[i]['extra'].GetValue())
        extra['level'] = to_int(self.tc_champ_level.GetValue())
        
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
        
        time = to_int(self.tc_time.GetValue())
        build_name += "_t=" + str(time)
        
        build = {'champ': champ, 'extra': extra, 'items': items, 'time': time}
        
        return {'name': build_name, 'data': build}
        
    def update_build (self, event):
        build = self.lb_builds.GetClientData(self.lb_builds.GetSelection())
        
        self.choice_champ.SetStringSelection(build['champ'].name)
        
        stats = {0: 'attack', 1: 'attack_scaling', 2: 'speed', 3: 'speed_scaling', 4: 'multiplier',
                5: 'flat_penetration', 6: 'percent_penetration', 7: 'critical_chance', 8: 'critical_damage'}
        
        for i in xrange(9):
            self.tc_champ_stats[i]['extra'].SetValue(str(build['extra'][stats[i]]))
        self.tc_champ_level.SetValue(str(build['extra']['level']))
        
        n = 0
        for item in build['items']:
            self.choice_item[n].SetStringSelection(item.name)
            n += 1
            
        self.tc_time.SetValue(str(build['time']))
    
    def graph (self, event):
        """
        Graph the builds
        """
        
        lb = self.lb_builds
        n  = lb.GetCount()
        
        if   (self.radio_calc_dps.GetValue() == 1):
            type = 'dps'
        elif (self.radio_calc_dpsgold.GetValue() == 1):
            type = 'dpsgold'
        
        armor = {'min': to_int(self.tc_armor_min.GetValue()), 'max': to_int(self.tc_armor_max.GetValue())}
        
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

        boost = {'item': to_int(self.cb_boost_item.GetValue()), 'champ': to_int(self.cb_boost_champ.GetValue())}
            
        if (type == 'dpsgold'):
            for i in xrange(n):
                if (builds[i]['items'] == []):
                    message = wx.MessageBox('Impossible to graph DPS/gold with no items.', 'Error', wx.OK | wx.ICON_ERROR)
                    return None
        
        make_graph (type, armor, builds, boost, file)
        
    def calc_optimal_builds (self, event):
        """
        Calculate the optimal build for each armor in the range of armors
        """
        
        if   (self.radio_calc_dps.GetValue() == 1):
            type = 'dps'
        elif (self.radio_calc_dpsgold.GetValue() == 1):
            type = 'dpsgold'
        
        boost = {'item': to_int(self.cb_boost_item.GetValue()), 'champ': to_int(self.cb_boost_champ.GetValue())}
        
        tiers = {}
        tiers['None']      = 0
        tiers['Basic']     = to_int(self.cb_tier_1.GetValue())
        tiers['Advanced']  = to_int(self.cb_tier_2.GetValue())
        tiers['Legendary'] = to_int(self.cb_tier_3.GetValue())
        
        armor_range = {'min': to_int(self.tc_armor_min.GetValue()),  'max': to_int(self.tc_armor_max.GetValue())}
        step_size   = self.gauge_armor_val.GetRange() / (armor_range['max'] - armor_range['min'])
        price_range = {'min': to_int(self.tc_budget_min.GetValue()), 'max': to_int(self.tc_budget_max.GetValue())}
        
        for i in xrange(len(self.radio_item_num)):
            if (self.radio_item_num[i].GetValue()):
                n_items = i+1
        
        build        = self.get_build()['data']
        champ        = build['champ']
        preset_items = build['items']
        extra        = build['extra']
        time         = build['time']
        
        n_items -= len(preset_items)
        if (n_items < 1):
            message = wx.MessageBox('Number of chosen items is equal or larger than the number of items to calculate.', 'Error', wx.OK | wx.ICON_ERROR)
            return None
        
        self.b_optimal_build.Disable()
        
        if   (self.radio_item_more.GetValue() == 1):
            item_opt = 'more'
        elif (self.radio_item_fast.GetValue() == 1):
            item_opt = 'fast'
        
        all_labels = []
        builds     = []
        
        n = 0
        self.lb_builds.Clear()
        self.gauge_armor_val.SetValue(0)
        for armor in xrange(armor_range['min'], armor_range['max'], 1):
            wx.Yield()
            self.tc_armor_val.SetValue(str(armor))
            old_pos = self.gauge_armor_val.GetValue()
            self.gauge_armor_val.SetValue(old_pos + step_size)
            
            optimal_items = optimal_build(armor, champ, extra, preset_items, time, boost, item_opt, n_items, tiers, price_range)
            
            new_label = get_label(champ, extra['level'], optimal_items, time)
            
            if not (new_label in all_labels):
                build = {'champ': champ, 'extra': extra, 'items': optimal_items, 'time': time}
                builds.append(build)
                self.lb_builds.Insert(new_label, n, build)
                all_labels.append(new_label)
                n += 1
                if (n > 8): break
        
        print "Optimal build(s) of %i item(s) calculated." % (n_items)
        
        self.b_graphs.Enable()
        self.b_optimal_build.Enable()
        self.gauge_armor_val.SetValue(self.gauge_armor_val.GetRange())
        self.timer_armor_val.Start(1500)
    
    def calc_optimal_path (self, event):
        """
        Calculate the optimal build path for the build
        """
        
        boost = {'item': to_int(self.cb_boost_item.GetValue()), 'champ': to_int(self.cb_boost_champ.GetValue())}
        
        armor_range = {'min': to_int(self.tc_armor_min.GetValue()),  'max': to_int(self.tc_armor_max.GetValue())}
        armor = (armor_range['min']+armor_range['max'])/2
        
        for i in xrange(len(self.radio_slots_num)):
            if (self.radio_slots_num[i].GetValue()):
                n_slots = i+1
        
        build = self.get_build()['data']
        champ = build['champ']
        items = build['items']
        extra = build['extra']
        time  = build['time']
        
        if (n_slots < len(items)):
            message = wx.MessageBox('Number of chosen items is larger than the number of slots.', 'Error', wx.OK | wx.ICON_ERROR)
            return None
        
        if (self.radio_method_best_dps.GetValue() == 1):
            optimal_path = optimal_path_best_dps(armor, champ, extra, items, time, boost, n_slots)
            method = self.radio_method_best_dps.GetLabel()
        
        optimal_path_text = ""
        i = 0
        for item in optimal_path:
            if (i != 0):
                optimal_path_text += " -> "
            optimal_path_text += item.name
            i += 1
        
        self.tc_optimal_path.SetValue(optimal_path_text)
        
        items_list = ""
        i = 0
        for item in items:
            if (i != 0):
                items_list += ", "
            items_list += item.name
            i += 1
        
        print "Optimal path calculated for (%s) using method %s" % (items_list, method)
        
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