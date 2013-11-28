import sys, os, random
from PySide.QtGui import *
from PySide.QtCore import *

try:
    from PySide.phonon import Phonon
except ImportError:
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "Music Player",
            "Your Qt installation does not have Phonon support.",
            QMessageBox.Ok | QMessageBox.Default,
            QMessageBox.NoButton)
    sys.exit(1)




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()


        self.media = Phonon.MediaObject(self)

        self.audio = Phonon.AudioOutput(Phonon.MusicCategory, self)
        self.video = Phonon.VideoWidget(self)
        self.metaInformationResolver = Phonon.MediaObject(self)

        Phonon.createPath(self.media, self.audio)
        Phonon.createPath(self.media, self.video)

        self.media.setTickInterval(1000)
        self.sources = []




        self.setupActions()
        self.setupConnections()
        self.setupUi()

        self.setWindowTitle("BLue PLayer")
        self.setMinimumSize(245,245)
        self.resize(680,400)


    def setupActions(self):
        self.playAction = QAction(QIcon('images/play.png'), self.tr("Play"), self)
        self.playAction.setShortcut(self.tr("SPACE"))
        self.playAction.setDisabled(True)

        self.pauseAction = QAction(QIcon('images/pause.png'), self.tr("Pause"), self)
        self.pauseAction.setShortcut(self.tr("SPACE"))
        self.pauseAction.setDisabled(True)

        self.stopAction = QAction(QIcon('images/stop.png'), self.tr("Stop"), self)
        self.stopAction.setShortcut(self.tr("Ctrl+S"))
        self.stopAction.setDisabled(True)

        self.nextAction = QAction(QIcon('images/next.png'), self.tr("Next"), self)
        self.nextAction.setShortcut(self.tr("Ctrl+LEFT"))

        self.previousAction = QAction(QIcon('images/previous.png'), self.tr("Previous"), self)
        self.previousAction.setShortcut(self.tr("Ctrl+RIGHT"))

        self.addFilesAction = QAction(QIcon('images/folder-add-2.png'), 'add file', self)
        self.addFilesAction.setShortcut(self.tr("Ctrl+O"))

        self.fullAction = QAction(QIcon('images/expand-2.png'), self.tr("full"), self)
        self.fullAction.setDisabled(True)

        self.playlistAcion = QAction(QIcon('images/list.png'), self.tr("Playlist"), self)

        self.repeatAction = QAction(QIcon('images/repeat.png'), self.tr("Repeat"), self)
        self.repeatAction.setCheckable(True)

        self.repeatListAction = QAction(QIcon('images/revert.png'), self.tr("Repeat List"), self)
        self.repeatListAction.setCheckable(True)

        self.shuffleAction = QAction(QIcon('images/shuffle.png'), self.tr("Repeat List"), self)
        self.shuffleAction.setCheckable(True)
        




    def setupConnections(self):

        self.connect(self.media, SIGNAL('tick(qint64)'),
                self.tick)
        self.connect(self.media,
                SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                self.stateChanged)
        self.connect(self.metaInformationResolver,
                SIGNAL('stateChanged(Phonon::State, Phonon::State)'),
                self.metaStateChanged)
        self.connect(self.media, SIGNAL('aboutToFinish()'),
                self.aboutToFinish)
        self.connect(self.media,
                SIGNAL('currentSourceChanged(Phonon::MediaSource)'),
                self.sourceChanged)



        self.connect(self.playAction, SIGNAL('triggered()'),
                self.media, SLOT('play()'))

        self.connect(self.pauseAction, SIGNAL('triggered()'),
                self.media, SLOT('pause()'))

        self.connect(self.stopAction, SIGNAL('triggered()'),
                self.media, SLOT('stop()'))

        self.connect(self.addFilesAction, SIGNAL('triggered()'),
                self.addFiles)

        self.connect(self.fullAction, SIGNAL('triggered()'),
                self.full)

        self.connect(self.playlistAcion, SIGNAL('triggered()'),
                self.showPlaylist)

        self.connect(self.nextAction, SIGNAL('triggered()'),
                self.nextSong)

        self.connect(self.previousAction, SIGNAL('triggered()'),
                self.prevSong)




    def addFiles(self):
        files,_ = QFileDialog.getOpenFileNames(self,
                  self.tr("Select Music Files"),
                  QDesktopServices.storageLocation(QDesktopServices.MusicLocation))

        if files=="":
            return

        index = len(self.sources)

        for string in files:
            self.sources.append(Phonon.MediaSource(string))

        if self.sources:
            self.metaInformationResolver.setCurrentSource(self.sources[index])

    
    def tick(self, time):
        displayTime = QTime(0, (time / 60000) % 60, (time / 1000) % 60)
        self.timeLcd.display(displayTime.toString('mm:ss'))

    def sourceChanged(self, source):
        self.playlistTable.selectRow(self.sources.index(source))
        self.timeLcd.display("00:00")

    def nextSong(self):
        if len(self.sources) > 1:
            if self.shuffleAction.isChecked():
                song = self.shuffleSong()
                self.media.setCurrentSource(song)
                self.media.play()

            else:
                index = self.sources.index(self.media.currentSource()) + 1
                if index == len(self.sources):
                    if self.repeatListAction.isChecked():
                        self.media.setCurrentSource(self.sources[0])
                        self.media.play()
                    else:
                        pass
                else:
                    self.media.setCurrentSource(self.sources[index])
                    self.media.play()
        else:
            pass

    

    def prevSong(self):
        lenSource = len(self.sources)
        if lenSource > 1:
            if self.shuffleAction.isChecked():
                song = self.shuffleSong()
                self.media.setCurrentSource(song)
                self.media.play()
            else:
                index = self.sources.index(self.media.currentSource()) - 1
                if index < 0:
                    if self.repeatListAction.isChecked():
                        self.media.setCurrentSource(self.sources[lenSource - 1 ])
                        self.media.play()
                    else:
                        pass
                else:
                    self.media.setCurrentSource(self.sources[index])
                    self.media.play()
        else:
            pass


    def shuffleSong(self):
        song = random.choice(self.sources)
        return song


    def stateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            if self.media.errorType() == Phonon.FatalError:
                QMessageBox.warning(self, self.tr("Fatal Error"),
                        self.media.errorString())
            else:
                QMessageBox.warning(self, self.tr("Error"),
                        self.media.errorString())

        elif newState == Phonon.PlayingState:
            self.playAction.setEnabled(False)
            self.pauseAction.setEnabled(True)
            self.stopAction.setEnabled(True)
            self.fullAction.setEnabled(True)

        elif newState == Phonon.StoppedState:
            self.stopAction.setEnabled(False)
            self.playAction.setEnabled(True)
            self.pauseAction.setEnabled(False)
            self.fullAction.setEnabled(False)
            self.timeLcd.display("00:00")

        elif newState == Phonon.PausedState:
            self.pauseAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.playAction.setEnabled(True)
            self.fullAction.setEnabled(True)

    
    def tableClicked(self, row, column):
        oldState = self.media.state()

        self.media.stop()
        self.media.clearQueue()

        self.media.setCurrentSource(self.sources[row])

        
        self.media.play()


    def full(self):
        if self.isFullScreen():
            self.playlistWidget.show()
            # self.widget.setWindowFlags(Qt.Window)
            self.widget.setWindowState(Qt.WindowNoState)
            self.widget.setVisible(True)
            self.widget.showNormal()
            self.showNormal()
        else: 
            self.playlistWidget.hide()
            # self.widget.setWindowFlags(Qt.Window)
            self.widget.setWindowState(Qt.WindowFullScreen)
            self.widget.setVisible(True)
            self.showFullScreen()


    def aboutToFinish(self):
        if not self.repeatAction.isChecked():
            index = self.sources.index(self.media.currentSource()) + 1
            if len(self.sources) > index:
                self.media.enqueue(self.sources[index])

        else:
            if self.shuffleAction.isChecked():
                song = self.shuffleSong()
                self.media.enqueue(song)
            else:
                index = self.sources.index(self.media.currentSource())
                self.media.enqueue(self.sources[index])

            


    def showPlaylist(self):
        if self.playlistWidget.isVisible() :
            self.playlistWidget.hide()  
        else:
            self.playlistWidget.show()



    def metaStateChanged(self, newState, oldState):
        if newState == Phonon.ErrorState:
            QMessageBox.warning(self, self.tr("Error opening files"),
                    self.metaInformationResolver.errorString())

            while self.sources and self.sources.pop() != self.metaInformationResolver.currentSource():
                pass

            return

        if newState != Phonon.StoppedState and newState != Phonon.PausedState:
            return

        if self.metaInformationResolver.currentSource().type() == Phonon.MediaSource.Invalid:
            return

        metaData = self.metaInformationResolver.metaData()

        
        title = self.metaInformationResolver.currentSource().fileName()
        title = os.path.basename(title)

        titleItem = QTableWidgetItem(title)
        titleItem.setFlags(titleItem.flags() ^ Qt.ItemIsEditable)

        artist = metaData.get('ARTIST', [""])[0]
        artistItem = QTableWidgetItem(artist)
        artistItem.setFlags(artistItem.flags() ^ Qt.ItemIsEditable)

        
        currentRow = self.playlistTable.rowCount()
        self.playlistTable.insertRow(currentRow)
        self.playlistTable.setItem(currentRow, 0, titleItem)
        self.playlistTable.setItem(currentRow, 1, artistItem)

        if not self.playlistTable.selectedItems():
            self.playlistTable.selectRow(0)
            self.media.setCurrentSource(self.metaInformationResolver.currentSource())

        source = self.metaInformationResolver.currentSource()
        index = self.sources.index(self.metaInformationResolver.currentSource()) + 1

        if len(self.sources) > index:
            self.metaInformationResolver.setCurrentSource(self.sources[index])
        else:
            self.playlistTable.resizeColumnsToContents()
            if self.playlistTable.columnWidth(0) > 300:
                self.playlistTable.setColumnWidth(0, 300)


    
    def setupUi(self):

        styles = """
          QSlider::groove:horizontal {
             background: red;
             position: absolute; /* absolutely position 4px from the left and right of the widget. setting margins on the widget should work too... */
             left: 4px; right: 4px;
             height:4px;
         }

         QSlider::handle:horizontal {
             height: 6px;
             width: 6px;
             background: red;
             
             border-radius: 100px;
         }

         QSlider::add-page:horizontal {
             background: white;
         }

         QSlider::sub-page:horizontal {
             background: skyblue;
         }
        """

        self.seekSlider = Phonon.SeekSlider(self.media, self)
        self.seekSlider.setStyleSheet(styles)
        self.volumeSlider = Phonon.VolumeSlider(self.audio)

        palette = QPalette()
        palette.setBrush(QPalette.Dark, Qt.lightGray)

        self.timeLcd = QLCDNumber()
        self.timeLcd.setPalette(palette)


        headers = [self.tr("Title"), self.tr("Duration")]

        self.playlistTable = QTableWidget(0, 2)
        self.playlistTable.setHorizontalHeaderLabels(headers)
        self.playlistTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.playlistTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.playlistTable.setStyleSheet('background-color: #ffffff; color: #000000')
        self.playlistTable.setMinimumWidth(250)


        self.connect(self.playlistTable, SIGNAL('cellPressed(int, int)'),
                self.tableClicked)

        playlistBar = QToolBar()
        playlistBar.addAction(self.addFilesAction)
        playlistBar.addAction(self.repeatListAction)
        playlistBar.addAction(self.shuffleAction)
        playlistBar.addAction(self.previousAction)
        playlistBar.addAction(self.nextAction)
        playlistBar.setStyleSheet('QToolBar{border-color:#cccccc;}QToolButton:checked{background-color:blue}')

        playlistLayout = QVBoxLayout()
        playlistLayout.addWidget(self.playlistTable)
        playlistLayout.addWidget(playlistBar)
        
        self.playlistWidget = QWidget()
        self.playlistWidget.setLayout(playlistLayout)


        bar = QToolBar()
        bar.addAction(self.playAction)
        bar.addAction(self.pauseAction)
        bar.addAction(self.stopAction)
        bar.addAction(self.fullAction)
        bar.addAction(self.repeatAction)
        bar.setStyleSheet('QToolBar{border-color:#cccccc;}QToolButton:checked{background-color:blue}')

        listbar = QToolBar()
        listbar.addAction(self.addFilesAction)
        listbar.addAction(self.playlistAcion)

        listbar.setStyleSheet('QToolBar {border-color:#cccccc;}')


        self.video.setMinimumWidth(400)

        videoLayout = QHBoxLayout()
        videoLayout.addWidget(self.video)
        videoLayout.addWidget(self.playlistWidget)


        seekerLayout = QHBoxLayout()
        seekerLayout.addWidget(self.seekSlider)
        seekerLayout.addWidget(self.timeLcd)

        playbackLayout = QHBoxLayout()
        playbackLayout.addWidget(bar)
        playbackLayout.addStretch()
        playbackLayout.addWidget(listbar)
        playbackLayout.addWidget(self.volumeSlider)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(videoLayout)
        mainLayout.addLayout(seekerLayout)
        mainLayout.addLayout(playbackLayout)

        self.widget = QWidget()
        self.widget.setLayout(mainLayout)
        self.widget.setStyleSheet('background-color: #000000;')
        self.widget.setMinimumWidth(200)



        self.setCentralWidget(self.widget)
        self.setStyleSheet('background-color: #000000;')




if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())