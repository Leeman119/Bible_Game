# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'release_notes.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_release_notes(object):
    def setupUi(self, release_notes):
        release_notes.setObjectName("release_notes")
        release_notes.resize(350, 450)
        release_notes.setMinimumSize(QtCore.QSize(350, 450))
        release_notes.setMaximumSize(QtCore.QSize(1920, 1080))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        release_notes.setFont(font)
        release_notes.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Images/scroll.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        release_notes.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(release_notes)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(release_notes)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 330, 399))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.update_lbl = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.update_lbl.sizePolicy().hasHeightForWidth())
        self.update_lbl.setSizePolicy(sizePolicy)
        self.update_lbl.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.update_lbl.setFont(font)
        self.update_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.update_lbl.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.update_lbl.setFrameShadow(QtWidgets.QFrame.Plain)
        self.update_lbl.setText("")
        self.update_lbl.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.update_lbl.setWordWrap(True)
        self.update_lbl.setObjectName("update_lbl")
        self.verticalLayout_4.addWidget(self.update_lbl)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(25)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.ok_btn = QtWidgets.QPushButton(release_notes)
        self.ok_btn.setMaximumSize(QtCore.QSize(80, 40))
        self.ok_btn.setObjectName("ok_btn")
        self.horizontalLayout.addWidget(self.ok_btn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(release_notes)
        QtCore.QMetaObject.connectSlotsByName(release_notes)

    def retranslateUi(self, release_notes):
        _translate = QtCore.QCoreApplication.translate
        release_notes.setWindowTitle(_translate("release_notes", "Latest release notes"))
        self.ok_btn.setText(_translate("release_notes", "Ok"))

