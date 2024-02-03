# Form implementation generated from reading ui file 'ML4MC.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from functools import partial
from controller import AgentController
import sys
import os
from multiprocessing import Process, Queue


DIRNAME = os.path.dirname(__file__)
OBS_QUEUE = Queue()
OBJECTIVE_QUEUE = Queue()
AI_CONTROLLER = AgentController(DIRNAME, OBS_QUEUE, OBJECTIVE_QUEUE)
BACKEND_PROCESS = Process(target=AI_CONTROLLER.run)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1154, 708)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(9, 9, 1131, 641))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.goalInfoGroupBox = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget_3)
        self.goalInfoGroupBox.setObjectName("goalInfoGroupBox")
        self.goalProgressBar = QtWidgets.QGroupBox(parent=self.goalInfoGroupBox)
        self.goalProgressBar.setGeometry(QtCore.QRect(10, 70, 351, 61))
        self.goalProgressBar.setObjectName("goalProgressBar")
        self.progressBar = QtWidgets.QProgressBar(parent=self.goalProgressBar)
        self.progressBar.setGeometry(QtCore.QRect(10, 30, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.goalSelectGroupbox = QtWidgets.QGroupBox(parent=self.goalInfoGroupBox)
        self.goalSelectGroupbox.setGeometry(QtCore.QRect(10, 140, 351, 311))
        self.goalSelectGroupbox.setObjectName("goalSelectGroupbox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.goalSelectGroupbox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 335, 281))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.diamondRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        self.diamondRadio.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(True)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.diamondRadio.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/diamond.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.diamondRadio.setIcon(icon)
        self.diamondRadio.setIconSize(QtCore.QSize(50, 50))
        self.diamondRadio.setChecked(True)
        self.diamondRadio.setObjectName("diamondRadio")
        self.verticalLayout.addWidget(self.diamondRadio)
        self.ironRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Assets/iron.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ironRadio.setIcon(icon1)
        self.ironRadio.setIconSize(QtCore.QSize(50, 50))
        self.ironRadio.setObjectName("ironRadio")
        self.verticalLayout.addWidget(self.ironRadio)
        self.surviveRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Assets/bed.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.surviveRadio.setIcon(icon2)
        self.surviveRadio.setIconSize(QtCore.QSize(50, 50))
        self.surviveRadio.setObjectName("surviveRadio")
        self.verticalLayout.addWidget(self.surviveRadio)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.woodRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Assets/log.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.woodRadio.setIcon(icon3)
        self.woodRadio.setIconSize(QtCore.QSize(50, 50))
        self.woodRadio.setObjectName("woodRadio")
        self.verticalLayout_2.addWidget(self.woodRadio)
        self.stoneRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Assets/cobble.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.stoneRadio.setIcon(icon4)
        self.stoneRadio.setIconSize(QtCore.QSize(50, 50))
        self.stoneRadio.setObjectName("stoneRadio")
        self.verticalLayout_2.addWidget(self.stoneRadio)
        self.combatRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Assets/hostiles.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.combatRadio.setIcon(icon5)
        self.combatRadio.setIconSize(QtCore.QSize(50, 50))
        self.combatRadio.setObjectName("combatRadio")
        self.verticalLayout_2.addWidget(self.combatRadio)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.currentObjectiveLabel = QtWidgets.QLabel(parent=self.goalInfoGroupBox)
        self.currentObjectiveLabel.setGeometry(QtCore.QRect(10, 20, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.currentObjectiveLabel.setFont(font)
        self.currentObjectiveLabel.setObjectName("currentObjectiveLabel")
        self.loadEnvironmentButton = QtWidgets.QPushButton(parent=self.goalInfoGroupBox)
        self.loadEnvironmentButton.setGeometry(QtCore.QRect(20, 460, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.loadEnvironmentButton.setFont(font)
        self.loadEnvironmentButton.setObjectName("loadEnvironmentButton")
        self.loadModelButton = QtWidgets.QPushButton(parent=self.goalInfoGroupBox)
        self.loadModelButton.setGeometry(QtCore.QRect(20, 510, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.loadModelButton.setFont(font)
        self.loadModelButton.setObjectName("loadModelButton")
        self.verticalLayout_6.addWidget(self.goalInfoGroupBox)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groupBox_AI_Stats = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget_3)
        self.groupBox_AI_Stats.setObjectName("groupBox_AI_Stats")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.groupBox_AI_Stats)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(20, 30, 331, 101))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.healthIcon = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.healthIcon.sizePolicy().hasHeightForWidth())
        self.healthIcon.setSizePolicy(sizePolicy)
        self.healthIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.healthIcon.setText("")
        self.healthIcon.setPixmap(QtGui.QPixmap("Assets/healthHQ.png"))
        self.healthIcon.setScaledContents(True)
        self.healthIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.healthIcon.setObjectName("healthIcon")
        self.horizontalLayout_5.addWidget(self.healthIcon)
        self.healthValue = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.healthValue.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.healthValue.setFont(font)
        self.healthValue.setObjectName("healthValue")
        self.horizontalLayout_5.addWidget(self.healthValue)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.hungerIcon = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.hungerIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.hungerIcon.setText("")
        self.hungerIcon.setPixmap(QtGui.QPixmap("Assets/hungerHQ.png"))
        self.hungerIcon.setScaledContents(True)
        self.hungerIcon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hungerIcon.setObjectName("hungerIcon")
        self.horizontalLayout_4.addWidget(self.hungerIcon)
        self.hungerValueLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.hungerValueLabel.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.hungerValueLabel.setFont(font)
        self.hungerValueLabel.setObjectName("hungerValueLabel")
        self.horizontalLayout_4.addWidget(self.hungerValueLabel)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.xCoordLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.xCoordLabel.setFont(font)
        self.xCoordLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.xCoordLabel.setObjectName("xCoordLabel")
        self.horizontalLayout_8.addWidget(self.xCoordLabel)
        self.yCoordLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.yCoordLabel.setFont(font)
        self.yCoordLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.yCoordLabel.setObjectName("yCoordLabel")
        self.horizontalLayout_8.addWidget(self.yCoordLabel)
        self.zCoordLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.zCoordLabel.setFont(font)
        self.zCoordLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.zCoordLabel.setObjectName("zCoordLabel")
        self.horizontalLayout_8.addWidget(self.zCoordLabel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.inventoryGroupBox = QtWidgets.QGroupBox(parent=self.groupBox_AI_Stats)
        self.inventoryGroupBox.setGeometry(QtCore.QRect(10, 140, 171, 451))
        self.inventoryGroupBox.setObjectName("inventoryGroupBox")
        self.inventoryTable = QtWidgets.QTableWidget(parent=self.inventoryGroupBox)
        self.inventoryTable.setGeometry(QtCore.QRect(10, 30, 151, 411))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inventoryTable.sizePolicy().hasHeightForWidth())
        self.inventoryTable.setSizePolicy(sizePolicy)
        self.inventoryTable.setMaximumSize(QtCore.QSize(10000, 10000))
        self.inventoryTable.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inventoryTable.setFont(font)
        self.inventoryTable.setTextElideMode(QtCore.Qt.TextElideMode.ElideRight)
        self.inventoryTable.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.inventoryTable.setObjectName("inventoryTable")
        self.inventoryTable.setColumnCount(1)
        self.inventoryTable.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setItem(2, 0, item)
        self.inventoryTable.horizontalHeader().setCascadingSectionResizes(False)
        self.stepsGroupBox = QtWidgets.QGroupBox(parent=self.groupBox_AI_Stats)
        self.stepsGroupBox.setGeometry(QtCore.QRect(190, 140, 171, 451))
        self.stepsGroupBox.setObjectName("stepsGroupBox")
        self.stepsTable = QtWidgets.QTableWidget(parent=self.stepsGroupBox)
        self.stepsTable.setGeometry(QtCore.QRect(10, 30, 151, 411))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stepsTable.sizePolicy().hasHeightForWidth())
        self.stepsTable.setSizePolicy(sizePolicy)
        self.stepsTable.setMaximumSize(QtCore.QSize(10000, 10000))
        self.stepsTable.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stepsTable.setFont(font)
        self.stepsTable.setTextElideMode(QtCore.Qt.TextElideMode.ElideRight)
        self.stepsTable.setGridStyle(QtCore.Qt.PenStyle.SolidLine)
        self.stepsTable.setObjectName("stepsTable")
        self.stepsTable.setColumnCount(1)
        self.stepsTable.setRowCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.stepsTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.stepsTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.stepsTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.stepsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.stepsTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.stepsTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.stepsTable.setItem(2, 0, item)
        self.stepsTable.horizontalHeader().setCascadingSectionResizes(False)
        self.verticalLayout_8.addWidget(self.groupBox_AI_Stats)
        self.horizontalLayout_7.addLayout(self.verticalLayout_8)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.controlsGroupBox = QtWidgets.QGroupBox(parent=self.horizontalLayoutWidget_3)
        self.controlsGroupBox.setObjectName("controlsGroupBox")
        self.actionGroupBox = QtWidgets.QGroupBox(parent=self.controlsGroupBox)
        self.actionGroupBox.setGeometry(QtCore.QRect(9, 20, 351, 121))
        self.actionGroupBox.setObjectName("actionGroupBox")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.actionGroupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 331, 82))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.playButton = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playButton.sizePolicy().hasHeightForWidth())
        self.playButton.setSizePolicy(sizePolicy)
        self.playButton.setText("")
        self.playButton.setPixmap(QtGui.QPixmap("Assets/play button.png"))
        self.playButton.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_2.addWidget(self.playButton)
        self.pauseButton = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pauseButton.sizePolicy().hasHeightForWidth())
        self.pauseButton.setSizePolicy(sizePolicy)
        self.pauseButton.setText("")
        self.pauseButton.setPixmap(QtGui.QPixmap("Assets/pause button.png"))
        self.pauseButton.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_2.addWidget(self.pauseButton)
        self.capturingGroupBox = QtWidgets.QGroupBox(parent=self.controlsGroupBox)
        self.capturingGroupBox.setGeometry(QtCore.QRect(10, 150, 351, 121))
        self.capturingGroupBox.setObjectName("capturingGroupBox")
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(parent=self.capturingGroupBox)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(10, 30, 331, 82))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.recordButton = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recordButton.sizePolicy().hasHeightForWidth())
        self.recordButton.setSizePolicy(sizePolicy)
        self.recordButton.setText("")
        self.recordButton.setPixmap(QtGui.QPixmap("Assets/record button.png"))
        self.recordButton.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.recordButton.setObjectName("recordButton")
        self.horizontalLayout_9.addWidget(self.recordButton)
        self.stopButton = QtWidgets.QLabel(parent=self.horizontalLayoutWidget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        self.stopButton.setText("")
        self.stopButton.setPixmap(QtGui.QPixmap("Assets/stop button.png"))
        self.stopButton.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_9.addWidget(self.stopButton)
        self.scriptsGroupBox = QtWidgets.QGroupBox(parent=self.controlsGroupBox)
        self.scriptsGroupBox.setGeometry(QtCore.QRect(10, 280, 351, 315))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scriptsGroupBox.sizePolicy().hasHeightForWidth())
        self.scriptsGroupBox.setSizePolicy(sizePolicy)
        self.scriptsGroupBox.setObjectName("scriptsGroupBox")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(parent=self.scriptsGroupBox)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(10, 20, 331, 291))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.craftingCheckBox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.craftingCheckBox.sizePolicy().hasHeightForWidth())
        self.craftingCheckBox.setSizePolicy(sizePolicy)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Assets/table.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.craftingCheckBox.setIcon(icon6)
        self.craftingCheckBox.setIconSize(QtCore.QSize(50, 50))
        self.craftingCheckBox.setChecked(True)
        self.craftingCheckBox.setObjectName("craftingCheckBox")
        self.verticalLayout_4.addWidget(self.craftingCheckBox)
        self.buildingCheckBox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buildingCheckBox.sizePolicy().hasHeightForWidth())
        self.buildingCheckBox.setSizePolicy(sizePolicy)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("Assets/stairs.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.buildingCheckBox.setIcon(icon7)
        self.buildingCheckBox.setIconSize(QtCore.QSize(50, 50))
        self.buildingCheckBox.setChecked(True)
        self.buildingCheckBox.setObjectName("buildingCheckBox")
        self.verticalLayout_4.addWidget(self.buildingCheckBox)
        self.lightingCheckBox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lightingCheckBox.sizePolicy().hasHeightForWidth())
        self.lightingCheckBox.setSizePolicy(sizePolicy)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("Assets/torch.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.lightingCheckBox.setIcon(icon8)
        self.lightingCheckBox.setIconSize(QtCore.QSize(50, 50))
        self.lightingCheckBox.setChecked(True)
        self.lightingCheckBox.setObjectName("lightingCheckBox")
        self.verticalLayout_4.addWidget(self.lightingCheckBox)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.smeltingCheckBox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.smeltingCheckBox.sizePolicy().hasHeightForWidth())
        self.smeltingCheckBox.setSizePolicy(sizePolicy)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("Assets/furnace.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.smeltingCheckBox.setIcon(icon9)
        self.smeltingCheckBox.setIconSize(QtCore.QSize(50, 50))
        self.smeltingCheckBox.setChecked(True)
        self.smeltingCheckBox.setObjectName("smeltingCheckBox")
        self.verticalLayout_5.addWidget(self.smeltingCheckBox)
        self.weaponsCheckBox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.weaponsCheckBox.sizePolicy().hasHeightForWidth())
        self.weaponsCheckBox.setSizePolicy(sizePolicy)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("Assets/sword.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.weaponsCheckBox.setIcon(icon10)
        self.weaponsCheckBox.setIconSize(QtCore.QSize(50, 50))
        self.weaponsCheckBox.setChecked(True)
        self.weaponsCheckBox.setObjectName("weaponsCheckBox")
        self.verticalLayout_5.addWidget(self.weaponsCheckBox)
        self.armorCheckBox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.armorCheckBox.sizePolicy().hasHeightForWidth())
        self.armorCheckBox.setSizePolicy(sizePolicy)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("Assets/boots.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.armorCheckBox.setIcon(icon11)
        self.armorCheckBox.setIconSize(QtCore.QSize(50, 50))
        self.armorCheckBox.setChecked(True)
        self.armorCheckBox.setObjectName("armorCheckBox")
        self.verticalLayout_5.addWidget(self.armorCheckBox)
        self.horizontalLayout_6.addLayout(self.verticalLayout_5)
        self.verticalLayout_7.addWidget(self.controlsGroupBox)
        self.horizontalLayout_7.addLayout(self.verticalLayout_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1154, 22))
        self.menubar.setObjectName("menubar")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ML4MC GUI"))
        self.goalInfoGroupBox.setTitle(_translate("MainWindow", "AI Goal"))
        self.goalProgressBar.setTitle(_translate("MainWindow", "Goal Progress"))
        self.goalSelectGroupbox.setTitle(_translate("MainWindow", "Goal Selection"))
        self.diamondRadio.setText(_translate("MainWindow", "Obtain\n"
"Diamond"))
        self.ironRadio.setText(_translate("MainWindow", "Obtain\n"
"Iron"))
        self.surviveRadio.setText(_translate("MainWindow", "Survive"))
        self.woodRadio.setText(_translate("MainWindow", "Gather\n"
"Wood"))
        self.stoneRadio.setText(_translate("MainWindow", "Gather\n"
"Stone"))
        self.combatRadio.setText(_translate("MainWindow", "Defeat\n"
"Enemies"))
        self.currentObjectiveLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Goal: <span style=\" font-weight:700;\">Obtain Diamond</span></p></body></html>"))
        self.loadEnvironmentButton.setText(_translate("MainWindow", "Load Environment"))
        self.loadModelButton.setText(_translate("MainWindow", "Load Model"))
        self.groupBox_AI_Stats.setTitle(_translate("MainWindow", "AI Stats"))
        self.healthValue.setText(_translate("MainWindow", "20"))
        self.hungerValueLabel.setText(_translate("MainWindow", "20"))
        self.xCoordLabel.setText(_translate("MainWindow", "X: N/A"))
        self.yCoordLabel.setText(_translate("MainWindow", "Y: N/A"))
        self.zCoordLabel.setText(_translate("MainWindow", "Z: N/A"))
        self.inventoryGroupBox.setTitle(_translate("MainWindow", "Inventory"))
        item = self.inventoryTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item 1"))
        item = self.inventoryTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Item 2"))
        item = self.inventoryTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Item 3"))
        item = self.inventoryTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Amount"))
        __sortingEnabled = self.inventoryTable.isSortingEnabled()
        self.inventoryTable.setSortingEnabled(False)
        item = self.inventoryTable.item(0, 0)
        item.setText(_translate("MainWindow", "64"))
        item = self.inventoryTable.item(1, 0)
        item.setText(_translate("MainWindow", "1"))
        item = self.inventoryTable.item(2, 0)
        item.setText(_translate("MainWindow", "16"))
        self.inventoryTable.setSortingEnabled(__sortingEnabled)
        self.stepsGroupBox.setTitle(_translate("MainWindow", "Steps Taken"))
        item = self.stepsTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Step 1"))
        item = self.stepsTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Step 2"))
        item = self.stepsTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Step 3"))
        item = self.stepsTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Step Taken"))
        __sortingEnabled = self.stepsTable.isSortingEnabled()
        self.stepsTable.setSortingEnabled(False)
        item = self.stepsTable.item(0, 0)
        item.setText(_translate("MainWindow", "Forward"))
        item = self.stepsTable.item(1, 0)
        item.setText(_translate("MainWindow", "Forward"))
        item = self.stepsTable.item(2, 0)
        item.setText(_translate("MainWindow", "Attack"))
        self.stepsTable.setSortingEnabled(__sortingEnabled)
        self.controlsGroupBox.setTitle(_translate("MainWindow", "AI Controls"))
        self.actionGroupBox.setTitle(_translate("MainWindow", "Action Controls"))
        self.capturingGroupBox.setTitle(_translate("MainWindow", "Interactor Capturing"))
        self.scriptsGroupBox.setTitle(_translate("MainWindow", "AI Scripts"))
        self.craftingCheckBox.setText(_translate("MainWindow", "Crafting"))
        self.buildingCheckBox.setText(_translate("MainWindow", "Building"))
        self.lightingCheckBox.setText(_translate("MainWindow", "Lighting"))
        self.smeltingCheckBox.setText(_translate("MainWindow", "Smelting"))
        self.weaponsCheckBox.setText(_translate("MainWindow", "Weapons"))
        self.armorCheckBox.setText(_translate("MainWindow", "Armor"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))

        self.loadEnvironmentButton.clicked.connect(self.load_environment)
        self.loadModelButton.clicked.connect(self.load_model)

        self.currentObjective = "Obtain Diamond"
        self.ironRadio.clicked.connect(partial(self.objective_clicked_callback, widget=self.ironRadio))
        self.woodRadio.clicked.connect(partial(self.objective_clicked_callback, widget=self.woodRadio))
        self.stoneRadio.clicked.connect(partial(self.objective_clicked_callback, widget=self.stoneRadio))
        self.combatRadio.clicked.connect(partial(self.objective_clicked_callback, widget=self.combatRadio))
        self.diamondRadio.clicked.connect(partial(self.objective_clicked_callback, widget=self.diamondRadio))
        self.surviveRadio.clicked.connect(partial(self.objective_clicked_callback, widget=self.surviveRadio))
        
        self.armorCheckBox.clicked.connect(partial(self.script_toggled_callback, widget=self.armorCheckBox))
        self.weaponsCheckBox.clicked.connect(partial(self.script_toggled_callback, widget=self.weaponsCheckBox))
        self.buildingCheckBox.clicked.connect(partial(self.script_toggled_callback, widget=self.buildingCheckBox))
        self.lightingCheckBox.clicked.connect(partial(self.script_toggled_callback, widget=self.lightingCheckBox))
        self.smeltingCheckBox.clicked.connect(partial(self.script_toggled_callback, widget=self.smeltingCheckBox))
        self.craftingCheckBox.clicked.connect(partial(self.script_toggled_callback, widget=self.craftingCheckBox))

        self.loadedEnvironment = ""

    def objective_clicked_callback(self, widget):
        """
            Description: Callback function that updates the selected AI objective and relevant UI elements.
            Inputs:
                widget - The GUI element that triggered the event.
            Output: None
        """
        newObjective = widget.text().replace('\n', ' ')
        if newObjective != self.currentObjective:
            # Different objective selected
            self.currentObjective = newObjective
            OBJECTIVE_QUEUE.put(self.currentObjective)
            print(f"Changed objective to {self.currentObjective}")
            for radio in [self.ironRadio, self.woodRadio, self.stoneRadio, self.combatRadio, self.diamondRadio, self.surviveRadio]:
                plainFont = QtGui.QFont()
                radio.setFont(plainFont)
                radio.setEnabled(True)
            boldFont = QtGui.QFont()
            boldFont.setBold(True)
            widget.setFont(boldFont)
            widget.setEnabled(False)
            if self.currentObjective == self.loadedEnvironment:
                self.loadEnvironmentButton.setEnabled(False)
            else:
                self.loadEnvironmentButton.setEnabled(True)
        else:
            print("Objective already selected.")

    def script_toggled_callback(self, state, widget):
        """
            Description: Callback function that toggles scripts and updates relevant UI elements.
            Inputs:
                widget - The GUI element that triggered the event and should be toggled.
            Output: None
        """
        scriptToggled = widget.text().replace('\n', ' ')
        if state:
            plainFont = QtGui.QFont()
            widget.setFont(plainFont)
            print(scriptToggled + " scripts toggled on.")

            # Do something to turn functionality on.
        else:
            strikeFont = QtGui.QFont()
            strikeFont.setStrikeOut(True)
            widget.setFont(strikeFont)
            print(scriptToggled + " scripts toggled off.")

            # Do something to turn functionality off.

    def load_environment(self):
        """
            Description:
                Function to load the custom ML4MC environment. Will not load
                reload the environment if the selected objective's environment
                is already loaded.
        """
        if self.loadedEnvironment != self.currentObjective:
            self.loadedEnvironment = self.currentObjective
            self.loadEnvironmentButton.setEnabled(False)
            print(f"Loading environment for {self.currentObjective}")
            BACKEND_PROCESS.start()
        else:
            print(f"Environment for {self.currentObjective} is already running.")
    
    def load_model(self):
        """
            Description:
                Function to load the model for the target objective.
        """
        try:
            AI_CONTROLLER.load_model(self.currentObjective)
            self.progressBar.setValue(0)
            self.currentObjectiveLabel.setText(f"Goal: <b>{self.currentObjective}</b>")
            self.currentObjectiveLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        except:
            print("TODO: Implement error window for invalid action.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    exit_code = app.exec()
    print("Exiting...")
    BACKEND_PROCESS.terminate()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
