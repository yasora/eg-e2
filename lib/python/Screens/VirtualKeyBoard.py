# Embedded file name: /usr/lib/enigma2/python/Screens/VirtualKeyBoard.py
from enigma import eListboxPythonMultiContent, gFont, RT_HALIGN_CENTER, RT_VALIGN_CENTER, getPrevAsciiCode
from Screens.Screen import Screen
from Components.Language import language
from Components.ActionMap import NumberActionMap
from Components.Sources.StaticText import StaticText
from Components.Input import Input
from Components.Label import Label
from Components.MenuList import MenuList
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
from Tools.Directories import resolveFilename, SCOPE_ACTIVE_SKIN
from Tools.LoadPixmap import LoadPixmap
from Tools.NumericalTextInput import NumericalTextInput
import skin

class VirtualKeyBoardList(MenuList):

    def __init__(self, list, enableWrapAround = False):
        MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
        font = skin.fonts.get('VirtualKeyboard', ('Regular', 28, 45))
        self.l.setFont(0, gFont(font[0], font[1]))
        self.l.setItemHeight(font[2])


class VirtualKeyBoardEntryComponent:

    def __init__(self):
        pass


class VirtualKeyBoard(Screen):

    def __init__(self, session, title = '', **kwargs):
        Screen.__init__(self, session)
        self.setTitle(_(title))
        self.keys_list = []
        self.shiftkeys_list = []
        self.lang = language.getLanguage()
        self.nextLang = None
        self.shiftMode = False
        self.selectedKey = 0
        self.smsChar = None
        self.sms = NumericalTextInput(self.smsOK)
        self.key_bg = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_bg.png'))
        self.key_sel = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_sel.png'))
        self.key_backspace = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_backspace.png'))
        self.key_all = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_all.png'))
        self.key_clr = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_clr.png'))
        self.key_esc = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_esc.png'))
        self.key_ok = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_ok.png'))
        self.key_shift = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_shift.png'))
        self.key_shift_sel = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_shift_sel.png'))
        self.key_space = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_space.png'))
        self.key_left = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_left.png'))
        self.key_right = LoadPixmap(path=resolveFilename(SCOPE_ACTIVE_SKIN, 'buttons/vkey_right.png'))
        self.keyImages = {'BACKSPACE': self.key_backspace,
         'ALL': self.key_all,
         'EXIT': self.key_esc,
         'OK': self.key_ok,
         'SHIFT': self.key_shift,
         'SPACE': self.key_space,
         'LEFT': self.key_left,
         'RIGHT': self.key_right}
        self.keyImagesShift = {'BACKSPACE': self.key_backspace,
         'CLEAR': self.key_clr,
         'EXIT': self.key_esc,
         'OK': self.key_ok,
         'SHIFT': self.key_shift_sel,
         'SPACE': self.key_space,
         'LEFT': self.key_left,
         'RIGHT': self.key_right}
        self['country'] = StaticText('')
        self['header'] = Label()
        self['text'] = Input(currPos=len(kwargs.get('text', '').decode('utf-8', 'ignore')), allMarked=False, **kwargs)
        self['list'] = VirtualKeyBoardList([])
        self['actions'] = NumberActionMap(['OkCancelActions',
         'WizardActions',
         'ColorActions',
         'KeyboardInputActions',
         'InputBoxActions',
         'InputAsciiActions'], {'gotAsciiCode': self.keyGotAscii,
         'ok': self.okClicked,
         'cancel': self.exit,
         'left': self.left,
         'right': self.right,
         'up': self.up,
         'down': self.down,
         'red': self.exit,
         'green': self.ok,
         'yellow': self.switchLang,
         'blue': self.shiftClicked,
         'deleteBackward': self.backClicked,
         'deleteForward': self.forwardClicked,
         'back': self.exit,
         'pageUp': self.cursorRight,
         'pageDown': self.cursorLeft,
         '1': self.keyNumberGlobal,
         '2': self.keyNumberGlobal,
         '3': self.keyNumberGlobal,
         '4': self.keyNumberGlobal,
         '5': self.keyNumberGlobal,
         '6': self.keyNumberGlobal,
         '7': self.keyNumberGlobal,
         '8': self.keyNumberGlobal,
         '9': self.keyNumberGlobal,
         '0': self.keyNumberGlobal}, -2)
        self.setLang()
        self.onExecBegin.append(self.setKeyboardModeAscii)
        self.onLayoutFinish.append(self.buildVirtualKeyBoard)
        self.onClose.append(self.__onClose)
        return

    def __onClose(self):
        self.sms.timer.stop()

    def switchLang(self):
        self.lang = self.nextLang
        self.setLang()
        self.buildVirtualKeyBoard()

    def setLang(self):
        if self.lang == 'de_DE':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfc',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xdc',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.nextLang = 'es_ES'
        elif self.lang == 'es_ES':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf3',
              u'\xe1',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\u0141',
              u'\u0155',
              u'\xe9',
              u'\u010d',
              u'\xed',
              u'\u011b',
              u'\u0144',
              u'\u0148',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xda',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd3',
              u'\xc1',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0154',
              u'\xc9',
              u'\u010c',
              u'\xcd',
              u'\u011a',
              u'\u0143',
              u'\u0147',
              u'OK']]
            self.nextLang = 'fi_FI'
        elif self.lang == 'fi_FI':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xe9',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'\u013a',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xc9',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0139',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.nextLang = 'lv_LV'
        elif self.lang == 'lv_LV':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'y',
              u'u',
              u'i',
              u'o',
              u'p',
              u'-',
              u'\u0161'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u';',
              u"'",
              u'\u016b'],
             [u'<',
              u'z',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              u'.',
              u'\u017e',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'\u0101',
              u'\u010d',
              u'\u0113',
              u'\u0123',
              u'\u012b',
              u'\u0137',
              u'\u013c',
              u'\u0146',
              u'LEFT',
              u'RIGHT']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'@',
              u'$',
              u'*',
              u'(',
              u')',
              u'_',
              u'=',
              u'/',
              u'\\',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Y',
              u'U',
              u'I',
              u'O',
              u'P',
              u'+',
              u'\u0160'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u':',
              u'"',
              u'\u016a'],
             [u'>',
              u'Z',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u'#',
              u'?',
              u'\u017d',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'\u0100',
              u'\u010c',
              u'\u0112',
              u'\u0122',
              u'\u012a',
              u'\u0136',
              u'\u013b',
              u'\u0145',
              u'LEFT',
              u'RIGHT']]
            self.nextLang = 'ru_RU'
        elif self.lang == 'ru_RU':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'\u0430',
              u'\u0431',
              u'\u0432',
              u'\u0433',
              u'\u0434',
              u'\u0435',
              u'\u0451',
              u'\u0436',
              u'\u0437',
              u'\u0438',
              u'\u0439',
              u'+'],
             [u'\u043a',
              u'\u043b',
              u'\u043c',
              u'\u043d',
              u'\u043e',
              u'\u043f',
              u'\u0440',
              u'\u0441',
              u'\u0442',
              u'\u0443',
              u'\u0444',
              u'#'],
             [u'<',
              u'\u0445',
              u'\u0446',
              u'\u0447',
              u'\u0448',
              u'\u0449',
              u'\u044a',
              u'\u044b',
              u',',
              u'.',
              u'-',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\u044c',
              u'\u044d',
              u'\u044e',
              u'\u044f',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'\u0410',
              u'\u0411',
              u'\u0412',
              u'\u0413',
              u'\u0414',
              u'\u0415',
              u'\u0401',
              u'\u0416',
              u'\u0417',
              u'\u0418',
              u'\u0419',
              u'*'],
             [u'\u041a',
              u'\u041b',
              u'\u041c',
              u'\u041d',
              u'\u041e',
              u'\u041f',
              u'\u0420',
              u'\u0421',
              u'\u0422',
              u'\u0423',
              u'\u0424',
              u"'"],
             [u'>',
              u'\u0425',
              u'\u0426',
              u'\u0427',
              u'\u0428',
              u'\u0429',
              u'\u042a',
              u'\u042b',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u042c',
              u'\u042d',
              u'\u042e',
              u'\u042f',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.nextLang = 'sv_SE'
        elif self.lang == 'sv_SE':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xe9',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\xf6',
              u'\xe4',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'@',
              u'\xdf',
              u'\u013a',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\xc9',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\xd6',
              u'\xc4',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u0139',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.nextLang = 'sk_SK'
        elif self.lang == 'sk_SK':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\u013e',
              u'@',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'\u0161',
              u'\u010d',
              u'\u017e',
              u'\xfd',
              u'\xe1',
              u'\xed',
              u'\xe9',
              u'OK',
              u'LEFT',
              u'RIGHT']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\u0165',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\u0148',
              u'\u010f',
              u"'"],
             [u'\xc1',
              u'\xc9',
              u'\u010e',
              u'\xcd',
              u'\xdd',
              u'\xd3',
              u'\xda',
              u'\u017d',
              u'\u0160',
              u'\u010c',
              u'\u0164',
              u'\u0147'],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\xe4',
              u'\xf6',
              u'\xfc',
              u'\xf4',
              u'\u0155',
              u'\u013a',
              u'OK']]
            self.nextLang = 'cs_CZ'
        elif self.lang == 'cs_CZ':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'z',
              u'u',
              u'i',
              u'o',
              u'p',
              u'\xfa',
              u'+'],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u'\u016f',
              u'@',
              u'#'],
             [u'<',
              u'y',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'-',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'\u011b',
              u'\u0161',
              u'\u010d',
              u'\u0159',
              u'\u017e',
              u'\xfd',
              u'\xe1',
              u'\xed',
              u'\xe9',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'"',
              u'\xa7',
              u'$',
              u'%',
              u'&',
              u'/',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Z',
              u'U',
              u'I',
              u'O',
              u'P',
              u'\u0165',
              u'*'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'\u0148',
              u'\u010f',
              u"'"],
             [u'>',
              u'Y',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'?',
              u'\\',
              u'\u010c',
              u'\u0158',
              u'\u0160',
              u'\u017d',
              u'\xda',
              u'\xc1',
              u'\xc9',
              u'OK']]
            self.nextLang = 'el_GR'
        elif self.lang == 'el_GR':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'=',
              u'\u03c2',
              u'\u03b5',
              u'\u03c1',
              u'\u03c4',
              u'\u03c5',
              u'\u03b8',
              u'\u03b9',
              u'\u03bf',
              u'\u03c0',
              u'[',
              u']'],
             [u'\u03b1',
              u'\u03c3',
              u'\u03b4',
              u'\u03c6',
              u'\u03b3',
              u'\u03b7',
              u'\u03be',
              u'\u03ba',
              u'\u03bb',
              u';',
              u"'",
              u'-'],
             [u'\\',
              u'\u03b6',
              u'\u03c7',
              u'\u03c8',
              u'\u03c9',
              u'\u03b2',
              u'\u03bd',
              u'\u03bc',
              u',',
              '.',
              u'/',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'\u03ac',
              u'\u03ad',
              u'\u03ae',
              u'\u03af',
              u'\u03cc',
              u'\u03cd',
              u'\u03ce',
              u'\u03ca',
              u'\u03cb',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'@',
              u'#',
              u'$',
              u'%',
              u'^',
              u'&',
              u'*',
              u'(',
              u')',
              u'BACKSPACE'],
             [u'+',
              u'\u20ac',
              u'\u0395',
              u'\u03a1',
              u'\u03a4',
              u'\u03a5',
              u'\u0398',
              u'\u0399',
              u'\u039f',
              u'\u03a0',
              u'{',
              u'}'],
             [u'\u0391',
              u'\u03a3',
              u'\u0394',
              u'\u03a6',
              u'\u0393',
              u'\u0397',
              u'\u039e',
              u'\u039a',
              u'\u039b',
              u':',
              u'"',
              u'_'],
             [u'|',
              u'\u0396',
              u'\u03a7',
              u'\u03a8',
              u'\u03a9',
              u'\u0392',
              u'\u039d',
              u'\u039c',
              u'<',
              u'>',
              u'?',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'\u0386',
              u'\u0388',
              u'\u0389',
              u'\u038a',
              u'\u038c',
              u'\u038e',
              u'\u038f',
              u'\u03aa',
              u'\u03ab',
              u'OK']]
            self.nextLang = 'pl_PL'
        elif self.lang == 'pl_PL':
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'y',
              u'u',
              u'i',
              u'o',
              u'p',
              u'-',
              u'['],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u';',
              u"'",
              u'\\'],
             [u'<',
              u'z',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'/',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'\u0105',
              u'\u0107',
              u'\u0119',
              u'\u0142',
              u'\u0144',
              u'\xf3',
              u'\u015b',
              u'\u017a',
              u'\u017c',
              u'OK']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'@',
              u'#',
              u'$',
              u'%',
              u'^',
              u'&',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Y',
              u'U',
              u'I',
              u'O',
              u'P',
              u'*',
              u']'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'?',
              u'"',
              u'|'],
             [u'>',
              u'Z',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'\u0104',
              u'\u0106',
              u'\u0118',
              u'\u0141',
              u'\u0143',
              u'\xd3',
              u'\u015a',
              u'\u0179',
              u'\u017b',
              u'OK']]
            self.nextLang = 'en_EN'
        else:
            self.keys_list = [[u'EXIT',
              u'1',
              u'2',
              u'3',
              u'4',
              u'5',
              u'6',
              u'7',
              u'8',
              u'9',
              u'0',
              u'BACKSPACE'],
             [u'q',
              u'w',
              u'e',
              u'r',
              u't',
              u'y',
              u'u',
              u'i',
              u'o',
              u'p',
              u'-',
              u'['],
             [u'a',
              u's',
              u'd',
              u'f',
              u'g',
              u'h',
              u'j',
              u'k',
              u'l',
              u';',
              u"'",
              u'\\'],
             [u'<',
              u'z',
              u'x',
              u'c',
              u'v',
              u'b',
              u'n',
              u'm',
              u',',
              '.',
              u'/',
              u'ALL'],
             [u'SHIFT',
              u'SPACE',
              u'OK',
              u'LEFT',
              u'RIGHT',
              u'*']]
            self.shiftkeys_list = [[u'EXIT',
              u'!',
              u'@',
              u'#',
              u'$',
              u'%',
              u'^',
              u'&',
              u'(',
              u')',
              u'=',
              u'BACKSPACE'],
             [u'Q',
              u'W',
              u'E',
              u'R',
              u'T',
              u'Y',
              u'U',
              u'I',
              u'O',
              u'P',
              u'+',
              u']'],
             [u'A',
              u'S',
              u'D',
              u'F',
              u'G',
              u'H',
              u'J',
              u'K',
              u'L',
              u'?',
              u'"',
              u'|'],
             [u'>',
              u'Z',
              u'X',
              u'C',
              u'V',
              u'B',
              u'N',
              u'M',
              u';',
              u':',
              u'_',
              u'CLEAR'],
             [u'SHIFT',
              u'SPACE',
              u'OK',
              u'LEFT',
              u'RIGHT',
              u'~']]
            self.lang = 'en_EN'
            self.nextLang = 'de_DE'
        self['country'].setText(self.lang)
        self.max_key = 47 + len(self.keys_list[4])

    def virtualKeyBoardEntryComponent(self, keys):
        w, h = skin.parameters.get('VirtualKeyboard', (45, 45))
        key_bg_width = self.key_bg and self.key_bg.size().width() or w
        key_images = self.shiftMode and self.keyImagesShift or self.keyImages
        res = [keys]
        text = []
        x = 0
        for key in keys:
            png = key_images.get(key, None)
            if png:
                width = png.size().width()
                res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=png))
            else:
                width = key_bg_width
                res.append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=self.key_bg))
                text.append(MultiContentEntryText(pos=(x, 0), size=(width, h), font=0, text=key.encode('utf-8'), flags=RT_HALIGN_CENTER | RT_VALIGN_CENTER))
            x += width

        return res + text

    def buildVirtualKeyBoard(self):
        self.previousSelectedKey = None
        self.list = []
        for keys in self.shiftMode and self.shiftkeys_list or self.keys_list:
            self.list.append(self.virtualKeyBoardEntryComponent(keys))

        self.markSelectedKey()
        return

    def markSelectedKey(self):
        w, h = skin.parameters.get('VirtualKeyboard', (45, 45))
        if self.previousSelectedKey is not None:
            self.list[self.previousSelectedKey / 12] = self.list[self.previousSelectedKey / 12][:-1]
        width = self.key_sel.size().width()
        x = self.list[self.selectedKey / 12][self.selectedKey % 12 + 1][1]
        self.list[self.selectedKey / 12].append(MultiContentEntryPixmapAlphaTest(pos=(x, 0), size=(width, h), png=self.key_sel))
        self.previousSelectedKey = self.selectedKey
        self['list'].setList(self.list)
        return

    def backClicked(self):
        self['text'].deleteBackward()

    def forwardClicked(self):
        self['text'].deleteForward()

    def shiftClicked(self):
        self.smsChar = None
        self.shiftMode = not self.shiftMode
        self.buildVirtualKeyBoard()
        return

    def okClicked(self):
        self.smsChar = None
        text = (self.shiftMode and self.shiftkeys_list or self.keys_list)[self.selectedKey / 12][self.selectedKey % 12].encode('UTF-8')
        if text == 'EXIT':
            self.close(None)
        elif text == 'BACKSPACE':
            self['text'].deleteBackward()
        elif text == 'ALL':
            self['text'].markAll()
        elif text == 'CLEAR':
            self['text'].deleteAllChars()
            self['text'].update()
        elif text == 'SHIFT':
            self.shiftClicked()
        elif text == 'SPACE':
            self['text'].char(' '.encode('UTF-8'))
        elif text == 'OK':
            self.close(self['text'].getText())
        elif text == 'LEFT':
            self['text'].left()
        elif text == 'RIGHT':
            self['text'].right()
        else:
            self['text'].char(text)
        return

    def ok(self):
        self.close(self['text'].getText())

    def exit(self):
        self.close(None)
        return

    def cursorRight(self):
        self['text'].right()

    def cursorLeft(self):
        self['text'].left()

    def left(self):
        self.smsChar = None
        self.selectedKey = self.selectedKey / 12 * 12 + (self.selectedKey + 11) % 12
        if self.selectedKey > self.max_key:
            self.selectedKey = self.max_key
        self.markSelectedKey()
        return

    def right(self):
        self.smsChar = None
        self.selectedKey = self.selectedKey / 12 * 12 + (self.selectedKey + 1) % 12
        if self.selectedKey > self.max_key:
            self.selectedKey = self.selectedKey / 12 * 12
        self.markSelectedKey()
        return

    def up(self):
        self.smsChar = None
        self.selectedKey -= 12
        if self.selectedKey < 0:
            self.selectedKey = self.max_key / 12 * 12 + self.selectedKey % 12
            if self.selectedKey > self.max_key:
                self.selectedKey -= 12
        self.markSelectedKey()
        return

    def down(self):
        self.smsChar = None
        self.selectedKey += 12
        if self.selectedKey > self.max_key:
            self.selectedKey %= 12
        self.markSelectedKey()
        return

    def keyNumberGlobal(self, number):
        self.smsChar = self.sms.getKey(number)
        self.selectAsciiKey(self.smsChar)

    def smsOK(self):
        if self.smsChar and self.selectAsciiKey(self.smsChar):
            print '[VirtualKeyboard] pressing ok now'
            self.okClicked()

    def keyGotAscii(self):
        self.smsChar = None
        if self.selectAsciiKey(str(unichr(getPrevAsciiCode()).encode('utf-8'))):
            self.okClicked()
        return

    def selectAsciiKey(self, char):
        if char == ' ':
            char = 'SPACE'
        for keyslist in (self.shiftkeys_list, self.keys_list):
            selkey = 0
            for keys in keyslist:
                for key in keys:
                    if key == char:
                        self.selectedKey = selkey
                        if self.shiftMode != (keyslist is self.shiftkeys_list):
                            self.shiftMode = not self.shiftMode
                            self.buildVirtualKeyBoard()
                        else:
                            self.markSelectedKey()
                        return True
                    selkey += 1

        return False