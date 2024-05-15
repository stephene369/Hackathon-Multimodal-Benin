from App import * 
from App.food import FoodWidget
from App.subtitle import SubtitleWidget
from App.voice import VoiceWidget


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.foodInterface = FoodWidget('Nourriture Beninoise :', self)
        self.subtitleInterface = SubtitleWidget('Generateur de sous titre :', self)
        self.voiceInterface = VoiceWidget('Reconnaissance vocal :', self)

        self.settingInterface = Widget('Parametre . ', self)


        self.initNavigation()
        self.initWindow()

        

    def initNavigation(self):


        self.addSubInterface(self.foodInterface, FIF.CAFE, 'Nourriture (Nùɖúɖú)')
        self.addSubInterface(self.subtitleInterface, QIcon("resources/subtitle.png"), 'Generateur de sous-titre')
        self.addSubInterface(self.voiceInterface, QIcon("resources/voice.jpg") , 'Reconnaissance Vocal')

        self.navigationInterface.addSeparator()

        #self.addSubInterface(self.albumInterface, FIF.ALBUM, 'Albums', NavigationItemPosition.SCROLL)
        #self.addSubInterface(self.albumInterface1, FIF.ALBUM, 'Album 1', parent=self.albumInterface)
        #self.addSubInterface(self.albumInterface1_1, FIF.ALBUM, 'Album 1.1', parent=self.albumInterface1)
        #self.addSubInterface(self.albumInterface2, FIF.ALBUM, 'Album 2', parent=self.albumInterface)
        #self.addSubInterface(self.folderInterface, FIF.FOLDER, 'Folder library', NavigationItemPosition.SCROLL)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('DrAgons', 'resource/shoko.png'),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM,
        )

        self.addSubInterface(self.settingInterface, FIF.SETTING, 'Settings', NavigationItemPosition.BOTTOM)

        # add badge to navigation item
        item = self.navigationInterface.widget(self.voiceInterface.objectName())
        InfoBadge.attension(
            text='',
            parent=item.parent(),
            target=item,
            position=InfoBadgePosition.NAVIGATION_ITEM
        )

        # NOTE: enable acrylic effect
        # self.navigationInterface.setAcrylicEnabled(True)


    def initWindow(self):
        self.resize(900, 700)
        #self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('DrAgons')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        # use custom background color theme (only available when the mica effect is disabled)
        self.setCustomBackgroundColor(*FluentBackgroundTheme.DEFAULT_BLUE)
        # self.setMicaEffectEnabled(False)

        # set the minimum window width that allows the navigation panel to be expanded
        # self.navigationInterface.setMinimumExpandWidth(900)
        # self.navigationInterface.expand(useAni=False)

    def showMessageBox(self):
        w = MessageBox(
            'DrAgons',
            'We are the best ',
            self
        )
        w.yesButton.setText('GitHub')
        w.cancelButton.setText('Cancel')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))




