#!/usr/bin/python

import wx
import wx.grid
import glob
import re
import math
import codecs
import operator
import os
import Image

from itertools import groupby
from operator import itemgetter 

## home directory
#home_dir = "/home/tmos/Desktop/polinet_front_end/front_end_v0.2"
home_dir = "D:\Documents\metaptuxiako\master_codes_more\polinet_front_end\front_end_v0.2"

## column and row labels
colLabels = ["Actor 1", "Actor 2", "Metric", "Rating", "Year"]
rowLabels = []

## scores to be displayed in grid
data = []
for i in xrange(1):
	data.append(["","","","",""])

#######################################
## gridTable definitions
#######################################
class GenericTable(wx.grid.PyGridTableBase):
	def __init__(self, data, rowLabels, colLabels):
		wx.grid.PyGridTableBase.__init__(self)
		self.data = data
		self.rowLabels = rowLabels
		self.colLabels = colLabels
        
	def GetNumberRows(self):
		return len(self.data)

	def GetNumberCols(self):
		return len(self.data[0])

	def GetColLabelValue(self, col):
		if self.colLabels:
			return self.colLabels[col]
        
	def GetRowLabelValue(self, row):
		if self.rowLabels:
			return self.rowLabels[row]
        
	def IsEmptyCell(self, row, col):
		return False

	def GetValue(self, row, col):
		return self.data[row][col]

	def SetValue(self, row, col, value):
		pass

	def AddRow(self, row):
		self.data.append(row)
		self.rowLabels.append(self.GetNumberRows())

		msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_APPENDED,1)  
		self.GetView().ProcessTableMessage(msg)

	def RemoveAllRows(self):

		tmp_num_rows = self.GetNumberRows()

		del self.data[:]

		msg = wx.grid.GridTableMessage(self, wx.grid.GRIDTABLE_NOTIFY_ROWS_DELETED,1,tmp_num_rows)  
		self.GetView().ProcessTableMessage(msg)

#######################################
## grid class
#######################################
class SimpleGrid(wx.grid.Grid):
	def __init__(self, parent):
		wx.grid.Grid.__init__(self, parent, -1, style=wx.RAISED_BORDER)
		self.tableBase = GenericTable(data, rowLabels, colLabels)
		self.SetTable(self.tableBase)  



#######################################
## class for add more actors frame
#######################################
class add_actors_frame(wx.Frame):

	def __init__(self, *args, **kwds):
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)

		self.label_actor1 = wx.StaticText(self, -1, "Actor1",style=wx.ALIGN_CENTRE)
		self.label_actor1.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.actor1_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor1_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.label_actor2 = wx.StaticText(self, -1, "Actor2",style=wx.ALIGN_CENTRE)
		self.label_actor2.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.actor2_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor2_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.label_actor3 = wx.StaticText(self, -1, "Actor3",style=wx.ALIGN_CENTRE)
		self.label_actor3.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.actor3_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor3_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.label_actor4 = wx.StaticText(self, -1, "Actor4",style=wx.ALIGN_CENTRE)
		self.label_actor4.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.actor4_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor4_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.label_actor5 = wx.StaticText(self, -1, "Actor5",style=wx.ALIGN_CENTRE)
		self.label_actor5.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.actor5_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor5_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.label_actor6 = wx.StaticText(self, -1, "Actor6",style=wx.ALIGN_CENTRE)
		self.label_actor6.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.actor6_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor6_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.button_load_actors = wx.Button(self, id=-1, label='Create file', pos=(8, 8), size=(175, 28))
		self.button_load_actors.Bind(wx.EVT_BUTTON, self.on_read_actors)
		self.button_load_actors.SetToolTip(wx.ToolTip("Click to save the selected actors"))

		self.button_close = wx.Button(self, id=-1, label='Close', pos=(8, 8), size=(175, 28))
		self.Bind(wx.EVT_BUTTON, self.OnCloseWindow)

		self.__do_layout()

	def __do_layout(self):

		sizer_main = wx.BoxSizer(wx.VERTICAL)

		sizer_actor1 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor1.Add(self.label_actor1, 0, wx.ALIGN_LEFT, 5)
		sizer_actor1.Add(self.actor1_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
		
		sizer_actor2 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor2.Add(self.label_actor2, 0, wx.ALIGN_LEFT, 5)
		sizer_actor2.Add(self.actor2_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		sizer_actor3 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor3.Add(self.label_actor3, 0, wx.ALIGN_LEFT, 5)
		sizer_actor3.Add(self.actor3_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		sizer_actor4 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor4.Add(self.label_actor4, 0, wx.ALIGN_LEFT, 5)
		sizer_actor4.Add(self.actor4_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		sizer_actor5 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor5.Add(self.label_actor5, 0, wx.ALIGN_LEFT, 5)
		sizer_actor5.Add(self.actor5_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		sizer_actor6 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor6.Add(self.label_actor6, 0, wx.ALIGN_LEFT, 5)
		sizer_actor6.Add(self.actor6_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)
		sizer_buttons.Add(self.button_load_actors, 0, wx.ALIGN_CENTRE, 5)
		sizer_buttons.Add(self.button_close, 0, wx.ALIGN_CENTRE, 5)

		sizer_main.Add(sizer_actor1, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
		sizer_main.Add(sizer_actor2, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
		sizer_main.Add(sizer_actor3, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
		sizer_main.Add(sizer_actor4, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)		
		sizer_main.Add(sizer_actor5, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
		sizer_main.Add(sizer_actor6, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
		sizer_main.Add(sizer_buttons, 0, wx.ALIGN_CENTRE, 5 )

		self.SetSizer(sizer_main)
		self.Layout()

	def on_read_actors(self, event):
		
		## input for actors
		actor1 = self.actor1_input.GetValue().encode('utf-8')
		actor2 = self.actor2_input.GetValue().encode('utf-8')
		actor3 = self.actor3_input.GetValue().encode('utf-8')
		actor4 = self.actor4_input.GetValue().encode('utf-8')
		actor5 = self.actor5_input.GetValue().encode('utf-8')
		actor6 = self.actor6_input.GetValue().encode('utf-8')

		## store the given actors in an array
		actors_mat = [actor1, actor2, actor3, actor4, actor5, actor6]
		
		dlg = wx.FileDialog(self, message="Save file with actor names", defaultDir=os.getcwd(), defaultFile="", style=wx.SAVE)

		if dlg.ShowModal() == wx.ID_OK:
			actorsfile_input = dlg.GetPath()

		## opens file to store the actors
		FILE = open(actorsfile_input, "w")

		## for each actor in the array
		for actor in actors_mat:
			if not(actor == ''):
				print >> FILE, actor
		FILE.close()

	def OnCloseWindow(self, event):
        	self.Close(True)

#######################################
## frame class definitions
#######################################
class MyFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)

		## parameters
		self.simtype = "" 
		self.similarity = "" 
		self.language = ""
		self.all_web_docs = 10000000000
		self.networkfile = ""

		## dictionary with the queries and counts
		self.diction_queries = {}
		self.diction_actors = {}
		self.diction_labels = {}

		## static lines
		self.static_line_0 = wx.StaticLine(self, -1)
		self.static_line_2 = wx.StaticLine(self, -1)
		self.static_line_3 = wx.StaticLine(self, -1)
		self.static_line_4 = wx.StaticLine(self, -1)

		## lists of options
		self.lang_options = ['English', 'Greek']
		self.sim_options = ['page_count:JAC','page_count:DICE', 'page_count:MI', 'page_count:NGD']		
		self.year_options = ['None','1994','1995','1996','1997','1998','1999','2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015']

		## similarity choices
		self.sim_choice = wx.Choice(self, -1, choices=self.sim_options)
		self.sim_choice.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## language choice
		self.lang_choice = wx.Choice(self, -1, choices=self.lang_options)
		self.lang_choice.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## year choice
		self.year_choice = wx.Choice(self, -1, choices=self.year_options)
		self.year_choice.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## title label
		self.label_title = wx.StaticText(self, -1, '''Policy Network Extraction demo''', style=wx.ALIGN_CENTRE)
		self.label_title.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0))

		## similarity choice label
		self.label_sim = wx.StaticText(self, -1, "Similarity",style=wx.ALIGN_CENTRE)
		self.label_sim.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## language choice label
		self.label_lang = wx.StaticText(self, -1, "Language",style=wx.ALIGN_CENTRE)
		self.label_lang.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## year choice label
		self.label_year = wx.StaticText(self, -1, "Year",style=wx.ALIGN_CENTRE)
		self.label_year.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## actor input labels
		self.label_actor1=wx.StaticText(self, 0, '''Actor 1''', style=wx.ALIGN_CENTRE)
		self.label_actor1.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.label_actor2=wx.StaticText(self, 0, '''Actor 2''', style=wx.ALIGN_CENTRE)
		self.label_actor2.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## actor input boxes
		self.actor1_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor1_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		self.actor2_input = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_PROCESS_TAB)
		self.actor2_input.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## button to insert more actors
		self.button_more_actors = wx.Button(self, id=-1, label='More actors', pos=(8, 8), size=(175, 28))
		self.button_more_actors.Bind(wx.EVT_BUTTON, self.on_more_actors)
		self.button_more_actors.SetToolTip(wx.ToolTip("Click to add more actors"))

		## create button for relatedness
		self.button_rel = wx.Button(self, id=-1, label='Compute relatedness', pos=(8, 8), size=(175, 28))
		self.button_rel.Bind(wx.EVT_BUTTON, self.on_compute_relatedness)
		self.button_rel.SetToolTip(wx.ToolTip("Click to compute strength of relation"))

		## create button to clear matrix
		self.button_clear_mat = wx.Button(self, id=-1, label='Clear table', pos=(8, 8), size=(175, 28))
		self.button_clear_mat.Bind(wx.EVT_BUTTON, self.on_clear_mat)
		self.button_clear_mat.SetToolTip(wx.ToolTip("Click to clear table with relatedness scores"))

		self.button_load_actors = wx.Button(self, id=-1, label='Load actors', pos=(8, 8), size=(175, 28))
		self.button_load_actors.Bind(wx.EVT_BUTTON, self.on_load_actors)
		self.button_load_actors.SetToolTip(wx.ToolTip("Click to load filename with actors"))

		self.button_load_net = wx.Button(self, id=-1, label='Load network', pos=(8, 8), size=(175, 28))
		self.button_load_net.Bind(wx.EVT_BUTTON, self.on_load_net)
		self.button_load_net.SetToolTip(wx.ToolTip("Click to load file of network"))

		## create button to create graph
		self.button_graph = wx.Button(self, id=-1, label='Create graph', pos=(8, 8), size=(175, 28))
		self.button_graph.Bind(wx.EVT_BUTTON, self.on_create_graph)
		self.button_graph.SetToolTip(wx.ToolTip("Click to visualize network as graph"))

		## create button to extract network
		self.button_exct_net = wx.Button(self, id=-1, label='Extract network', pos=(8, 8), size=(175, 28))
		self.button_exct_net.Bind(wx.EVT_BUTTON, self.on_exct_net)
		self.button_exct_net.SetToolTip(wx.ToolTip("Click to extract the selected network"))

		## on selection of parameters
		self.sim_choice.Bind(wx.EVT_CHOICE,self.onSelect_sim)
		self.lang_choice.Bind(wx.EVT_CHOICE,self.onSelect_lang)
		self.year_choice.Bind(wx.EVT_CHOICE,self.onSelect_year)

		## box for gridtable
		self.grid = SimpleGrid(self)

		## error messages box
		self.msg_box = wx.TextCtrl(self, -1, "",style=wx.TE_LEFT|wx.TE_LINEWRAP|wx.TE_READONLY)
		self.msg_box.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0))

		## fix geometry of the whole interface
		self.__do_layout()
	
	def __do_layout(self):
		## main sizer
		sizer_main = wx.BoxSizer(wx.VERTICAL)

		sizer_actor1 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor1.Add(self.label_actor1, 0, wx.ALIGN_LEFT, 5)
		sizer_actor1.Add(self.actor1_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)
		
		sizer_actor2 = wx.BoxSizer(wx.VERTICAL)
		sizer_actor2.Add(self.label_actor2, 0, wx.ALIGN_LEFT, 5)
		sizer_actor2.Add(self.actor2_input, 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		sizer_more_actors = wx.BoxSizer(wx.HORIZONTAL)
		sizer_more_actors.Add(self.button_more_actors, 0, wx.ALIGN_CENTRE, 5)

		sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_10.Add(self.button_load_actors, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_10.Add(self.button_load_net, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_10.Add(self.button_rel, 0, wx.ALIGN_CENTRE_VERTICAL, 5) 

		sizer_sim = wx.BoxSizer(wx.HORIZONTAL)
		sizer_sim.Add(self.label_sim, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_sim.Add(self.sim_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		sizer_lang = wx.BoxSizer(wx.HORIZONTAL)
		sizer_lang.Add(self.label_lang, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_lang.Add(self.lang_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		sizer_year = wx.BoxSizer(wx.HORIZONTAL)
		sizer_year.Add(self.label_year, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_year.Add(self.year_choice, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)

		sizer_prop = wx.BoxSizer(wx.HORIZONTAL)
		sizer_prop.Add(sizer_sim,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
		sizer_prop.Add(sizer_lang,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)		
		sizer_prop.Add(sizer_year,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)		

		## add table
		sizer_12 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_12.Add(self.grid, 1,  wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		sizer_bottom_buttons = wx.BoxSizer(wx.HORIZONTAL)
		sizer_bottom_buttons.Add(self.button_clear_mat, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		sizer_bottom_buttons.Add(self.button_exct_net, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL)
		sizer_bottom_buttons.Add(self.button_graph, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL)

		## add error box
		sizer_msg_box = wx.BoxSizer(wx.HORIZONTAL)
		sizer_msg_box.Add(self.msg_box, 1,  wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 5)

		## add to main sizer
		sizer_main.Add(self.label_title, 0, wx.ALIGN_CENTRE, 5)
		sizer_main.Add(self.static_line_0, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
		sizer_main.Add(sizer_actor1,0,wx.EXPAND, 5)
		sizer_main.Add(sizer_actor2,0,wx.EXPAND, 5)
		sizer_main.Add(sizer_more_actors,0,wx.ALIGN_CENTRE, 5)
		sizer_main.Add(self.static_line_2, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
		sizer_main.Add(sizer_prop, 2, wx.ALIGN_CENTRE, 0)
		sizer_main.Add(self.static_line_3, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
		sizer_main.Add(sizer_10, 0, wx.ALIGN_CENTRE, 0)
		sizer_main.Add(self.static_line_4, 0, wx.TOP|wx.BOTTOM|wx.EXPAND, 5)
		sizer_main.Add(sizer_12, 8, wx.EXPAND, 0)
		sizer_main.Add(sizer_bottom_buttons, 0, wx.ALIGN_CENTRE, 5)		
		sizer_main.Add(sizer_msg_box, 0, wx.EXPAND, 0)		

		self.SetSizer(sizer_main)
		self.Layout()

		self.grid.tableBase.RemoveAllRows()
		self.RefreshFilters()

	## for the computation the actor1-actor2 relatedness
	def on_compute_relatedness(self,event):
		
		## read actor name given as input
		actor1 = self.actor1_input.GetValue().encode('utf-8')
		actor2 = self.actor2_input.GetValue().encode('utf-8')

		self.Compute_relatedness(actor1, actor2, 1)
		
		self.button_rel.Show()
		self.RefreshFilters()

	def on_exct_net(self, event):

		self.diction_rel = {}

		self.msg_box.SetValue('Computing relatedness scores, please wait ... ')

		## compute relatedness for each relation
		for a1 in range(0, len(self.diction_actors)):
			for a2 in range(a1+1, len(self.diction_actors)):
				rel_score = self.Compute_relatedness(self.diction_actors[str(a1)], self.diction_actors[str(a2)], 0)
				rel_key = str(a1)+'_'+str(a2)
				self.diction_rel[rel_key] = rel_score

		## sort dictionary with the relations
		self.diction_rel_sorted = self.sortedDictValues(self.diction_rel)

		dlg = wx.FileDialog(self, message="Save file with actor names", defaultDir=os.getcwd(), defaultFile="", style=wx.SAVE)

		if dlg.ShowModal() == wx.ID_OK:
			self.networkfile = dlg.GetPath()

		self.map_values(self.diction_rel_sorted, self.networkfile)

		self.msg_box.SetValue('Computation of the relatedness has finished successfully!!')

	## select and read file with actors
	def on_load_actors(self,event):

		dlg = wx.FileDialog(self, message="Open file with actor names", defaultDir=os.getcwd(), defaultFile="", style=wx.OPEN)

		if dlg.ShowModal() == wx.ID_OK:
			self.actorsfile = dlg.GetPath()
			
		self.diction_queries = {}
		self.ReadActorFile(self.actorsfile)

		
	def on_load_net(self,event):
		dlg = wx.FileDialog(self, message="Open file with network", defaultDir=os.getcwd(), defaultFile="", style=wx.OPEN)

		if dlg.ShowModal() == wx.ID_OK:
			self.networkfile = dlg.GetPath()

		self.ReadNetwork(self.networkfile)

	## on select language
	def onSelect_lang(self, event):
		self.diction_queries = {}
		self.RefreshFilters()

	## on select similarity type
	def onSelect_sim(self, event):
		self.RefreshFilters()

	## on select year
	def onSelect_year(self, event):
		self.diction_queries = {}
		self.RefreshFilters()

	## on clear table
	def on_clear_mat(self, event):
		## remove all rows from table
		self.grid.tableBase.RemoveAllRows()
		self.msg_box.SetValue('Table with relations and scores cleared successfully!!')
		self.RefreshFilters()

	def on_more_actors(self, event):
		
		add_actors = add_actors_frame(None, -1, "Actors", pos=(300,150), size=(400,450))
		add_actors.Show()

	## create IND query
	def CreateQueries(self, actor1, actor2):
	
		IND_quer_1 = re.sub(r'\s*,\s*','_OR_',actor1)
		IND_quer_1 = re.sub(r' ','_',IND_quer_1)

		IND_quer_2 = re.sub(r'\s*,\s*','_OR_',actor2)
		IND_quer_2 = re.sub(r' ','_',IND_quer_2)

		## create AND query
		AND_quer = IND_quer_1+"_AND_"+IND_quer_2

		return [AND_quer, IND_quer_1, IND_quer_2] 


	## read file with actors to create the network
	def ReadActorFile(self, actorsfile):

		self.diction_actors = {}

		for line in open(actorsfile, "r"):
	
			words = line.rstrip().split(";")	

			self.diction_actors[words[0]] = words[2]
			self.diction_labels[words[0]] = words[1]
		
		self.msg_box.SetValue('File: '+actorsfile+' has been loaded successfully!!')


	## read network in net format
	def ReadNetwork(self, networkfile):

		netdata = []

		data_flag = 0
		label_flag = 0

		for line in open(networkfile,"r"):

			if( re.match('labels\:', line) ):
				label_flag = 1
				continue

			if(label_flag == 1):
				labels = line.rstrip().split(',')
				
				for l in range(0,len(labels)):
					self.diction_labels[l] = labels[l]
				label_flag = 0

			if( re.match('data\:', line)):
				data_flag = 1 
				continue
		
			if data_flag == 1:
				rel_weights = line.rstrip().split(' ')	
				netdata.append(rel_weights)

		for i in range(0, len(labels)):
			for j in range(i+1, len(labels)):
				actor1 = self.diction_labels[i]
				actor2 = self.diction_labels[j]

				if not(netdata[i][j] == '0'):
					rel_score = float(netdata[i][j])
					self.grid.tableBase.AddRow([actor1, actor2, 'None', round(rel_score,2), 'None'])

	## use the search engine to retrieve page-counts
	def Compute_relatedness(self, actor1, actor2, flag):

		[AND_quer, IND_quer_1, IND_quer_2] = self.CreateQueries(actor1, actor2)

		## call perl script to find IND and AND counts
		if not(IND_quer_1 in self.diction_queries):
			counts_IND_1_str = os.popen("perl find_page_count.pl "+IND_quer_1+" "+self.language+" "+self.year,"r").read().rstrip()
			self.diction_queries[IND_quer_1] = counts_IND_1_str
		else:
			counts_IND_1_str = self.diction_queries[IND_quer_1]

		if not(IND_quer_2 in self.diction_queries):
			counts_IND_2_str = os.popen("perl find_page_count.pl "+IND_quer_2+" "+self.language+" "+self.year,"r").read().rstrip()
			self.diction_queries[IND_quer_2] = counts_IND_2_str
		else:
			counts_IND_2_str = self.diction_queries[IND_quer_2]

		if not(AND_quer in self.diction_queries):
			counts_AND_str = os.popen("perl find_page_count.pl "+AND_quer+" "+self.language+" "+self.year,"r").read().rstrip()
			self.diction_queries[AND_quer] = counts_AND_str
		else:
			counts_AND_str =  self.diction_queries[AND_quer]

		counts_AND = float(counts_AND_str)
		counts_IND_1 = float(counts_IND_1_str)
		counts_IND_2 = float(counts_IND_2_str)

		## compute selected similarity
		if self.similarity == "JAC":
			rel_score = counts_AND / (counts_IND_1 + counts_IND_2 - counts_AND)

		elif self.similarity == "DICE":
			rel_score = 2*counts_AND/(counts_IND_1 + counts_IND_2)			

		elif self.similarity == "MI":
			if counts_AND > 0:
				rel_score = math.log( (counts_AND/self.all_web_docs)/((counts_IND_1/self.all_web_docs)*(counts_IND_2/self.all_web_docs)) )
			else:
				rel_score = 0
		else:
			counts = [counts_IND_1, counts_IND_2]
			tmp_score = ( math.log(max(counts) + 1) - math.log(counts_AND + 1) ) / (math.log(self.all_web_docs) - math.log(min(counts) + 1) )

			rel_score = math.exp(-2*tmp_score)
		
		## add computed relatedness score in table
		if flag == 1:
			self.grid.tableBase.AddRow([actor1, actor2, self.similarity, round(rel_score,5), self.year])

		return rel_score

	## def map values 
	def map_values(self, rel_scores, net_file):


		## write the ratings in file
		FILE_MAT = open(net_file,"w")
		actors_num = str(len(self.diction_actors) + 1)

		print >> FILE_MAT,"dl n="+actors_num
		print >> FILE_MAT,"format = fullmatrix"
		print >> FILE_MAT,"labels:"

		labels = []
		for i in range(0,len(self.diction_labels)):
			labels.append(self.diction_labels[str(i)])

		toprint = str(labels)
		toprint = re.sub(r'[\[\]\']','',toprint)
		print >> FILE_MAT, toprint

		## map values in [1,3] using min-max normalization
		rel_scores_vect = []
		for i in range(0, len(rel_scores)):
			rel_scores_vect.append([])

		rel_scores_mat = []
		for i in range(0, len(self.diction_actors)):
			nline = []
			for j in range(0, len(self.diction_actors)):
				nline.append([])
			rel_scores_mat.append(nline)

		for i in range(0, len(self.diction_actors)):
			for j in range(0, len(self.diction_actors)):
				rel_scores_mat[i][j] = 0


		rel_scores.sort(key=itemgetter(1), reverse=False)
		min_val = list(groupby(rel_scores, key=itemgetter(1)).next()[1])

		rel_scores.sort(key=itemgetter(1), reverse=True)
		max_val = list(groupby(rel_scores, key=itemgetter(1)).next()[1])

		## print mapped scores (they are sorted)
		for k in range(0, len(rel_scores)):

			if not(rel_scores[k][1] == 0):
				## apply the min-max normalization
				rel_scores_vect[k] = (2*(rel_scores[k][1] - min_val[0][1])/( max_val[0][1] - min_val[0][1] ) ) + 1			

				rel_score_mapped = rel_scores_vect[k] 

				a1_a2 = rel_scores[k][0].split('_')

				actor1 = self.diction_actors[a1_a2[0]]
				actor2 = self.diction_actors[a1_a2[1]]

				rel_scores_mat[int(a1_a2[0])][int(a1_a2[1])] = round(rel_score_mapped,2)
				rel_scores_mat[int(a1_a2[1])][int(a1_a2[0])] = round(rel_score_mapped,2)

				## add the mapped value in table
				self.grid.tableBase.AddRow([actor1, actor2, self.similarity, round(rel_score_mapped,2) , self.year])
		
		print >> FILE_MAT,"data:"
		## print matrix in file in square format
		for i in range(0, len(self.diction_actors)):
			toprint = str(rel_scores_mat[i])
			print >> FILE_MAT, re.sub(r'[\[\,\]]','',toprint)

		FILE_MAT.close()
		
		rel_scores_vect.sort()

		## fix thresholds for visualization
		FILE_THRES = open("thres_file.txt","w")
		
		for t in range(1,5):
			print >> FILE_THRES, str(round(rel_scores_vect[int(t*math.floor(len(rel_scores)/5)-1)],2))
			
		FILE_THRES.close()

	## to create graph and visualize
	def on_create_graph(self, event):
		
		graph_image = os.popen("perl create_graph.pl "+self.networkfile+" black "+" 0 "+" thres_file.txt").read().rstrip()
		Image.open(graph_image).show()

	## sort dict in values
	def sortedDictValues(self, adict):

		sorted_dict = sorted(adict.iteritems(), key=operator.itemgetter(1))
		return sorted_dict


	## reset parameters
	def RefreshFilters(self):

		tmp_sim = self.sim_options[self.sim_choice.GetSelection()]
		tmp_simtype_sim = tmp_sim.split(':')

		self.simtype = tmp_simtype_sim[0]
		self.similarity = tmp_simtype_sim[1]

		tmp_lang = self.lang_options[self.lang_choice.GetSelection()]

		if tmp_lang == "Greek":
			self.language = "el"
		else: 
			self.language = "en"

		self.year = self.year_options[self.year_choice.GetSelection()]


## Main
if __name__ == "__main__":
	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	frame_1 = MyFrame(None, -1, "Polinet", pos=(300,150), size=(700,500))
	app.SetTopWindow(frame_1)
	frame_1.Show()
	app.MainLoop()

