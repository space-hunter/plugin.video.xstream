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

SITE_IDENTIFIER = 'szene-streams_com'
SITE_NAME = 'Szene-Streams'

URL_MAIN = 'http://www.szene-streams.com/'
URL_MOVIES = URL_MAIN + 'publ/'
URL_SHOWS = URL_MAIN + 'load/'

def load():
    logger.info("Load %s" % SITE_NAME)
    oGui = cGui()
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    oGui.addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showTvShowMenu'))
    oGui.setEndOfDirectory()

def showMovieMenu():
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('mediaTypePageId', 1)
    params.setParam('sUrl', URL_MAIN)
    oGui.addFolder(cGuiElement('Neue Filme', SITE_IDENTIFIER, 'showEntries'), params)
    params.setParam('sUrl', URL_MOVIES)
    oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
    oGui.setEndOfDirectory()

def showTvShowMenu():
    oGui = cGui()
    params = ParameterHandler()
    params.setParam('mediaTypePageId', 1)
    params.setParam('sUrl', URL_SHOWS)
    oGui.addFolder(cGuiElement('Alle Serien', SITE_IDENTIFIER, 'showEntries'), params)
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showGenre'), params)
    oGui.setEndOfDirectory()

def showGenre():
    oGui = cGui()
    params = ParameterHandler()
    oRequestHandler = cRequestHandler(params.getValue('sUrl'))
    sHtmlContent = oRequestHandler.request()
    # Get the URL
    pattern = '<a[^>]*?class="CatInf"[^>]*?href="(.*?)"[^>]*?>.*?'
     # Get the entry count
    pattern += '<div[^>]*?class="CatNumInf"[^>]*?>(\d+)</div>.*?'
    # Get the genre name
    pattern += '<div[^>]*?class="CatNameInf"[^>]*?>([^<>]+)</div>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    for sUrl, sNum, sName in aResult[1]:
        if not sUrl or not sNum or not sName: return
        oGuiElement = cGuiElement("%s (%d)" %(sName, int(sNum)), SITE_IDENTIFIER, 'showEntries')
        params.setParam('sUrl', sUrl)
        params.setParam('mediaTypePageId', 1)
        oGui.addFolder(oGuiElement, params)
    oGui.setEndOfDirectory()

def showEntries(sContent = False):
    oGui = cGui()
    oGui.setView('movie')
    params = ParameterHandler()
    if sContent:
        sHtmlContent = sContent
    else:
        oRequestHandler = cRequestHandler(params.getValue('sUrl'))
        sHtmlContent = oRequestHandler.request()
    # Grab the thumbnail
    pattern = '<div class="screenshot".*?<a href="([^"]+)"'
    # Grab the name and link
    pattern += '.*?<a class="[^"]*?entryLink[^"]*?".*?href="([^"]+)">(.*?)</a>'
    # Grab the description
    pattern += '.*?<div class="MessWrapsNews2".*?>([^<>]+).*?</div>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    for sThumbnail, sUrl, sName, sDesc in aResult[1]:
        # Remove HTML tags from the name
        sName = re.sub('<[^<]+?>', '', sName)
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showHosters')
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc.strip())
        params.setParam('entryUrl', sUrl)
        oGui.addFolder(oGuiElement, params, bIsFolder = False)

    pattern = '<a class="swchItem" href="([^"]+)".*?><span>(\d+)</span></a>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if aResult[0]:
        currentPage = int(params.getValue('mediaTypePageId'))
        for sUrl, sPage in aResult[1]:
            page = int(sPage)
            if page <= currentPage: continue
            params.setParam('sUrl', URL_MAIN + sUrl)
            params.setParam('mediaTypePageId', page)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
            break
    oGui.setEndOfDirectory()

# Show the hosters dialog
def showHosters():
    params= ParameterHandler()
    oRequestHandler = cRequestHandler(params.getValue('entryUrl'))
    sHtmlContent = oRequestHandler.request()
    pattern = '<div class="inner" style="display:none;">'
    pattern += '.*?<a target="_blank" href="([^"]+)">'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    hosters = []
    for sUrl in aResult[1]:
        hoster = dict()
        hoster['link'] = sUrl
        hname = 'Unknown Hoster'
        try:
            hname = re.compile('^(?:https?:\/\/)?(?:[^@\n]+@)?([^:\/\n]+)', flags=re.I | re.M).findall(hoster['link'])[0]
        except:
            pass
        if hname == 'linkcrypt.ws':
            resolveLinkcrypt(sUrl, hosters)
            continue

        hoster['name'] = hname
        hoster['displayedName'] = hname
        hosters.append(hoster)
    if hosters:
        hosters.append('getHosterUrl')
    return hosters

# Show the search dialog, return/abort on empty input
def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(oGui, sSearchText)
    oGui.setEndOfDirectory()

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

# Search using the requested string sSearchText
def _search(oGui, sSearchText):
    if not sSearchText: return
    req = urllib2.Request(URL_MOVIES)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    values = { 'query' : sSearchText, 'a' : '2' }
    response = urllib2.urlopen(req, urllib.urlencode(values))
    data = response.read()
    response.close()
    showEntries(data)

# Taken and modified from pyLoad module/plugins/crypter/LinkCryptWs.py
def resolveLinkcrypt(sUrl, hosters):
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    pattern = '<form action="http://linkcrypt.ws/out.html"[^>]*?>.*?<input[^>]*?value="(.+?)"[^>]*?name="file"'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return

    for idx, weblink_id in enumerate(aResult[1]):
        try:
            data = urllib.urlencode({ 'file' : weblink_id })
            req = urllib2.Request("http://linkcrypt.ws/out.html", data)
            res = urllib2.urlopen(req).read()
            link = re.compile("top.location.href=doNotTrack\('(.+?)'\)").findall(res)[0]
            hname = re.compile('^(?:https?:\/\/)?(?:[^@\n]+@)?([^:\/\n]+)', flags=re.I | re.M).findall(link)[0]
            hname = "Part %d - %s" % (idx + 1, hname)
            logger.info("Resolved LinkCrypt link: %s" % link)
            hoster = dict()
            hoster['link'] = link
            hoster['name'] = hname
            hoster['displayedName'] = hname
            hosters.append(hoster)
        except Exception, detail:
            logger.info(detail)
            pass
