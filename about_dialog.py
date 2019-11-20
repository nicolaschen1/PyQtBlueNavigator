##############################
#   Name: Blue Navigator     # 
#  Filename: about_dialog.py #
#       Version: 1.0         # 
#   Developer: Nicolas CHEN  # 
##############################

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtPrintSupport import *

import os
import sys

class AboutDialog(QDialog):
    """ Class AboutDialog """
    
    def __init__(self, *args, **kwargs):
        """ Constructor of the class MainWindow.
            We define all widgets needed.      
        """
        super(AboutDialog, self).__init__(*args, **kwargs)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Blue Navigator")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)
        title.setAlignment(Qt.AlignHCenter)

        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join('icons', 'earth.png')))
        layout.addWidget(logo)

        layout.addWidget(QLabel("Version 1.0"))
        layout.addWidget(QLabel("Developer: Nicolas CHEN"))
        layout.addWidget(QLabel("Copyright 2019 Blue Navigator"))

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)