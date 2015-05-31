"""
    Moonlight - Add-on to launch Moonlight application from Kodi/XBMC
"""

import xbmcgui
import xbmcaddon
import platform
import sys
import xbmcaddon
import subprocess

__addon__    = xbmcaddon.Addon()
__dialog__   = xbmcgui.Dialog()
__strings__  = __addon__.getLocalizedString
__name__     = __addon__.getAddonInfo('name')
__version__  = __addon__.getAddonInfo('version')
__path__     = __addon__.getAddonInfo('path')
__settings__ = __addon__.getSetting
__handle__   = sys.argv[1]

class Launch():

    def __init__(self):

        isCompatible = False
        availableSys = ['win32', 'darwin', 'linux']
        currentSys   = sys.platform

        java      = __settings__("java_path").replace("\\", "\\\\")
        moonlight = __settings__("moonlight_path").replace("\\", "\\\\")
        ip        = __settings__("host_ip")
        reso      = __settings__("resolution").replace("p","")
        fps       = __settings__("fps")
        moon_type = __settings__("moonlight_type")
        strm_cmd  = "-host"
        args_dash = "-"
        fullscrn  = " -fs"

        if moon_type == "embedded":
            args_dash = ""
            fullscrn  = ""
            strm_cmd  = "stream"

        for avSys in availableSys:
            if currentSys.startswith(avSys):
                isCompatible = True

        if isCompatible:
            if self.checkSettings(__settings__) and self.checkJava(currentSys):
                if self.isPaired(java, moonlight, args_dash, ip):
                    self.startProcess(java, moonlight, args_dash, ip, reso, fps, fullscrn, strm_cmd)
                else:
                    self.fail("Connection error - Can't pair to host")
        else:
            sef.fail("Your current platform is incompatible with this add-on !")



    def checkSettings(self, settings):

        if len(settings("moonlight_path")) < 1:
            self.fail("Please set up the Moonlight path in settings !")
            return False

        elif len(settings("host_ip")) < 1:
            self.fail("Please set up the host IP in settings !")
            return False

        elif len(settings("java_path")) < 1:
            self.fail("Please set up the Java path in settings !")
            return False

        return True



    def checkJava(self, system):

        p = subprocess.Popen('"'+__settings__('java_path')+'" -version', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if 'java version' in p.stdout.readlines()[0]:
            return True
        else:
            return False



    def stream(self, java, moonlight, ip, reso, fps, fullscreen, stream):

        __dialog__.notification(__name__, "Streaming from host...", xbmcgui.NOTIFICATION_INFO, 5000)

        streaming = subprocess.Popen('"'+java+'" -jar "'+moonlight+'" '+stream+' '+ip+' -'+reso+' -'+fps+fullscreen, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.flush()
        for line in iter(streaming.stdout.readline, b''):
            sys.stdout.flush()
            if "java.net.ConnectException" in line:
                self.fail(line)
                streaming.kill()


    def isPaired(self, java, moonlight, dash, ip):

        __dialog__.notification(__name__, "Pairing to host...", xbmcgui.NOTIFICATION_INFO, 5000)

        pairing = subprocess.Popen('"'+java+'" -jar "'+moonlight+'" '+dash+'pair '+ip, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.stdout.flush()
        for line in iter(pairing.stdout.readline, b''):
            sys.stdout.flush()
            if "java.net.ConnectException" in line:
                pairing.kill()
                return False
        if pairing.wait() == 1:
            return True
        else: 
            return False



    def fail(self, message):

        __dialog__.notification(__name__+" - "+"Error", message, xbmcgui.NOTIFICATION_ERROR)
