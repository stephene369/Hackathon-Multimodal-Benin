from .lib import * 


class SubtitleWidget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.VBox = QVBoxLayout(self)

        setFont(self.label, 28)
        self.setObjectName(text.replace(' ', '-'))

        self.initUi()
        self.initConnection()


    def initUi(self) : 

        ### Fame 1 
        self.frame1 = QFrame(self)

        self.frame1_hox = QHBoxLayout(self.frame1)
        self.frame1_hox.addWidget(self.label)
        
        ### Frame 2 
        self.frame2 = QFrame(self)

            ## label 1 : 
        #self.frame2lab1  = SubtitleLabel(self.frame2)
        #setFont(self.frame2lab1 , 20)
        
            ### button
        self.frame2Button = PushButton("Importer une video" , self.frame2 , FIF.DOWNLOAD )
    

        self.frame2_hbox = QHBoxLayout(self.frame2)
        self.frame2_hbox.addWidget(self.frame2Button)


        #### HBOX 
        self.VBox.addWidget(self.frame1 )#, 0 , Qt.AlignmentFlag.AlignTop)
        self.VBox.addWidget(self.frame2, 1, Qt.AlignmentFlag.AlignCenter )#,  0 , Qt.AlignmentFlag.AlignTop)
        

    def initConnection(self) : 
        self.frame2Button.clicked.connect(self.openFileDialog)


    def onButtonClicked(self , message):

        if self.stateTooltip:
            self.stateTooltip.setContent('Operation terminee')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip('En cours', 'Veuillez patienter, ceci peut prendre un moment.', self)
            self.stateTooltip.move(510, 30)
            self.stateTooltip.show()

    def openFileDialog(self , parent):
        from .gen import Worker
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        fileName, _ = QFileDialog.getOpenFileName(self, "Choisir un fichier vidéo", "", "Fichiers vidéo (*.mp4 *.avi *.mov *.mkv);;Tous les fichiers (*)", options=options)
        if fileName:
            self.frame2Button.setEnabled(False)
            self.stateTooltip = None
            self.onButtonClicked(True)
            work = Worker(filename=fileName)
            work.finished.connect(self.onButtonClicked)
            work.run()

            
