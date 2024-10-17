import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
    QMessageBox, QFileDialog, QSlider, QComboBox, QApplication, QSizePolicy, QColorDialog
)
from PyQt5.QtGui import QPixmap, QIcon
from penstate import PenState
from canvas import Canvas
from imageOperations import ImageProcessor
from undoRedoManager import UndoRedoManager
from classHelpDialog import CustomDialog


def show_help_dialog():
    dialog = CustomDialog()
    dialog.exec_()


class UX(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 900, 900)

        self.sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # class members
        self.canvas = Canvas()
        self.undoRedoManager = UndoRedoManager()
        self.imageProcessor = ImageProcessor()

        self.noBrightnessModificationImage = None

        self.hiddenImageOperations = 0
        self.hiddenPainting = 0
        self.lightDarkMode = 0

        self.menubar = self.menuBar()
        self.horizontalLayout = QVBoxLayout()

        self.centralWidget = QWidget()

        self.undoButton = QPushButton("Undo\t(Ctrl+Z)", self.centralWidget)
        self.redoButton = QPushButton("Redo\t(Ctrl+Y)", self.centralWidget)

        self.averageFilterButton = QPushButton("Average Filter", self.centralWidget)
        self.medianFilterButton = QPushButton("Median Filter", self.centralWidget)
        self.gaussianFilterButton = QPushButton("Gaussian Filter", self.centralWidget)
        self.grayScaleButton = QPushButton("Gray Scale", self.centralWidget)

        self.brushButton = QPushButton(" Brush", self.centralWidget)
        self.sprayButton = QPushButton(" Spray", self.centralWidget)
        self.penButton = QPushButton(" Pen", self.centralWidget)
        self.fillButton = QPushButton(" Fill", self.centralWidget)
        self.rectangleButton = QPushButton(" Rectangle", self.centralWidget)
        self.circleButton = QPushButton(" Circle", self.centralWidget)

        self.colorButton = QPushButton('Choose Color', self)

        self.canvasLayout = QVBoxLayout()

        self.canvasTextLabel = QLabel("Canvas")
        self.canvasTextLabel.setAlignment(Qt.AlignCenter)

        self.colorLabel = QLabel()
        self.widthSliderLabel = QLabel("Width Size: 1")

        self.brightnessLabel = QLabel('Brightness Value: 0')
        self.filterComboBoxLabel = QLabel('Filter Size')

        self.brightnessSlider = QSlider(Qt.Horizontal)
        self.widthSlider = QSlider(Qt.Horizontal)

        self.filterComboBox = QComboBox(self)

        self.mainLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.undoRedoButtonLayout = QHBoxLayout()
        self.filterButtonLayout = QHBoxLayout()
        self.filterSizeLayout = QVBoxLayout()
        self.brightnessWidgetsLayout = QVBoxLayout()
        self.paintButtonsLayout = QVBoxLayout()
        self.colorSettingLayout = QVBoxLayout()
        self.widthSettingLayout = QVBoxLayout()
        self.centerLayout = QHBoxLayout()

        # initializations
        self.initUndoRedoButtonsAndLayout()
        self.initFilterButtonsAndLayout()

        self.buttonLayout.addWidget(self.grayScaleButton)

        self.initBrightnessSlider()

        self.initPaintWidgets()

        self.mainLayout.addLayout(self.buttonLayout)

        self.centerLayout.addLayout(self.paintButtonsLayout)

        self.canvasLayout.addWidget(self.canvasTextLabel)
        self.canvasLayout.addWidget(self.canvas)
        self.centerLayout.addLayout(self.canvasLayout)

        self.mainLayout.addLayout(self.centerLayout)

        self.centralWidget.setLayout(self.mainLayout)

        self.setCentralWidget(self.centralWidget)

        self.setStyleOfWidgets()

        self.connectWidgets()

        self.fileMenu()
        self.viewMenu()
        self.helpMenu()

    def initUndoRedoButtonsAndLayout(self):
        self.undoButton.setDisabled(True)
        self.redoButton.setDisabled(True)

        self.undoRedoButtonLayout.addWidget(self.undoButton)
        self.undoRedoButtonLayout.addWidget(self.redoButton)
        self.buttonLayout.addLayout(self.undoRedoButtonLayout)

    def initFilterButtonsAndLayout(self):
        self.filterButtonLayout.addWidget(self.averageFilterButton)
        self.filterButtonLayout.addWidget(self.medianFilterButton)
        self.filterButtonLayout.addWidget(self.gaussianFilterButton)

        self.filterComboBox.addItem("3")
        self.filterComboBox.addItem("5")
        self.filterComboBox.addItem("7")
        self.filterComboBox.addItem("9")
        self.filterComboBox.addItem("11")
        self.filterComboBox.addItem("13")
        self.filterComboBox.addItem("15")

        self.filterSizeLayout.addWidget(self.filterComboBoxLabel)
        self.filterSizeLayout.addWidget(self.filterComboBox)
        self.filterButtonLayout.addLayout(self.filterSizeLayout)

        self.buttonLayout.addLayout(self.filterButtonLayout)

    def initBrightnessSlider(self):
        self.brightnessSlider.setMinimum(-100)
        self.brightnessSlider.setMaximum(100)
        self.brightnessSlider.setSingleStep(1)
        self.brightnessSlider.setValue(0)

        self.brightnessSlider.setMaximumSize(140, 20)
        self.brightnessLabel.setMaximumSize(140, 20)

        self.brightnessWidgetsLayout.addWidget(self.brightnessLabel)
        self.brightnessWidgetsLayout.addWidget(self.brightnessSlider)

        self.buttonLayout.addLayout(self.brightnessWidgetsLayout)

    def initPaintWidgets(self):
        self.setupPaintingButtons(self.brushButton, "brush.png")
        self.setupPaintingButtons(self.sprayButton, "spray.png")
        self.setupPaintingButtons(self.penButton, "pencil.png")
        self.setupPaintingButtons(self.fillButton, "fill.png")
        self.setupPaintingButtons(self.rectangleButton, "square.png")
        self.setupPaintingButtons(self.circleButton, "circle.png")

        self.colorButton.setGeometry(10, 10, 150, 30)
        self.colorLabel.setGeometry(10, 50, 150, 150)
        self.colorLabel.setStyleSheet("background-color: white;")

        self.colorSettingLayout.addWidget(self.colorButton)
        self.colorSettingLayout.addWidget(self.colorLabel)
        self.paintButtonsLayout.addLayout(self.colorSettingLayout)

        self.widthSlider.setRange(1, 35)

        self.widthSettingLayout.addWidget(self.widthSliderLabel)
        self.widthSettingLayout.addWidget(self.widthSlider)
        self.paintButtonsLayout.addLayout(self.widthSettingLayout)

    def setupPaintingButtons(self, button, imageName):
        button.setFixedWidth(150)
        originalPixmap = QPixmap(f"Resurse/Icons/{imageName}")
        desiredSize = (32, 32)
        pixmap = originalPixmap.scaled(*desiredSize)
        icon = QIcon(pixmap)
        button.setIcon(icon)
        button.setIconSize(pixmap.size())
        self.paintButtonsLayout.addWidget(button)

    def setStyleOfWidgets(self):
        self.setStyleSheet("")

        borderStyle = "border: 2px solid black;"
        self.canvas.setStyleSheet(borderStyle)
        self.colorLabel.setStyleSheet(borderStyle)
        self.colorLabel.setMaximumHeight(50)
        self.widthSliderLabel.setMaximumHeight(50)

        self.canvasTextLabel.setSizePolicy(self.sizePolicy)

        filePath = 'Resurse/Stylesheets/stylesheet.txt'
        try:
            with open(filePath, 'r') as file:
                fileContents = file.read()

            self.setStyleSheet(fileContents)

        except Exception as e:
            print(f"Error reading or applying stylesheet: {e}")

        self.filterButtonLayout.setContentsMargins(15, 10, 15, 10)
        self.brightnessWidgetsLayout.setContentsMargins(15, 0, 15, 0)

        self.widthSlider.setFixedSize(150, self.widthSlider.sizeHint().height())

    def connectWidgets(self):
        self.undoButton.clicked.connect(self.undo)
        self.redoButton.clicked.connect(self.redo)

        self.averageFilterButton.clicked.connect(self.onAverageFilterButtonPressed)
        self.medianFilterButton.clicked.connect(self.onMedianFilterButtonPressed)
        self.gaussianFilterButton.clicked.connect(self.onGaussianFilterButtonPressed)
        self.filterComboBox.currentIndexChanged.connect(self.onComboIndexChanged)
        self.grayScaleButton.clicked.connect(self.imageToGrayScale)
        self.brightnessSlider.valueChanged.connect(self.brightnessSliderValueChanged)

        self.colorButton.clicked.connect(self.showColorDialog)

        self.brushButton.clicked.connect(self.onBrush)
        self.sprayButton.clicked.connect(self.onSpray)
        self.fillButton.clicked.connect(self.onFill)
        self.penButton.clicked.connect(self.onPen)
        self.rectangleButton.clicked.connect(self.onRectangle)
        self.circleButton.clicked.connect(self.onCircle)
        self.widthSlider.valueChanged.connect(self.setSize)

    def fileMenu(self):
        fileMenu = self.menubar.addMenu('File')

        openAction = QAction('Open\t(Ctrl+O)', self)
        openAction.triggered.connect(self.openFile)
        fileMenu.addAction(openAction)

        saveAction = QAction('Save\t(Ctrl+S)', self)
        saveAction.triggered.connect(self.saveFile)
        fileMenu.addAction(saveAction)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.exitFile)
        fileMenu.addAction(exitAction)

    def viewMenu(self):
        viewMenu = self.menubar.addMenu('View')

        showHideImageOperationsMenuAction = QAction('Show/Hide Image Operations Menu', self)
        showHideImageOperationsMenuAction.triggered.connect(self.showHideImageOperationsMenu)
        viewMenu.addAction(showHideImageOperationsMenuAction)

        showHidePaintingMenuAction = QAction('Show/Hide Painting Menu', self)
        showHidePaintingMenuAction.triggered.connect(self.showHidePaintingMenu)
        viewMenu.addAction(showHidePaintingMenuAction)

        showHidePaintingMenuAction = QAction('Light/Dark Mode', self)
        showHidePaintingMenuAction.triggered.connect(self.changeLightDarkMode)
        viewMenu.addAction(showHidePaintingMenuAction)

    def helpMenu(self):
        helpMenu = self.menubar.addMenu('Help')

        helpAction = QAction('About', self)
        helpAction.triggered.connect(show_help_dialog)
        helpMenu.addAction(helpAction)

    def showHideImageOperationsMenu(self):
        if self.hiddenImageOperations == 0:
            self.redoButton.hide()
            self.undoButton.hide()
            self.averageFilterButton.hide()
            self.gaussianFilterButton.hide()
            self.filterComboBox.hide()
            self.filterComboBoxLabel.hide()
            self.medianFilterButton.hide()
            self.grayScaleButton.hide()
            self.brightnessLabel.hide()
            self.brightnessSlider.hide()

            self.hiddenImageOperations = 1

        elif self.hiddenImageOperations == 1:
            self.redoButton.setHidden(False)
            self.undoButton.setHidden(False)
            self.averageFilterButton.setHidden(False)
            self.gaussianFilterButton.setHidden(False)
            self.filterComboBox.setHidden(False)
            self.filterComboBoxLabel.setHidden(False)
            self.medianFilterButton.setHidden(False)
            self.grayScaleButton.setHidden(False)
            self.brightnessLabel.setHidden(False)
            self.brightnessSlider.setHidden(False)

            self.hiddenImageOperations = 0

    def showHidePaintingMenu(self):
        if self.hiddenPainting == 0:
            self.brushButton.hide()
            self.sprayButton.hide()
            self.penButton.hide()
            self.fillButton.hide()
            self.rectangleButton.hide()
            self.circleButton.hide()
            self.colorLabel.hide()
            self.colorButton.hide()
            self.widthSliderLabel.hide()
            self.widthSlider.hide()

            self.hiddenPainting = 1

        elif self.hiddenPainting == 1:
            self.brushButton.setHidden(False)
            self.sprayButton.setHidden(False)
            self.penButton.setHidden(False)
            self.fillButton.setHidden(False)
            self.rectangleButton.setHidden(False)
            self.circleButton.setHidden(False)
            self.colorLabel.setHidden(False)
            self.colorButton.setHidden(False)
            self.widthSliderLabel.setHidden(False)
            self.widthSlider.setHidden(False)

            self.hiddenPainting = 0

    def changeLightDarkMode(self):
        if self.lightDarkMode == 0:
            filePath = 'Resurse/Stylesheets/stylesheet2.txt'
            try:
                with open(filePath, 'r') as file:
                    fileContents = file.read()

                self.setStyleSheet(fileContents)

            except Exception as e:
                print(f"Error reading or applying stylesheet: {e}")

            self.lightDarkMode = 1

        elif self.lightDarkMode == 1:
            filePath = 'Resurse/Stylesheets/stylesheet.txt'
            try:
                with open(filePath, 'r') as file:
                    fileContents = file.read()

                self.setStyleSheet(fileContents)

            except Exception as e:
                print(f"Error reading or applying stylesheet: {e}")

            self.lightDarkMode = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
            self.openFile()
        if event.key() == Qt.Key_S and event.modifiers() == Qt.ControlModifier:
            self.saveFile()
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            if len(self.undoRedoManager.get_previous_states()) > 0:
                self.undo()
        if event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            if len(self.undoRedoManager.get_next_states()) > 0:
                self.redo()

    # Functions for connections
    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
                                                  "Image Files (*.jpg *.png *.bmp);;All Files (*)", options=options)

        if fileName:
            image = cv2.cvtColor(cv2.imread(fileName), cv2.COLOR_RGB2BGR)

            labelWidth = self.canvas.width()
            labelHeight = self.canvas.height()

            aspectRatio = image.shape[1] / image.shape[0]
            newWidth = labelWidth
            newHeight = int(labelWidth / aspectRatio)

            if newHeight > labelHeight:
                newHeight = labelHeight
                newWidth = int(labelHeight * aspectRatio)

            image = cv2.resize(image, (newWidth, newHeight))

            self.updatePixmap(self.imageProcessor.cvMatToQImage(image))

    def saveFile(self):
        if len(self.undoRedoManager.get_previous_states()) != 0:
            self.undoRedoManager.reset_next_images()
            self.undoRedoManager.reset_previous_states()

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileDialog = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png);;All Files (*)",
                                                 options=options)

        filePath, selected_filter = fileDialog

        if filePath:
            qImage = self.canvas.pixmap()

            qImage.save(filePath, "PNG", -1)

    def exitFile(self):
        if len(self.undoRedoManager.get_previous_states()) != 0:
            messageBox = QMessageBox()
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setWindowTitle("Save and Exit")
            messageBox.setText("Do you want to save the file before exiting?")
            messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            messageBox.setDefaultButton(QMessageBox.Yes)

            response = messageBox.exec_()

            if response == QMessageBox.Yes:
                self.saveFile()
        else:
            QApplication.quit()

    def closeEvent(self, event):
        self.exitFile()
        event.accept()

    def onComboIndexChanged(self):
        self.filterComboBox.currentText()

    def onAverageFilterButtonPressed(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            image = self.imageProcessor.applyAverageFilter(self.canvas.pixmap().toImage(), int(self.filterComboBox.currentText()))
            self.updatePixmap(image)

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None

        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onMedianFilterButtonPressed(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            image = self.imageProcessor.applyMedianFilter(self.canvas.pixmap().toImage(), int(self.filterComboBox.currentText()))
            self.updatePixmap(image)

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None

        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onGaussianFilterButtonPressed(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            image = self.imageProcessor.applyGaussianFilter(self.canvas.pixmap().toImage(), int(self.filterComboBox.currentText()))
            self.updatePixmap(image)

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None

        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def imageToGrayScale(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            image = self.imageProcessor.imageToGrayScale(self.canvas.pixmap().toImage())
            self.updatePixmap(image)

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None

        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def brightnessSliderValueChanged(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            self.brightnessLabel.setText(f'Brightness Value: {self.brightnessSlider.value()}')

            if self.noBrightnessModificationImage is None:
                self.noBrightnessModificationImage = self.canvas.pixmap().toImage()

            image = self.imageProcessor.changeBrightness(self.noBrightnessModificationImage, int(self.brightnessSlider.value()))

            self.updatePixmap(image)

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onSpray(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            self.canvas.penState = PenState.SPRAY

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onBrush(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            self.canvas.penState = PenState.BRUSH

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onPen(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            self.canvas.penState = PenState.NORMAL

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onFill(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            self.canvas.penState = PenState.FILL

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def setSize(self, value):
        try:
            self.canvas.pen_width = value

            self.widthSliderLabel.setText(f'Width Size: {self.widthSlider.value()}')

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onRectangle(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            self.canvas.penState = PenState.RECTANGLE

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def onCircle(self):
        try:
            self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                     self.widthSlider.value())

            self.canvas.penState = PenState.CIRCLE

            if not self.undoButton.isEnabled():
                self.undoButton.setEnabled(True)

            self.noBrightnessModificationImage = None
        except Exception as e:
            print(f"Error: {str(e)}")
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")

    def updatePixmap(self, qImage):
        pixmap = QPixmap.fromImage(qImage)
        self.canvas.setPixmap(pixmap)
        self.canvas.setAlignment(Qt.AlignTop)

    def showColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.colorLabel.setStyleSheet(f"background-color: {color.name()};")
            self.canvas.set_pen_color(color)

    def undo(self):
        if not self.redoButton.isEnabled():
            self.redoButton.setEnabled(True)

        if len(self.undoRedoManager.get_previous_states()) == 1:
            self.undoButton.setEnabled(False)

        self.undoRedoManager.add_next_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                             self.widthSlider.value())

        image, brightnessValue, widthValue = self.undoRedoManager.undo()
        self.canvas.setPixmap(QPixmap.fromImage(image))
        self.brightnessSlider.setValue(brightnessValue)
        self.widthSlider.setValue(widthValue)

    def redo(self):
        if len(self.undoRedoManager.get_next_states()) == 1:
            self.redoButton.setEnabled(False)

        self.undoRedoManager.add_previous_states(self.canvas.pixmap().toImage(), self.brightnessSlider.value(),
                                                 self.widthSlider.value())

        image, brightnessValue, widthValue = self.undoRedoManager.redo()
        self.canvas.setPixmap(QPixmap.fromImage(image))
        self.brightnessSlider.setValue(brightnessValue)
        self.widthSlider.setValue(widthValue)

        if not self.undoButton.isEnabled():
            self.undoButton.setEnabled(True)
