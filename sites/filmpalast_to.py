# -*- coding: utf-8 -*-
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib import logger
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.pluginHandler import cPluginHandler
from resources.lib.util import cUtil
import re, urllib, urllib2

SITE_IDENTIFIER = 'filmpalast_to'
SITE_NAME = 'FilmPalast.to'
SITE_ICON = 'filmpalast.png'

URL_MAIN = 'http://www.filmpalast.to/'
URL_STREAM = URL_MAIN + 'stream/%d/1'
URL_MOVIES_NEW = URL_MAIN + 'movies/new'
URL_MOVIES_TOP = URL_MAIN + 'movies/top'
URL_SHOWS_NEW = URL_MAIN + 'serien/view'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('sUrl', URL_MOVIES_NEW)
    oGui.addFolder(cGuiElement('Neue Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_SHOWS_NEW)
    oGui.addFolder(cGuiElement('Neue Serien', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES_TOP)
    oGui.addFolder(cGuiElement('Top Filme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.setEndOfDirectory()

def showEntries():
    oGui = cGui()
    params = ParameterHandler()
    entryUrl = params.getValue('sUrl')
    oRequestHandler = cRequestHandler(entryUrl)
    oGui.setView('tvshows' if 'serien/' in entryUrl else 'movie')
    sHtmlContent = oRequestHandler.request()
    # Grab the link and title
    pattern = '<a[^>]*href="([^"]*)"[^>]*title="([^"]*)"[^>]*>[^<]*'
    # Grab the thumbnail
    pattern +='<img[^>]*src=["\']([^"\']*)["\'][^>]*class="cover-opacity"[^>]*>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    for sUrl, sName, sThumbnail in aResult[1]:
        logger.info(sThumbnail)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(__checkUrl(sThumbnail))
        params.setParam('entryUrl', __checkUrl(sUrl))
        oGui.addFolder(oGuiElement, params, bIsFolder = False)

    pattern = '<a[^>]*class="[^"]*pageing[^"]*"[^>]*'
    pattern += 'href=["\']([^"\']*)["\'][^>]*>[ ]*vorw'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0]:
        logger.info(aResult[1][0])
        params.setParam('sUrl', aResult[1][0])
        oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
    oGui.setEndOfDirectory()

# Show the hosters dialog
def showHosters():
    params= ParameterHandler()
    logger.info(params.getValue('entryUrl'))
    oRequestHandler = cRequestHandler(params.getValue('entryUrl'))
    sHtmlContent = oRequestHandler.request()
    pattern = '<p[^>]*class="hostName"[^>]*>([^<>]+)</p>.*?'
    pattern += '<a[^>]*class="[^"]*stream-src[^"]*"[^>]*data-id="([^"]+)"[^>]*>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    hosters = []
    for sHost, sId in aResult[1]:
        hoster = dict()
        hoster['link'] = __getSource(sId)
        hoster['name'] = sHost
        hoster['displayedName'] = sHost
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

def getHosterUrl(sUrl = False):
    oParams = ParameterHandler()
    if not sUrl:
        sUrl = oParams.getValue('url')
    results = []
    result = {}
    result['streamUrl'] = sUrl
    result['resolved'] = False
    results.append(result)
    return results

def __checkUrl(url):
    return url if 'http:' in url else URL_MAIN + url

def __getSource(id):
    url = URL_STREAM % int(id)
    from t0mm0.common.net import Net
    idValue = { 'streamID' : id }
    headValue = { 'Referer' : URL_MAIN, 'X-Requested-With':'XMLHttpRequest' }
    data = Net().http_POST(url, idValue, headValue).content
    return re.compile('"url":"([^"]+)"').findall(data)[0].replace('\\', '')
