import os
import configparser
import wx
import functions as fcn

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        self.width = 1280
        self.height = 720
        self.ui_border = 15
        self.path = os.path.dirname(os.path.abspath(__file__))
        wx.Frame.__init__(self, parent, title=title, size=(self.width, self.height))
        self.get_config()
        self.init_ui()
        self.init_menu()
        self.Show()

    def init_menu(self):
        filemenu = wx.Menu()
        menu_exit = filemenu.Append(wx.ID_EXIT, '終了')
        self.Bind(wx.EVT_MENU, self.exit, menu_exit)

        menu_bar = wx.MenuBar()
        menu_bar.Append(filemenu, 'メニュー')
        self.SetMenuBar(menu_bar)

    def init_ui(self):
        self.CreateStatusBar()

        layout = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, -1)
        
        layout_ui = wx.BoxSizer(wx.HORIZONTAL)
        self.address = self.config['DATA']['address']
        self.choose_button = wx.Button(panel, wx.ID_ANY, 'フォルダ選択', size=(100, 28))
        self.choose_text = wx.TextCtrl(panel, wx.ID_ANY, self.address)
        self.choose_button.Bind(wx.EVT_BUTTON, self.choose_folder)
        layout_ui.Add(self.choose_text, 1)
        layout_ui.Add((20, -1))
        layout_ui.Add(self.choose_button)
        layout.Add(layout_ui, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, self.ui_border)

        layout.Add((-1, 20))

        layout_search = wx.BoxSizer(wx.HORIZONTAL)
        self.search_text = wx.TextCtrl(panel, wx.ID_ANY)
        self.search_button = wx.Button(panel, wx.ID_ANY, '検索', size=(100, 28))
        self.search_button.Bind(wx.EVT_BUTTON, self.onsearch)
        layout_search.Add(self.search_text, 1)
        layout_search.Add((20, -1))
        layout_search.Add(self.search_button)
        layout.Add(layout_search, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, self.ui_border)

        layout.Add((-1, 20))

        layout_cf = wx.BoxSizer(wx.HORIZONTAL)
        self.check1 = wx.CheckBox(panel, wx.ID_ANY, '大文字小文字を区別しない')
        self.check1.SetValue(self.config['DATA'].getboolean('ignorecase'))
        self.check2 = wx.CheckBox(panel, wx.ID_ANY, '検索結果をテキスト出力')
        self.check2.SetValue(self.config['DATA'].getboolean('output'))
        overwrite_button = wx.Button(panel, wx.ID_ANY, '設定を保存', size=(100, 28))
        overwrite_button.Bind(wx.EVT_BUTTON, self.overwrite_config)
        layout_cf.Add(self.check1)
        layout_cf.Add(self.check2)
        layout_cf.Add(overwrite_button, 0, wx.ALIGN_RIGHT)
        layout.Add(layout_cf, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, self.ui_border)

        layout.Add((-1, 20))

        layout_res = wx.BoxSizer(wx.HORIZONTAL)
        self.res = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE)
        layout_res.Add(self.res, 1, wx.EXPAND)
        layout.Add(layout_res, 1, wx.EXPAND | wx.BOTTOM | wx.LEFT | wx.RIGHT, self.ui_border)

        panel.SetSizer(layout)

    def get_config(self):
        if 'config.ini' not in os.listdir(self.path):
            self.create_config()
        self.config = configparser.ConfigParser()
        self.config.read(self.path + '\\config.ini')

    def overwrite_config(self, event):
        self.config['DATA']['address'] = self.choose_text.GetValue()
        self.config['DATA']['ignorecase'] = str(self.check1.GetValue())
        self.config['DATA']['output'] = str(self.check2.GetValue())
        with open(self.path + '\\config.ini', 'w') as cf:
            self.config.write(cf)
        self.SetStatusText('設定を保存')

    def create_config(self):
        config = configparser.ConfigParser()
        config['DATA'] = {'address': 'C:\\Users\\User\\AppData\\Roaming\\.minecraft\\logs'
        , 'ignorecase': 'True'
        , 'output': 'False'}
        with open(self.path + '\\config.ini', 'w') as cf:
            config.write(cf)

    def onsearch(self, event):
        if self.search_text.GetValue() != '':
            try:
                fcn.search(self)
            except:
                self.SetStatusText('エラーが発生しました')

    def choose_folder(self, event):
        folder = wx.DirDialog(self, style=wx.DD_CHANGE_DIR, message='ログ保存フォルダ')
        if folder.ShowModal() == wx.ID_OK:
            self.address = folder.GetPath()
        folder.Destroy()
        self.choose_text.SetLabel(self.address)
        self.config['DATA']['address'] = self.address

    def exit(self, event):
        self.Close(True)

app = wx.App(False)
frame = MainWindow(None, 'Log search')
app.MainLoop()