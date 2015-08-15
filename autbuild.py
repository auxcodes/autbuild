# GNU GENERAL PUBLIC LICENSE
#
# Copyright (C) 2015 remoteaut - Phill Banks - https://github.com/Phill-B/remoteaut
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
from Tkinter import *
import ttk
import tkFileDialog
import tkMessageBox
import subprocess
import os
import re
import webbrowser # used for opening AUT file after it is created


class Application(Frame):
    def createWidgets(self):   
## Set Variables
    #MQSC Variables
        self.qexpr = StringVar()
        self.qexpr.set(r"(QALIAS|QREMOTE|QLOCAL)(.+?)\(\'(.+?)\'\)")
        self.chlexpr = StringVar()
        self.chlexpr.set(r"CHANNEL(.+?)\(\'(.+?)\'\)")
        self.qlist = []
        self.chlist = []
        self.mqsc = StringVar()
        self.mqsc.set('C:/directory/path/to/the/MQSC/script/QMGRNAME.MQSC')
        self.mqscname = StringVar()         # MQSC file location var
        self.mqscname.set('QMGRNAME.MQSC')

        self.grpexpr = StringVar()

    #AUT Variables
        self.objTypeVar = StringVar() ##channel or queue
        self.aut_str = []
        self.grplist = []
        # check button variables
        self.mqmcb = StringVar()
        self.mqmcb.set('mqm')
        self.mqbrkrscb = StringVar()
        self.mqbrkrscb.set('off')
        self.mqxplrcb = StringVar()
        self.mqxplrcb.set('mqxplr')
        self.clstaffcb = StringVar()
        self.clstaffcb.set('clstaff')
        self.wascb = StringVar()
        self.wascb.set('off')
        self.was6cb = StringVar()
        self.was6cb.set('off')
        # checkbutton list
        self.chkbtnlist = [self.mqmcb, self.mqbrkrscb, self.mqxplrcb,
                           self.clstaffcb, self.wascb, self.was6cb]
        self.queueauth = []

        self.mqobjVar = StringVar()                           
        self.qmgr = StringVar()
        self.qmgr.set('QMGRNAME')
        self.qmgr.trace("w", self.on_qmgr_trace)
    #
        self.output = StringVar()       # output file var
        self.output.set('C:/directory/path/to/where/AUT/file/should/go/')
        self.outputfile = StringVar()   # output file name string
        self.outputfile.set('QMGRNAME.AUT') # set output file name
        self.state = BooleanVar()       # State variable to indicate the application has just been opened
        self.cmdaut = StringVar()      # MQSC command string
        self.cmdaut.set(" setmqaut -m QMGR -n 'NAME.OF.THE.QUEUE.OR.CHANNEL' -t queue -g mqm +browse +chg +clr +dlt +dsp +get +inq +put +passall +passid +set +setall +setid ")


        
### Create a frame inside the window for all widgets to be added to
        self.mainFrame = ttk.Frame(self)
        self.mainFrame.grid(row=0, column= 0, sticky='NSWE',
                                padx=5, pady=5, ipadx=5, ipady=5)
        self.mainFrame.columnconfigure(0, weight=1)
        self.mainFrame.rowconfigure(3, weight=1) # allows listbox labelFrame to resize inside mainFrame

## Add MQSC Label Frame
    # MQSC Label Frame
        self.mqscLabelFrame = ttk.LabelFrame(self.mainFrame)
        self.mqscLabelFrame["text"] = "MQSC File Location"
        self.mqscLabelFrame.grid(row=1, column= 0, sticky=(N, E, W),
                                padx=5, pady=5, ipadx=5, ipady=5)
        self.mqscLabelFrame.columnconfigure(2, weight=1)
        
    # MQSC Label Widgets        
        # Script Label            
        self.mqscLabel = ttk.Label(self.mqscLabelFrame)
        self.mqscLabel["text"] = "MQSC Script:"
        self.mqscLabel.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        # output authority Label            
        self.outputLabel = ttk.Label(self.mqscLabelFrame)
        self.outputLabel["text"] = "Queue Manager:"
        self.outputLabel.grid(row=1, column=0, padx=5, pady=5, sticky='W')

    # MQSC Entry Widgets
        # Script Entry            
        self.mqscnameEntry = ttk.Entry(self.mqscLabelFrame, textvariable=self.mqscname)
        self.mqscnameEntry["width"] = "20"
        self.mqscnameEntry["state"] = "disabled"
        self.mqscnameEntry.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky='WE')
        # QMGR Entry            
        self.qmgrnameEntry = ttk.Entry(self.mqscLabelFrame, textvariable=self.qmgr)
        self.qmgrnameEntry["width"] = "20"
        self.qmgrnameEntry.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky='WE')
        # Script Entry            
        self.mqscEntry = ttk.Entry(self.mqscLabelFrame, textvariable=self.mqsc)
        self.mqscEntry["width"] = "50"
        self.mqscEntry.grid(row=0, column=2, columnspan=5, padx=5, pady=5, sticky='WE')

    # MQSC Buttons
        # MQSC Dialog Button
        self.mqscButton = ttk.Button(self.mqscLabelFrame)
        self.mqscButton["text"] = "Browse..."
        self.mqscButton["command"] = lambda: self.open_filebrowse(1)
        self.mqscButton.grid(row=0, column=7, columnspan=2, padx=5, pady=5, sticky='W')

## Add groups Label Frame
    # groups Label Frame
        self.grpsLabelFrame = ttk.LabelFrame(self.mainFrame)
        self.grpsLabelFrame["text"] = "Select AUT Groups"
        self.grpsLabelFrame.grid(row=2, column= 0, sticky=(N, E, W),
                                padx=5, pady=5, ipadx=5, ipady=5)
        #self.grpsLabelFrame.columnconfigure(0, weight=1)

    # Check Buttons
        #mqm
        self.mqmCheckBtn = ttk.Checkbutton(self.grpsLabelFrame, var=self.mqmcb, onvalue='mqm', offvalue='off')
        self.mqmCheckBtn["text"] = "mqm"
        self.mqmCheckBtn["state"] = "disabled"
        self.mqmCheckBtn.grid(row=0, column=0, padx=5, pady=5, sticky='W')

        #mqbrkrs
        self.mqbrkrsCheckBtn = ttk.Checkbutton(self.grpsLabelFrame, var=self.mqbrkrscb, onvalue='mqbrkrs', offvalue='off')
        self.mqbrkrsCheckBtn["text"] = "mqbrkrs"
        self.mqbrkrsCheckBtn.grid(row=0, column=1, padx=5, pady=5, sticky='W')

        #mqxplr
        self.mqxplrCheckBtn = ttk.Checkbutton(self.grpsLabelFrame, var=self.mqxplrcb, onvalue='mqxplr', offvalue='off')
        self.mqxplrCheckBtn["text"] = "mqxplr"
        self.mqxplrCheckBtn.grid(row=0, column=2, padx=5, pady=5, sticky='W')

        #clstaff
        self.clstaffCheckBtn = ttk.Checkbutton(self.grpsLabelFrame, var=self.clstaffcb, onvalue='clstaff', offvalue='off')
        self.clstaffCheckBtn["text"] = "clstaff"
        self.clstaffCheckBtn.grid(row=0, column=3, padx=5, pady=5, sticky='W')

        #was
        self.wasCheckBtn = ttk.Checkbutton(self.grpsLabelFrame, var=self.wascb, onvalue='was', offvalue='off')
        self.wasCheckBtn["text"] = "was"
        self.wasCheckBtn.grid(row=0, column=4, padx=5, pady=5, sticky='W')

        #was6
        self.was6CheckBtn = ttk.Checkbutton(self.grpsLabelFrame, var=self.was6cb, onvalue='was6', offvalue='off')
        self.was6CheckBtn["text"] = "was6"
        self.was6CheckBtn.grid(row=0, column=5, padx=5, pady=5, sticky='W')

## List of Authority Commands Label Frame
	# List Label Frame
        self.listLabelFrame = ttk.LabelFrame(self.mainFrame)
        self.listLabelFrame["text"] = "Authority Commands"
        self.listLabelFrame.grid(row=3, column= 0, sticky='NSWE',
                                padx=5, pady=5, ipadx=5, ipady=5)
        self.listLabelFrame.columnconfigure(0, weight=1)     
        self.listLabelFrame.rowconfigure(1, weight=1) # allow listbox to resize in labelFrame

    # List Widget Labels
        # Script Label            
        self.listLabel = ttk.Label(self.listLabelFrame)
        self.listLabel["text"] = "Add AUT commands from MQSC file:"
        self.listLabel.grid(row=0, column=3, padx=5, pady=5, sticky='E') 

    # List box for deployment details
        self.listbox = Listbox(self.listLabelFrame, selectmode=EXTENDED)
        # add vertical scrollbar
        self.listscrollv = ttk.Scrollbar(self.listLabelFrame, orient=VERTICAL)
        self.listbox.config(yscrollcommand=self.listscrollv.set)
        self.listscrollv.config(command=self.listbox.yview)
        # add horizontal scrollbar
        self.listscrollh = ttk.Scrollbar(self.listLabelFrame, orient=HORIZONTAL)
        self.listbox.config(xscrollcommand=self.listscrollh.set)
        self.listscrollh.config(command=self.listbox.xview)
        # add default text to listbox
        self.listbox.insert(END, self.cmdaut.get())
        # set scrollbars and list box in grid
        self.listscrollv.grid(row=1, column=7, columnspan=1, padx=(0,5), pady=(5,0), sticky='NSW')
        self.listscrollh.grid(row=2, column=0, columnspan=7, padx=(5,0), pady=(0,5), sticky='WE')
        self.listbox.grid(row=1, column=0, columnspan=7, padx=(5,0), pady=(5,0), sticky='NSWE')

    # Process mqsc file Button
        self.addButton = ttk.Button(self.listLabelFrame)
        self.addButton["text"] = "Add"
        self.addButton["command"] = self.readMqsc
        self.addButton.grid(row=0, column=4, columnspan=1, padx=(5,0), pady=5, sticky='W')
    # Remove commands Button
        self.remButton = ttk.Button(self.listLabelFrame)
        self.remButton["text"] = "Remove"
        self.remButton["command"] = self.removeCommand
        self.remButton.grid(row=0, column=5, columnspan=1, padx=(5,0), pady=2, sticky='E')
    # Clear all commands Button
        self.clearButton = ttk.Button(self.listLabelFrame)
        self.clearButton["text"] = "Clear"
        self.clearButton["command"] = self.clearCommand
        self.clearButton.grid(row=0, column=6, columnspan=1, padx=(5,0), pady=2, sticky='E')

## Export AUT file details Label Frame
    # Export Label Frame
        self.exportLabelFrame = ttk.LabelFrame(self.mainFrame)
        self.exportLabelFrame["text"] = "Export AUT File"
        self.exportLabelFrame.grid(row=4, column= 0, sticky='NSWE',
                                padx=5, pady=5, ipadx=5, ipady=5)
        self.exportLabelFrame.columnconfigure(3, weight=1)
        
    # Export Label Widgets
        # Script Name Label              
        self.scriptnameLabel = ttk.Label(self.exportLabelFrame)
        self.scriptnameLabel["text"] = "AUT Name:"
        self.scriptnameLabel.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        # Export Label              
        self.exportLabel = ttk.Label(self.exportLabelFrame)
        self.exportLabel["text"] = "Export To:"
        self.exportLabel.grid(row=0, column=2, padx=5, pady=5, sticky='W')

    # Export Entry Widgets
        # Script Name Entry              
        self.scriptnameEntry = ttk.Entry(self.exportLabelFrame, textvariable=self.outputfile)
        self.scriptnameEntry["width"] = "15"
        self.scriptnameEntry.grid(row=0, column=1, columnspan=1, padx=(0,5), pady=5, sticky='W')
        self.scriptnameEntry["state"] = "disabled"
        # Export Entry              
        self.exportEntry = ttk.Entry(self.exportLabelFrame, textvariable=self.output)
        self.exportEntry["width"] = "50"
        self.exportEntry.grid(row=0, column=3, columnspan=1, padx=(0,5), pady=5, sticky='WE')
        self.exportEntry["state"] = "disabled"
        # Open after expert checkbutton
        self.clstaffCheckBtn = ttk.Checkbutton(self.grpsLabelFrame, var=self.clstaffcb, onvalue='clstaff', offvalue='off')
        self.clstaffCheckBtn["text"] = "clstaff"
        self.clstaffCheckBtn.grid(row=0, column=3, padx=5, pady=5, sticky='W')

    # Export Buttons
        # Output Dialog Button
        self.outputButton = ttk.Button(self.exportLabelFrame)
        self.outputButton["text"] = "Browse..."
        self.outputButton["command"] = lambda: self.open_dirbrowse(1)
        self.outputButton.grid(row=0, column=5, columnspan=2, padx=5, pady=5, sticky='W')
        self.outputButton["state"] = "disabled"
        # Export Button
        self.exportButton = ttk.Button(self.exportLabelFrame)
        self.exportButton["text"] = "Export"
        self.exportButton["command"] = self.checkAutExists
        self.exportButton.grid(row=1, column=5, columnspan=1, padx=5, pady=5, sticky='E')
        self.exportButton["state"] = "disabled"

# read group authorities file
    def read_queueAut(self):
        ##print "about to try reading config"
        # reading values from grpaut 
        if os.path.isfile("queueaut.ini") == True:
            with open("queueaut.ini") as f:
                file_str = f.readlines()      
            # set grp aut
            for grp in file_str:
                self.queueauth.append(grp.rstrip())
                
            f.close()
            print self.queueauth
            ##print "read config \n" + self.configpath.get() + "\n" + self.dirpath.get() 
        else:
            with open("queueaut.ini", "w+") as f:
                file_str = ['mqm +browse +chg +clr +dlt +dsp +get +inq +put +passall +passid +set +setall +setid\n',
                            'mqbrkrs +browse +chg +clr +dlt +dsp +get +inq +put +passall +passid +set +setall +setid\n',
                            'clstaff +browse +dsp +get +inq',
                            'mqxplr +browse +dsp +get +inq',
                            'was +dsp +passall +passid +setall +setid +browse +get +inq +put +set',
                            'was6 +dsp +passall +passid +setall +setid +browse +get +inq +put +set']
                f.writelines(file_str)
                f.close()
            # Call myself after creating file to set values
            self.read_queueAut()

## Check which AUT check buttons are selected and make a list
    def autList(self):
        for cb in self.chkbtnlist:
            print cb.get()
            if cb.get() != 'off':
                self.grplist.append(cb.get())
                print self.grplist
        # concat grps into a string
        # concat grps string with rest of regular expression
        # set grpexpr
        self.grpexpr.set(r"(QALIAS|QREMOTE|QLOCAL)(.+?)\(\'(.+?)\'\)")

## Read MQSC file and get the required information
    def readMqsc(self):
        # check mqsc file exists
        if os.path.isfile(self.mqsc.get()):
            # open mqsc file
            with open(self.mqsc.get()) as f: 
                    file_str = f.readlines() 
            # search file for queues and channels 
            for t in file_str: 
                mqueue = re.search(self.qexpr.get(), t)
                mchnl = re.search(self.chlexpr.get(), t)
                if mqueue: 
                    qname = mqueue.group(3)
                    self.qlist.append(qname)
                elif mchnl:
                    chlname = mchnl.group(2)
                    self.chlist.append(chlname)
            # empty group list
            del self.grplist[:]
            # check which AUT groups have been selected
            self.autList()
            # call function that creates AUT commands and adds them to the listBox
            self.createAutList()
            f.close()
        else:
            if os.path.isfile(self.mqsc.get()) == False:
                # if mqsc script doesn't exist in specified location alert user
                tkMessageBox.showerror(title='MQSC Script Error',
                              message='I cannot find the MQSC Script in the specified path:\n\n' +
                              self.mqsc.get())
            

## Create AUT file and write authority commands for the MQ objects
    def writeAut(self):
        # create new AUT file
        outputloc = self.output.get() + '/' + self.outputfile.get()
        with open(outputloc, "w+") as f:
            l = []
            for x in self.listbox.get(0, END):
                l.append(x + '\n')
            f.writelines(l)
        f.close()
        webbrowser.open(outputloc)

            
    def checkAutExists(self):
        # check export destination exists
        outputloc = self.output.get() + '/' + self.outputfile.get()
        if os.path.isdir(self.output.get()):
            if os.path.isfile(outputloc) == False:
                self.writeAut()
            else:
                result = tkMessageBox.askquestion(title='Overwrite Existin AUT File?',
                                         message='AUT file ' + self.outputfile.get() + ' already exists!!\n\n' +
                                                  'Would you like to overwrite it?',
                                         default='no')
                if result == 'yes':
                    self.writeAut()
                else:
                    return
        elif os.path.isdir(self.output.get()) == False:
            # path doesn't exist alert user
            tkMessageBox.showerror(title='Output File Error',
                                  message='I cannot find the Output File path:\n\n' +
                                  self.output.get())
        else:
            return
                

    def createAutList(self):
        # clear list box before adding
        self.listbox.delete(0, END)
        # create commands for queue names in the list
        tmplist = self.qlist
        for q in tmplist:
            self.objTypeVar.set('queue')
            self.mqobjVar.set(q)
            self.createCommand()
           
        # create commands for channel names in the list
        for c in self.chlist:
            self.objTypeVar.set('channel')
            self.mqobjVar.set(c)
            self.createCommand()

        # empty lists
        del self.qlist[:]
        del self.chlist[:]
        # enable export and remove buttons and entries
        self.scriptnameEntry["state"] = "normal"
        self.exportEntry["state"] = "normal"
        self.outputButton["state"] = "normal"
        self.exportButton["state"] = "normal"
        self.remButton["state"] = "normal"
        self.clearButton["state"] = "normal"
        
        

## Create authoritiy commands
    def createCommand(self):
        autmaxqueue = ' +browse +chg +clr +dlt +dsp +get +inq +put +passall +passid +set +setall +setid '
        autappqueue = ' +dsp +passall +passid +setall +setid +browse +get +inq +put +set '
        autminqueue = ' +browse +dsp +get +inq '
        autmaxchl = ' +chg +dlt +dsp +ctrl +ctrlx '
        autminchl = ' +dsp '
        autcmdVar = StringVar()
        # create commands for each user group
        for g in self.grplist:
            if self.objTypeVar.get() == 'queue':
                # if user group mqm or broker give full authorities else basic authoritites 
                if g == 'mqm' or g == 'mqbrkrs':
                        autcmdVar.set('setmqaut -m ' + self.qmgr.get() + ' -n '
                                                                + self.mqobjVar.get() + ' -t ' + self.objTypeVar.get() + ' -g ' + g + autmaxqueue)
                        self.listbox.insert(END, autcmdVar.get())
                elif g == 'was':
                        autcmdVar.set('setmqaut -m ' + self.qmgr.get() + ' -n '
                                                                + self.mqobjVar.get() + ' -t ' + self.objTypeVar.get() + ' -g ' + g + autappqueue)
                        self.listbox.insert(END, autcmdVar.get())
                else:
                        autcmdVar.set('setmqaut -m ' + self.qmgr.get() + ' -n '
                                                                + self.mqobjVar.get() + ' -t ' + self.objTypeVar.get() + ' -g ' + g + autminqueue)
                        self.listbox.insert(END, autcmdVar.get())
            elif self.objTypeVar.get() == 'channel':
                if g == 'mqm' or g == 'mqbrkrs':
                        autcmdVar.set('setmqaut -m ' + self.qmgr.get() + ' -n '
                                                                + self.mqobjVar.get() + ' -t ' + self.objTypeVar.get() + ' -g ' + g + autmaxchl)
                        self.listbox.insert(END, autcmdVar.get())
                else:
                        autcmdVar.set('setmqaut -m ' + self.qmgr.get() + ' -n '
                                                                + self.mqobjVar.get() + ' -t ' + self.objTypeVar.get() + ' -g ' + g + autminchl)
                        self.listbox.insert(END, autcmdVar.get())

            
    # text change detected in QMGR entry, update output feild
    def on_qmgr_trace(self, *args):
        outputfile = self.qmgr.get() + '.AUT'
        self.outputfile.set(outputfile)

    
        
    # Remove selected items from Listbox    
    def removeCommand(self):
        self.listitems = self.listbox.curselection()
        for x in self.listitems:
            l = self.listbox.curselection()
            li = l[0] 
            self.listbox.delete(li)
            
        # Check if list is empty if so disable script buttons
        if self.listbox.size() == 0:
            self.scriptnameEntry["state"] = "disabled"
            self.exportEntry["state"] = "disabled"
            self.outputButton["state"] = "disabled"
            self.exportButton["state"] = "disabled"
            self.exportButton["state"] = "disabled"
            self.remButton["state"] = "disabled"
            self.clearButton["state"] = "disabled"

    # Clear all from Listbox    
    def clearCommand(self):
        # clear listbox
        self.listbox.delete(0, END)          
        # disable things
        self.scriptnameEntry["state"] = "disabled"
        self.exportEntry["state"] = "disabled"
        self.outputButton["state"] = "disabled"
        self.exportButton["state"] = "disabled"
        self.exportButton["state"] = "disabled"
        self.remButton["state"] = "disabled"
        self.clearButton["state"] = "disabled"
            
    # Open file dialog
    def open_filebrowse(self, number):
        # file dialog
        fileloc = tkFileDialog.askopenfilename(parent=app,title='Please select a file')
        if number == 1:
            # set mqsc file path before spliting it
            self.mqsc.set(fileloc)
            # get filepath and set output file path
            filepath, filename = os.path.split(self.mqsc.get())
            qmgrname = os.path.splitext(filename)[0]
            self.qmgr.set(qmgrname)
            self.mqscname.set(filename)
            self.output.set(filepath)
            #self.scriptloc.set(filepath)
        else:
            return
            #self.scriptfloc.set(fileloc)

            
    # Open directory dialog
    def open_dirbrowse(self, number):
        # directory dialog
        dirname = tkFileDialog.askdirectory(parent=app,title='Please select a directory')
        # opened by output
        if number == 1:
            self.output.set(dirname)
        else:
            return
            #self.scriptloc.set(dirname)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(column=0, row=0, sticky=(N, S, W, E))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.createWidgets()
        self.state.set('True')

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.minsize(width=750, height=440)
app = Application(master=root)
img = PhotoImage(file='iconBlue.gif')
app.master.call('wm', 'iconphoto', root._w, img)
app.master.title("AUT Builder")
app.mainloop()
