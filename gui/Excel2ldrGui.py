#!/usr/bin/python
# Author: Jonathan Yu
# Date: 7/12/2017
# Email: jonathan.yu@csiro.au

# GUI wrapper for excel2ldr using wxPython

import wx, wx.html
import sys, os
import ldrpyutils
import json
import ldrpyutils.core
import requests


aboutText = """<p>Excel to LDR is a client tool for uploading/updating registers on the Linked Data Registry.
See ldrpyutils Github page for more info about the toolkit.<br/>
(c) 2017 CSIRO Land and Water. Environmental Informatics Group. 
</p>"""

VERSION = 'v1.1.0'

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600, 400)):
        wx.html.HtmlWindow.__init__(self, parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About Excel to LDR",
                           style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER |
                                 wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400, 200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        self.isMulti = False
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth() + 25, irep.GetHeight() + 10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()

#Main panel setup here
class Frame(wx.Frame):

    # initialise configuration
    def setupConfigs(self):
        self.configfile = self.resource_path("config.json")
        self.readConfig()
        self.isMulti = False

    def resource_path(self, relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    def readConfig(self):
        self.config = None

        #path = os.path.realpath(__file__)
        #path = os.path.realpath(self.configfile)
        with open(self.configfile) as cfg_file:
            #print(cfg_file)
            self.config = json.load(cfg_file)
        #print(self.config)

    def __init__(self, title):
        self.setupConfigs()
        wx.Frame.__init__(self, None, title=title, pos=(150, 150), size=(500, 500))
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        ico = wx.Icon(self.resource_path("csiro.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        # Menu items defined here
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        m_exit = menu.Append(wx.ID_EXIT, "E&xit\tAlt-X", "Close window and exit program.")
        self.Bind(wx.EVT_MENU, self.OnClose, m_exit)
        menuBar.Append(menu, "&File")
        menu = wx.Menu()
        m_about = menu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, m_about)
        menuBar.Append(menu, "&Help")
        self.SetMenuBar(menuBar)

        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusWidths([100, -1])

        self.statusbar.SetStatusText(VERSION)

        # Main panel defined here
        panel = wx.Panel(self)
        box = wx.BoxSizer(wx.VERTICAL)

        # Header
        m_text = wx.StaticText(panel, -1, "Excel to LDR")
        m_text.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        m_text.SetSize(m_text.GetBestSize())
        box.Add(m_text, 0, wx.ALL, 10)

        # User input panel widgets defined here
        # File picker
        self.label1 = wx.StaticText(panel, wx.ID_ANY, "Select the Input File")
        self.fileCtrl = wx.FilePickerCtrl(panel, message="Select the input file name")
        #self.selectedfile = wx.TextCtrl(panel, wx.ID_ANY, "None", size=(490, 25))
        self.selectedfile = None

        self.fileCtrl.Bind(wx.EVT_FILEPICKER_CHANGED, self.Selected)
        #row1 = wx.BoxSizer(wx.VERTICAL)
        #row1.Add(self.label1, 0, wx.TOP | wx.RIGHT, 5)
        #row1.Add(self.fileCtrl)
        #row1.Add(self.selectedfile)
        box.Add(self.label1, 0, wx.ALL, 10)
        box.Add(self.fileCtrl, 0, wx.ALL, 10)
        #box.Add(self.selectedfile, 0, wx.ALL, 10)

        # Ask user if file is configured for multi-register content update
        self.cb1 = wx.CheckBox(panel, label='Multi-register')
        self.Bind(wx.EVT_CHECKBOX, self.onChecked)
        box.Add(self.cb1, 0, wx.ALL, 10)

        # Ask for user credentials
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        userLabel = wx.StaticText(panel, -1, "Username:")
        self.userText = wx.TextCtrl(panel, -1, "", size=(175, -1))
        self.userText.SetInsertionPoint(0)

        pwdLabel = wx.StaticText(panel, -1, "Password:")
        self.pwdText = wx.TextCtrl(panel, -1, "", size=(175, -1), style=wx.TE_PASSWORD)

        box.Add(userLabel, 0, wx.ALL, 10)
        box.Add(self.userText, 0, wx.ALL, 10)

        box.Add(pwdLabel, 0, wx.ALL, 10)
        box.Add(self.pwdText, 0, wx.ALL, 10)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Action buttons
        m_send_content = wx.Button(panel, wx.ID_OK, "Send content")
        m_send_content.Bind(wx.EVT_BUTTON, self.OnSend)
        btnSizer.Add(m_send_content, 0, wx.ALL, 10)

        box.Add(btnSizer, 0 , wx.ALL, 10)

        panel.SetSizer(box)
        panel.Layout()

    # Event function: on checked
    def onChecked(self, e):
        cb = e.GetEventObject()
        #print cb.GetLabel(), ' is clicked', cb.GetValue()
        if(cb.GetValue() == 'Multi-register'):
            self.isMulti = cb.GetValue()

    # Event: on file selected
    def Selected(self, event):
        #self.selectedfile.SetValue(self.fileCtrl.GetPath())
        self.selectedfile = self.fileCtrl.GetPath()

    # Event: on send button clicked
    def OnSend(self, event):
        self.run()

    # Event: on close event (not currently used but might be useful!)
    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
                               "Do you really want to close this application?",
                               "Confirm Exit", wx.OK | wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()

    # About clicked
    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy()

    # Method to call ldrpyutils send functions
    def run(self):
        filepath = self.selectedfile
        user = self.userText.GetValue()
        passwd = self.pwdText.GetValue()
        isMulti = self.isMulti
        emitFile = self.config['emitFile']
        registry_url = self.config['registry_url']
        updateOnlineRegisters = self.config['updateOnlineRegisters']
        verbose = self.config['verbose']

        registry_auth_url = registry_url + "/system/security/apilogin"

        if filepath is None:
            self.displayNoFileSelectedProblemDlg()
            return

        #print(user)
        #print(passwd)
        if user == '' or passwd == ''\
                or user == None or passwd == None:
            self.displayUserCredentialsProblemDlg()
            return

        try:
            if isMulti:
                resultFlag = ldrpyutils.core.load_multi_register_file(filepath, user, passwd, emitFile=emitFile,
                                                  registry_auth_url=registry_auth_url,
                                                  updateOnlineRegisters=updateOnlineRegisters,
                                                  verbose=verbose)

            else:
                resultFlag = ldrpyutils.core.load_simple_file(filepath, user, passwd, emitFile=emitFile,
                                          registry_auth_url=registry_auth_url,
                                          updateOnlineRegisters=updateOnlineRegisters,
                                          verbose=verbose
                                          )
                if(resultFlag):
                    self.statusbar.SetStatusText("Content successfully sent!",1)
                else:
                    self.statusbar.SetStatusText("Content send failed.",1)
        except requests.ConnectionError as e:
            #print("ConnectionError")
            self.displayConnectionProblemDlg()

    # method to show info dialog boxes
    def displayInfoDlg(self, title, message):
        dlg = wx.MessageDialog(self,
                               message,
                               title, wx.OK )
        result = dlg.ShowModal()
        dlg.Destroy()

    # pre-canned info dialog box messages

    def displayConnectionProblemDlg(self):
        self.displayInfoDlg("Connection issue", "Could not reach registry at " + self.config['registry_url']
                                    + ". Check your connection and try again later.")

    def displayNoFileSelectedProblemDlg(self):
        self.displayInfoDlg("Please select file", "No file selected. Please select a file to update registry with.")

    def displayUserCredentialsProblemDlg(self):
        self.displayInfoDlg("Please enter username and password",
                "No username and/or password found. Please enter user credentials.")

    def displayUserCredentialsProblemDlg(self):
        self.displayInfoDlg("Success!",
                "Content was submitted successfully! Check the register online to verify.")



app = wx.App(redirect=True)  # Error messages go to popup window
top = Frame("Excel to LDR")
top.Show()
app.MainLoop()