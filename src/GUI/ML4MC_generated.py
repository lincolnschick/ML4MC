# Form implementation generated from reading ui file 'ML4MC.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1140, 703)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(9, 9, 1131, 651))
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
        self.progressBar.setProperty("value", 0)
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
        self.ironRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        self.ironRadio.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Assets/iron.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.ironRadio.setIcon(icon)
        self.ironRadio.setIconSize(QtCore.QSize(50, 50))
        self.ironRadio.setChecked(True)
        self.ironRadio.setObjectName("ironRadio")
        self.verticalLayout.addWidget(self.ironRadio)
        self.surviveRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Assets/bed.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.surviveRadio.setIcon(icon1)
        self.surviveRadio.setIconSize(QtCore.QSize(50, 50))
        self.surviveRadio.setObjectName("surviveRadio")
        self.verticalLayout.addWidget(self.surviveRadio)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.woodRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Assets/log.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.woodRadio.setIcon(icon2)
        self.woodRadio.setIconSize(QtCore.QSize(50, 50))
        self.woodRadio.setObjectName("woodRadio")
        self.verticalLayout_2.addWidget(self.woodRadio)
        self.combatRadio = QtWidgets.QRadioButton(parent=self.horizontalLayoutWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Assets/hostiles.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.combatRadio.setIcon(icon3)
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
        self.resetEnvironmentButton = QtWidgets.QPushButton(parent=self.goalInfoGroupBox)
        self.resetEnvironmentButton.setEnabled(False)
        self.resetEnvironmentButton.setGeometry(QtCore.QRect(10, 590, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.resetEnvironmentButton.setFont(font)
        self.resetEnvironmentButton.setObjectName("resetEnvironmentButton")
        self.agentButton = QtWidgets.QPushButton(parent=self.goalInfoGroupBox)
        self.agentButton.setGeometry(QtCore.QRect(10, 530, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.agentButton.setFont(font)
        self.agentButton.setObjectName("agentButton")
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.goalInfoGroupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 460, 351, 61))
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayoutWidget_9 = QtWidgets.QWidget(parent=self.groupBox_3)
        self.horizontalLayoutWidget_9.setGeometry(QtCore.QRect(10, 30, 331, 22))
        self.horizontalLayoutWidget_9.setObjectName("horizontalLayoutWidget_9")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_9)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.agentCheckbox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_9)
        self.agentCheckbox.setChecked(True)
        self.agentCheckbox.setObjectName("agentCheckbox")
        self.horizontalLayout_13.addWidget(self.agentCheckbox)
        self.interactorCheckbox = QtWidgets.QCheckBox(parent=self.horizontalLayoutWidget_9)
        self.interactorCheckbox.setChecked(False)
        self.interactorCheckbox.setObjectName("interactorCheckbox")
        self.horizontalLayout_13.addWidget(self.interactorCheckbox)
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
        self.healthLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.healthLabel.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.healthLabel.setFont(font)
        self.healthLabel.setObjectName("healthLabel")
        self.horizontalLayout_5.addWidget(self.healthLabel)
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
        self.hungerLabel = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        self.hungerLabel.setMaximumSize(QtCore.QSize(50, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.hungerLabel.setFont(font)
        self.hungerLabel.setObjectName("hungerLabel")
        self.horizontalLayout_4.addWidget(self.hungerLabel)
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
        self.inventoryGroupBox.setGeometry(QtCore.QRect(10, 140, 351, 501))
        self.inventoryGroupBox.setObjectName("inventoryGroupBox")
        self.inventoryTable = QtWidgets.QTableWidget(parent=self.inventoryGroupBox)
        self.inventoryTable.setGeometry(QtCore.QRect(10, 30, 331, 461))
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
        self.inventoryTable.setColumnCount(2)
        self.inventoryTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.inventoryTable.setHorizontalHeaderItem(1, item)
        self.inventoryTable.horizontalHeader().setCascadingSectionResizes(False)
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
        self.playButton.setEnabled(False)
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
        self.pauseButton.setEnabled(False)
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
        self.recordButton.setEnabled(False)
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
        self.stopButton.setEnabled(False)
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
        self.scriptsGroupBox.setGeometry(QtCore.QRect(10, 280, 351, 361))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scriptsGroupBox.sizePolicy().hasHeightForWidth())
        self.scriptsGroupBox.setSizePolicy(sizePolicy)
        self.scriptsGroupBox.setObjectName("scriptsGroupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.scriptsGroupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 19, 331, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(parent=self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 146, 271))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.diamondIcon = QtWidgets.QLabel(parent=self.layoutWidget)
        self.diamondIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.diamondIcon.setText("")
        self.diamondIcon.setPixmap(QtGui.QPixmap("Assets/diamond.png"))
        self.diamondIcon.setScaledContents(True)
        self.diamondIcon.setObjectName("diamondIcon")
        self.horizontalLayout_14.addWidget(self.diamondIcon)
        self.diamondScriptButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.diamondScriptButton.setEnabled(False)
        self.diamondScriptButton.setIconSize(QtCore.QSize(50, 50))
        self.diamondScriptButton.setObjectName("diamondScriptButton")
        self.horizontalLayout_14.addWidget(self.diamondScriptButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.stoneIcon = QtWidgets.QLabel(parent=self.layoutWidget)
        self.stoneIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.stoneIcon.setText("")
        self.stoneIcon.setPixmap(QtGui.QPixmap("Assets/cobble.png"))
        self.stoneIcon.setScaledContents(True)
        self.stoneIcon.setObjectName("stoneIcon")
        self.horizontalLayout_15.addWidget(self.stoneIcon)
        self.stoneScriptButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.stoneScriptButton.setEnabled(False)
        self.stoneScriptButton.setIconSize(QtCore.QSize(50, 50))
        self.stoneScriptButton.setObjectName("stoneScriptButton")
        self.horizontalLayout_15.addWidget(self.stoneScriptButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.script3Icon = QtWidgets.QLabel(parent=self.layoutWidget)
        self.script3Icon.setEnabled(False)
        self.script3Icon.setMaximumSize(QtCore.QSize(50, 50))
        self.script3Icon.setText("")
        self.script3Icon.setPixmap(QtGui.QPixmap("Assets/table.png"))
        self.script3Icon.setScaledContents(True)
        self.script3Icon.setObjectName("script3Icon")
        self.horizontalLayout_16.addWidget(self.script3Icon)
        self.script3Button = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.script3Button.setEnabled(False)
        self.script3Button.setIconSize(QtCore.QSize(50, 50))
        self.script3Button.setObjectName("script3Button")
        self.horizontalLayout_16.addWidget(self.script3Button)
        self.verticalLayout_4.addLayout(self.horizontalLayout_16)
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.verticalLayoutWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 151, 271))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.surfaceIcon = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.surfaceIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.surfaceIcon.setText("")
        self.surfaceIcon.setPixmap(QtGui.QPixmap("Assets/Cobblestone_Stairs_(N)_JE6_BE6.webp"))
        self.surfaceIcon.setScaledContents(True)
        self.surfaceIcon.setObjectName("surfaceIcon")
        self.horizontalLayout_10.addWidget(self.surfaceIcon)
        self.surfaceScriptButton = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.surfaceScriptButton.setEnabled(False)
        self.surfaceScriptButton.setIconSize(QtCore.QSize(50, 50))
        self.surfaceScriptButton.setObjectName("surfaceScriptButton")
        self.horizontalLayout_10.addWidget(self.surfaceScriptButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.depthIcon = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.depthIcon.setMaximumSize(QtCore.QSize(50, 50))
        self.depthIcon.setText("")
        self.depthIcon.setPixmap(QtGui.QPixmap("Assets/iron_pickaxe.webp"))
        self.depthIcon.setScaledContents(True)
        self.depthIcon.setObjectName("depthIcon")
        self.horizontalLayout_11.addWidget(self.depthIcon)
        self.depthScriptButton = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.depthScriptButton.setEnabled(False)
        self.depthScriptButton.setIconSize(QtCore.QSize(50, 50))
        self.depthScriptButton.setObjectName("depthScriptButton")
        self.horizontalLayout_11.addWidget(self.depthScriptButton)
        self.verticalLayout_5.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.script6Icon = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.script6Icon.setEnabled(False)
        self.script6Icon.setMaximumSize(QtCore.QSize(50, 50))
        self.script6Icon.setText("")
        self.script6Icon.setPixmap(QtGui.QPixmap("Assets/torch.png"))
        self.script6Icon.setScaledContents(True)
        self.script6Icon.setObjectName("script6Icon")
        self.horizontalLayout_12.addWidget(self.script6Icon)
        self.script6Button = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.script6Button.setEnabled(False)
        self.script6Button.setIconSize(QtCore.QSize(50, 50))
        self.script6Button.setObjectName("script6Button")
        self.horizontalLayout_12.addWidget(self.script6Button)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_6.addWidget(self.groupBox_2)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.stopScriptButton = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.stopScriptButton.setEnabled(False)
        self.stopScriptButton.setObjectName("stopScriptButton")
        self.verticalLayout_9.addWidget(self.stopScriptButton)
        self.verticalLayout_7.addWidget(self.controlsGroupBox)
        self.horizontalLayout_7.addLayout(self.verticalLayout_7)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1140, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ML4MC GUI"))
        self.goalInfoGroupBox.setTitle(_translate("MainWindow", "AI Goal"))
        self.goalProgressBar.setTitle(_translate("MainWindow", "Goal Progress"))
        self.goalSelectGroupbox.setTitle(_translate("MainWindow", "Change Objective"))
        self.ironRadio.setText(_translate("MainWindow", "  Obtain\n"
"  Iron"))
        self.surviveRadio.setText(_translate("MainWindow", "  Survive"))
        self.woodRadio.setText(_translate("MainWindow", "Gather\n"
"Wood"))
        self.combatRadio.setText(_translate("MainWindow", "Defeat\n"
"Enemies"))
        self.currentObjectiveLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Goal: <span style=\" font-weight:700;\">Obtain Iron</span></p></body></html>"))
        self.resetEnvironmentButton.setText(_translate("MainWindow", "Reset Environment"))
        self.agentButton.setText(_translate("MainWindow", "Start Agent"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Start / Reset Options"))
        self.agentCheckbox.setText(_translate("MainWindow", "Load Agent POV on Start"))
        self.interactorCheckbox.setText(_translate("MainWindow", "Load Interactor on Start"))
        self.groupBox_AI_Stats.setTitle(_translate("MainWindow", "AI Stats"))
        self.healthLabel.setText(_translate("MainWindow", "N/A"))
        self.hungerLabel.setText(_translate("MainWindow", "N/A"))
        self.xCoordLabel.setText(_translate("MainWindow", "X: N/A"))
        self.yCoordLabel.setText(_translate("MainWindow", "Y: N/A"))
        self.zCoordLabel.setText(_translate("MainWindow", "Z: N/A"))
        self.inventoryGroupBox.setTitle(_translate("MainWindow", "Inventory"))
        item = self.inventoryTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Item"))
        item = self.inventoryTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Amount"))
        self.controlsGroupBox.setTitle(_translate("MainWindow", "AI Controls"))
        self.actionGroupBox.setTitle(_translate("MainWindow", "Action Controls"))
        self.capturingGroupBox.setTitle(_translate("MainWindow", "Screen Capturing"))
        self.scriptsGroupBox.setTitle(_translate("MainWindow", "AI Scripts"))
        self.groupBox.setTitle(_translate("MainWindow", "Continuous"))
        self.diamondScriptButton.setText(_translate("MainWindow", "Collect\n"
"Diamond"))
        self.stoneScriptButton.setText(_translate("MainWindow", "Gather\n"
"Stone"))
        self.script3Button.setText(_translate("MainWindow", "Placeholder\n"
"Text"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Execute Once"))
        self.surfaceScriptButton.setText(_translate("MainWindow", "Mine\n"
"to Surface"))
        self.depthScriptButton.setText(_translate("MainWindow", "Dig\n"
"to Depth"))
        self.script6Button.setText(_translate("MainWindow", "Placeholder\n"
"Text"))
        self.stopScriptButton.setText(_translate("MainWindow", "Stop Script"))
