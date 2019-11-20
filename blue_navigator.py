###############################
#   Name: Blue Navigator      # 
# Filename: blue_navigator.py #
#       Version: 1.0          # 
#   Developer: Nicolas CHEN   # 
###############################

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys
import about_dialog

class MainWindow(QMainWindow):
    """ Class MainWindow with all widgets """

    def __init__(self, *args, **kwargs):
        """ Constructor of the class MainWindow.
            We define all widgets needed.      
        """
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)        

        self.setCentralWidget(self.tabs)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon(os.path.join('icons', 'arrow_left.png')), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        next_btn = QAction(QIcon(os.path.join('icons', 'arrow_right.png')), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(next_btn)

        reload_btn = QAction(QIcon(os.path.join('icons', 'arrow_reload.png')), "Reload", self)
        reload_btn.setStatusTip("Reload")
        reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navtb.addAction(reload_btn)

        home_btn = QAction(QIcon(os.path.join('icons', 'home.png')), "Home", self)
        home_btn.setStatusTip("Home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock.png')))
        navtb.addWidget(self.httpsicon)

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction(QIcon(os.path.join('icons', 'cross_square.png')), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        navtb.addAction(stop_btn)
        
        self.menuBar().setNativeMenuBar(False)

        file_menu = self.menuBar().addMenu("&File")

        new_tab_action = QAction(QIcon(os.path.join('icons', 'add_tab.png')), "New Tab...", self)
        new_tab_action.setStatusTip("Open a new tab")
        new_tab_action.triggered.connect(lambda x: self.add_new_tab())
        file_menu.addAction(new_tab_action)

        open_file_action = QAction(QIcon(os.path.join('icons', 'open_file.png')), "Open file...", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join('icons', 'save.png')), "Save Page As...", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction(QIcon(os.path.join('icons', 'printer.png')), "Print...", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        help_menu = self.menuBar().addMenu("&Help")

        navigate_blue_navigator_action = QAction(QIcon(os.path.join('icons', 'lifebuoy.png')), "Go to Wikipedia", self)
        navigate_blue_navigator_action.setStatusTip("Find out more about Wikipedia")
        navigate_blue_navigator_action.triggered.connect(self.navigate_blue_navigator)
        help_menu.addAction(navigate_blue_navigator_action)

        about_action = QAction(QIcon(os.path.join('icons', 'question.png')), "About Blue Navigator", self)
        about_action.setStatusTip("Find out more about Blue Navigator")
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)        

        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')       

        self.show()

        self.setWindowTitle("Blue Navigator")
        self.setWindowIcon(QIcon(os.path.join('icons', 'earth.png')))

    def add_new_tab(self, qurl=None, label="New Tab"):
        """ Add a new tab

        Parameters:
        self -- instance of a class
        qurl -- url address
        label -- new tab label
        """        
        if qurl is None:
            qurl =QUrl('') 

        browser = QWebView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)  

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))

        browser.loadFinished.connect(lambda _, i=i, browser=browser: 
            self.tabs.setTabText(i, browser.page().mainFrame().title()))

    def tab_open_doubleclick(self, output_double_click):
        """ Open a new tab with double click

        Parameters:
        self -- instance of a class
        output_double_click -- output of double click
        """        
        if output_double_click == -1:
            self.add_new_tab()

    def current_tab_changed(self):
        """ Current tab change

        Parameters:
        self -- instance of a class
        """
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())

    def close_current_tab(self, i):
        """ Close current tab

        Parameters:
        self -- instance of a class
        i -- tab number
        """        
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def navigate_blue_navigator(self):
        """ Go to the Wikipedia web page

        Parameters:
        self -- instance of a class
        """        
        self.tabs.currentWidget().setUrl(QUrl("https://www.wikipedia.org"))

    def about(self):
        """ About window

        Parameters:
        self -- instance of a class
        """        
        dlg = about_dialog.AboutDialog()
        dlg.exec_()

    def open_file(self):
        """ Open a new file

        Parameters:
        self -- instance of a class
        """        
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Hypertext Markup Language (*.htm *.html);;""All files (*.*)")

        if filename:
            with open(filename, 'r') as f:
                html = f.read()

            self.tabs.currentWidget().setHtml(html)
            self.urlbar.setText(filename)

    def save_file(self):
        """ Save a new file

        Parameters:
        self -- instance of a class
        """        
        filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "", "Hypertext Markup Language (*.htm *.html);;""All files (*.*)")

        if filename:
            html = self.tabs.currentWidget().page().mainFrame().toHtml()
            with open(filename, 'w') as f:
                f.write(html.encode('utf8'))

    def print_page(self):
        """ Print web page

        Parameters:
        self -- instance of a class
        """        
        dlg = QPrintPreviewDialog()
        dlg.paintRequested.connect(self.tabs.currentWidget().print_)

        dlg.exec_()

    def navigate_home(self):
        """ Go to Home page

        Parameters:
        self -- instance of a class
        """        
        self.tabs.currentWidget().setUrl(QUrl("http://google.com"))

    def navigate_to_url(self):
        """ Navigate to url

        Parameters:
        self -- instance of a class
        """        
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, qurl, browser=None):
        """ Update the url bar

        Parameters:
        self -- instance of a class
        browser -- QWebView()
        """        
        
        if browser != self.tabs.currentWidget():
            #if this signal is not from the current tab, ignore
            return

        if qurl.scheme() == 'https':
            # Secure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock-ssl.png')))
        else:
            # Insecure padlock icon
            self.httpsicon.setPixmap(QPixmap(os.path.join('icons', 'lock.png')))

        self.urlbar.setText(qurl.toString())
        self.urlbar.setCursorPosition(0)

app = QApplication(sys.argv)
app.setApplicationName("Blue Navigator")
app.setOrganizationName("Blue Navigator")
app.setOrganizationDomain("blue-navigator.org")

window = MainWindow()
window.show()

app.exec_()