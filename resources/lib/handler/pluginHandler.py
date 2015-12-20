import sys
import os
import json
from resources.lib.config import cConfig
from resources.lib import common, logger

class cPluginHandler:

    def __init__(self):
        self.addon = common.addon
        self.rootFolder = common.addonPath
        self.settingsFile = os.path.join(self.rootFolder, 'resources', 'settings.xml')
        self.profilePath = common.profilePath
        self.pluginDBFile = os.path.join(self.profilePath,'pluginDB')
        logger.info('profile folder: %s' % self.profilePath)
        logger.info('root folder: %s' % self.rootFolder)
        self.defaultFolder =  os.path.join(self.rootFolder, 'sites')
        logger.info('default sites folder: %s' % self.defaultFolder)

    def getAvailablePlugins(self):
        pluginDB = self.__getPluginDB()
        # default plugins
        update = False
        fileNames = self.__getFileNamesFromFolder(self.defaultFolder)
        for fileName in fileNames:
            plugin = {'name':'', 'icon':'', 'settings':'','modified':0}
            plugin.update(pluginDB[fileName])
            try:
                modTime = os.path.getmtime( os.path.join(self.defaultFolder,fileName+'.py'))
            except OSError:
                modTime = 0
            if fileName not in pluginDB or modTime > plugin['modified']:
                logger.info('load plugin: '+ str(fileName))
                # try to import plugin
                pluginData = self.__getPluginData(fileName)
                if pluginData:
                    pluginData['modified'] = modTime
                    pluginDB[fileName] = pluginData
                    update = True
        # check pluginDB for obsolete entries
        deletions = []
        for pluginID in pluginDB:
            if pluginID not in fileNames:
                deletions.append(pluginID)
        for id in deletions:
            del pluginDB[id]
        if update or deletions:
            self.__updateSettings(pluginDB)
            self.__updatePluginDB(pluginDB)

        return self.getAvailablePluginsFromDB()

        

    def getAvailablePluginsFromDB(self):
        plugins = []
        oConfig = cConfig()
        iconFolder = os.path.join(self.rootFolder, 'resources','art','sites')
        pluginDB = self.__getPluginDB()
        for pluginID in pluginDB:
            plugin = pluginDB[pluginID]
            pluginSettingsName = 'plugin_%s' % pluginID
            plugin['id'] = pluginID
            if plugin['icon']:
                plugin['icon'] = os.path.join(iconFolder, plugin['icon'])
            else:
                plugin['icon'] = ''
            # existieren zu diesem plugin die an/aus settings
            if oConfig.getSetting(pluginSettingsName) == 'true':
                    plugins.append(plugin)
        return plugins

    def __updatePluginDB(self, data):
        file = open(self.pluginDBFile, 'w')
        json.dump(data,file)
        file.close()

    def __getPluginDB(self):
        if not os.path.exists(self.pluginDBFile):
            return dict()
        file = open(self.pluginDBFile, 'r')
        try:
            data = json.load(file)
        except ValueError:
            logger.error("pluginDB seems corrupt, creating new one")
            data = dict()
        file.close()
        return data

    def __updateSettings(self, pluginData):
        '''
        data (dict): containing plugininformations
        '''
        xmlString = '<plugin_settings>%s</plugin_settings>'
        import xml.etree.ElementTree as ET
        tree = ET.parse(self.settingsFile)
        #find Element for plugin Settings
        pluginElem = False
        for elem in tree.findall('category'):
            if elem.attrib['label']=='30022':
                pluginElem = elem
                break
        if not pluginElem:
            logger.info('could not update settings, pluginElement not found')
            return False
        pluginElements = pluginElem.findall('setting')
        for elem in pluginElements:
            pluginElem.remove(elem)          
        # add plugins to settings
        for pluginID in sorted(pluginData):
            plugin = pluginData[pluginID]
            ET.SubElement(pluginElem,'setting', {'type': 'lsep', 'label':plugin['name']})
            attrib = {'default': 'false', 'type': 'bool'}
            attrib['id'] = 'plugin_%s' % pluginID
            attrib['label'] = plugin['name']
            ET.SubElement(pluginElem, 'setting', attrib)
            if plugin['settings']:
                customSettings = []
                try:
                    customSettings = ET.XML(xmlString % plugin['settings']).findall('setting')
                except:
                    logger.info('Parsing of custom settings for % failed.' % plugin['name'])
                for setting in customSettings:
                    pluginElem.append(setting)
        try:
            ET.dump(pluginElem)
        except:
            logger.info('Settings update failed')
            return
        tree.write(self.settingsFile)

    def __getFileNamesFromFolder(self, sFolder):
        aNameList = []
        items = os.listdir(sFolder)
        for sItemName in items:
            if sItemName.endswith('.py'):
                sItemName = os.path.basename(sItemName[:-3])
                aNameList.append(sItemName)
        return aNameList

    def __getPluginData(self, fileName):
        pluginData = {}
        try:
            plugin = __import__(fileName, globals(), locals())
            pluginData['name'] = plugin.SITE_NAME                       
        except Exception, e:
            logger.error("Can't import plugin: %s :%s" % (fileName, e))
            return False
        try:
            pluginData['icon'] = plugin.SITE_ICON
        except:
            pass
        try:
            pluginData['settings'] = plugin.SITE_SETTINGS
        except:
            pass
        return pluginData