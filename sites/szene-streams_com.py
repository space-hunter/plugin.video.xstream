# -*- coding: utf-8 -*-
import urllib
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.util import cUtil
from resources.lib.config import cConfig
from resources.lib import logger
from json import loads
import re
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib import jsunprotect

SITE_IDENTIFIER = 'szene-streams_com'
SITE_NAME = 'Szene-Streams'
#SITE_ICON = '1kino.png'

URL_MAIN = 'http://www.szene-streams.com/'
URL_MOVIES = URL_MAIN + 'publ/'

def load():
    logger.info("Load %s" % SITE_NAME)

    oGui = cGui()
    oGui.addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'))
    oGui.setEndOfDirectory()

def showMovieMenu():
    oGui = cGui()
    oGui.addFolder(cGuiElement('Genre', SITE_IDENTIFIER, 'showMovieGenre'))
    oGui.setEndOfDirectory()

def showMovieGenre():
    oGui = cGui()
    params = ParameterHandler()
    oRequestHandler = cRequestHandler(URL_MOVIES)
    sHtmlContent = oRequestHandler.request()
    pattern = '<a class="CatInf" href="([^"]+)">' # Get the URL
    pattern += '.*?<div class="CatNumInf">([^<>]+)</div>' # Get the entry count
    pattern += '.*?<div class="CatNameInf">([^<>]+)</div>' # Get the genre name
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    for sUrl, sNum, sName in aResult[1]:
        if not sUrl or not sNum or not sName: return
        oGuiElement = cGuiElement("%s (%d)" %(sName, int(sNum)), SITE_IDENTIFIER, 'showMovies')
        params.setParam('sUrl', sUrl)
        oGui.addFolder(oGuiElement, params)
    oGui.setEndOfDirectory()

def showMovies():
    oGui = cGui()
    params = ParameterHandler()
    oRequestHandler = cRequestHandler(params.getValue('sUrl'))
    sHtmlContent = oRequestHandler.request()
    pattern = '<div class="screenshot".*?<a href="([^"]+)" class="ulightbox"'
    pattern += '.*?<a class="newstitl entryLink".*?href="([^"]+)">([^<>]+)</a>'
    pattern += '.*?<div class="MessWrapsNews2".*?>([^<>]+).*?</div>'
    aResult = cParser().parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    for sThumbnail, sUrl, sName, sDesc in aResult[1]:
        oGuiElement = cGuiElement(sName, SITE_IDENTIFIER, 'showMovies')
        oGuiElement.setMediaType('movie')
        oGuiElement.setThumbnail(sThumbnail)
        oGuiElement.setDescription(sDesc.strip())
        oGui.addFolder(oGuiElement, params)
    oGui.setView('movie')
    oGui.setEndOfDirectory()


