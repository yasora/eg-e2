# Embedded file name: /usr/lib/enigma2/python/Components/SystemInfo.py
from os import path
from enigma import eDVBResourceManager, Misc_Options
from Tools.Directories import fileExists, fileCheck
from Tools.HardwareInfo import HardwareInfo
from boxbranding import getBoxType, getMachineBuild
SystemInfo = {}

def getNumVideoDecoders():
    idx = 0
    while fileExists('/dev/dvb/adapter0/video%d' % idx, 'f'):
        idx += 1

    return idx


SystemInfo['NumVideoDecoders'] = getNumVideoDecoders()
SystemInfo['PIPAvailable'] = SystemInfo['NumVideoDecoders'] > 1
SystemInfo['CanMeasureFrontendInputPower'] = eDVBResourceManager.getInstance().canMeasureFrontendInputPower()

def countFrontpanelLEDs():
    leds = 0
    if fileExists('/proc/stb/fp/led_set_pattern'):
        leds += 1
    while fileExists('/proc/stb/fp/led%d_pattern' % leds):
        leds += 1

    return leds


SystemInfo['12V_Output'] = Misc_Options.getInstance().detected_12V_output()
SystemInfo['ZapMode'] = fileCheck('/proc/stb/video/zapmode') or fileCheck('/proc/stb/video/zapping_mode')
SystemInfo['NumFrontpanelLEDs'] = countFrontpanelLEDs()
SystemInfo['FrontpanelDisplay'] = fileExists('/dev/dbox/oled0') or fileExists('/dev/dbox/lcd0')
SystemInfo['OledDisplay'] = fileExists('/dev/dbox/oled0')
SystemInfo['LcdDisplay'] = fileExists('/dev/dbox/lcd0') or getMachineBuild() in ('inihde', 'inihde2', 'inihdx')
SystemInfo['DisplayLED'] = getBoxType() in ('gb800se', 'gb800solo')
SystemInfo['LEDButtons'] = getBoxType() == 'vuultimo'
SystemInfo['DeepstandbySupport'] = HardwareInfo().has_deepstandby()
SystemInfo['Fan'] = fileCheck('/proc/stb/fp/fan')
SystemInfo['FanPWM'] = SystemInfo['Fan'] and fileCheck('/proc/stb/fp/fan_pwm')
SystemInfo['StandbyPowerLed'] = fileExists('/proc/stb/power/standbyled')
SystemInfo['StandbyLED'] = fileCheck('/proc/stb/power/standbyled')
SystemInfo['WakeOnLAN'] = getBoxType() not in ('et8000', 'et10000') and fileCheck('/proc/stb/power/wol') or fileCheck('/proc/stb/fp/wol')
SystemInfo['HDMICEC'] = (fileExists('/dev/hdmi_cec') or fileExists('/dev/misc/hdmi_cec0')) and fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/HdmiCEC/plugin.pyo')
SystemInfo['SABSetup'] = fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/SABnzbd/plugin.pyo')
SystemInfo['SeekStatePlay'] = False
SystemInfo['GraphicLCD'] = getBoxType() in ('vuultimo', 'et10000', 'mutant2400', 'quadbox2400') or getMachineBuild() in 'inihdp'
SystemInfo['Blindscan'] = fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/Blindscan/plugin.pyo')
SystemInfo['Satfinder'] = fileExists('/usr/lib/enigma2/python/Plugins/SystemPlugins/Satfinder/plugin.pyo')
SystemInfo['HasExternalPIP'] = getMachineBuild() not in ('et9x00', 'et6x00', 'et5x00') and fileCheck('/proc/stb/vmpeg/1/external')
SystemInfo['hasPIPVisibleProc'] = fileCheck('/proc/stb/vmpeg/1/visible')
SystemInfo['VideoDestinationConfigurable'] = fileExists('/proc/stb/vmpeg/0/dst_left')
SystemInfo['GBWOL'] = fileExists('/usr/bin/gigablue_wol')
SystemInfo['isGBIPBOX'] = fileExists('/usr/lib/enigma2/python/gbipbox.so')
SystemInfo['LCDSKINSetup'] = path.exists('/usr/share/enigma2/display')
SystemInfo['VFD_scroll_repeats'] = fileCheck('/proc/stb/lcd/scroll_repeats')
SystemInfo['VFD_scroll_delay'] = fileCheck('/proc/stb/lcd/scroll_delay')
SystemInfo['VFD_initial_scroll_delay'] = fileCheck('/proc/stb/lcd/initial_scroll_delay')
SystemInfo['VFD_final_scroll_delay'] = fileCheck('/proc/stb/lcd/final_scroll_delay')
SystemInfo['LcdLiveTV'] = fileCheck('/proc/stb/fb/sd_detach')
SystemInfo['LCDMiniTV'] = fileExists('/proc/stb/lcd/mode')
SystemInfo['LCDMiniTVPiP'] = SystemInfo['LCDMiniTV'] and getBoxType() != 'gb800ueplus'
SystemInfo['3DMode'] = fileCheck('/proc/stb/fb/3dmode') or fileCheck('/proc/stb/fb/primary/3d')
SystemInfo['3DZNorm'] = fileCheck('/proc/stb/fb/znorm') or fileCheck('/proc/stb/fb/primary/zoffset')
SystemInfo['Blindscan_t2_available'] = fileCheck('/proc/stb/info/vumodel')
SystemInfo['grautec'] = fileExists('/tmp/usbtft')
SystemInfo['CanUse3DModeChoices'] = fileExists('/proc/stb/fb/3dmode_choices') and True or False