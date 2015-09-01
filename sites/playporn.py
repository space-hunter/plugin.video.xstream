# -*- coding: utf-8 -*-
# Created by Burnst
from resources.lib.gui.gui import cGui
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.util import cUtil


SITE_IDENTIFIER = 'PlayPorn'
SITE_NAME = 'PlayPorn'
#SITE_ICON = 'kinoleak.png'

IS_ADULT = True

URL_MAIN = 'http://playporn.to/'
URL_ALL  = 'http://playporn.to/category/xxx-movie-stream/'

URL_AMATEURE    = 'http://playporn.to/category/xxx-movie-stream/amateure/'
URL_ANAL    = 'http://playporn.to/category/xxx-movie-stream/anal/'
URL_ASIAN    = 'http://playporn.to/category/xxx-movie-stream/asian-girls/'
URL_BIGTITS  = 'http://playporn.to/category/xxx-movie-stream/big-tits-stream/'
URL_BLACK  = 'http://playporn.to/category/xxx-movie-stream/black/'
URL_DEUTSCH     = 'http://playporn.to/category/xxx-movie-stream/deutsch/'
URL_FETISH   = 'http://playporn.to/category/xxx-movie-stream/fetish/'
URL_GROUPSEX = 'http://playporn.to/category/xxx-movie-stream/gangbang-gruppensex/'
URL_HARDCORE = 'http://playporn.to/category/xxx-movie-stream/hardcore-fuck/'
URL_LESBIEN     = 'http://playporn.to/category/xxx-movie-stream/lesben-sex/'
URL_MASTURBATION     = 'http://playporn.to/category/xxx-movie-stream/masturbation-toys/'
URL_MATURE     = 'http://playporn.to/category/xxx-movie-stream/mature-milf-xxx-movie-stream/'
URL_ORAL     = 'http://playporn.to/category/xxx-movie-stream/oral-blowjob/'
URL_PORNSTARS     = 'http://playporn.to/category/xxx-movie-stream/pornstars/'
URL_TEENS     = 'http://playporn.to/category/xxx-movie-stream/teens-sex/'


def load():
  oGui = cGui()
  oGui.addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch'))
  oGui.addFolder(cGuiElement('Alle Filme', SITE_IDENTIFIER, 'showAllMovies'))
  oGui.addFolder(cGuiElement('Amateure', SITE_IDENTIFIER, 'showGenreAmateure'))
  oGui.addFolder(cGuiElement('Anal', SITE_IDENTIFIER, 'showGenreAnal'))
  oGui.addFolder(cGuiElement('Asian', SITE_IDENTIFIER, 'showGenreAsian'))
  oGui.addFolder(cGuiElement('Titten', SITE_IDENTIFIER, 'showGenreTitten'))  
  oGui.addFolder(cGuiElement('Black', SITE_IDENTIFIER, 'showGenreBlack'))
  oGui.addFolder(cGuiElement('Deutsch', SITE_IDENTIFIER, 'showGenreDeutsch'))
  oGui.addFolder(cGuiElement('Fetisch', SITE_IDENTIFIER, 'showGenreFetish'))
  oGui.addFolder(cGuiElement('Gruppensex', SITE_IDENTIFIER, 'showGenreGroupsex'))
  oGui.addFolder(cGuiElement('Hardcore', SITE_IDENTIFIER, 'showGenreHardcore'))
  oGui.addFolder(cGuiElement('Lesben', SITE_IDENTIFIER, 'showGenreLesbien'))
  oGui.addFolder(cGuiElement('Masturbation', SITE_IDENTIFIER, 'showGenreMasturbation'))
  oGui.addFolder(cGuiElement('MILF', SITE_IDENTIFIER, 'showGenreMature'))
  oGui.addFolder(cGuiElement('Oral', SITE_IDENTIFIER, 'showGenreOral'))
  oGui.addFolder(cGuiElement('Pornstars', SITE_IDENTIFIER, 'showGenrePornstars'))
  oGui.addFolder(cGuiElement('Teens', SITE_IDENTIFIER, 'showGenreTeens'))
  oGui.setEndOfDirectory()

def showAllMovies():
    Page = 1
    Search = False
    _parseMovieList(URL_ALL, Page, Search)

def showGenreAmateure():
    Page = 1
    Search = False
    _parseMovieList(URL_AMATEURE, Page, Search)
  
def showGenreAnal():
    Page = 1
    Search = False
    _parseMovieList(URL_ANAL, Page, Search)

def showGenreAsian():
    Page = 1
    Search = False
    _parseMovieList(URL_ASIAN, Page, Search)

def showGenreTitten():
    Page = 1
    Search = False
    _parseMovieList(URL_BIGTITS, Page, Search)
    
def showGenreBlack():
    Page = 1
    Search = False
    _parseMovieList(URL_BLACK, Page, Search)

def showGenreDeutsch():
    Page = 1
    Search = False
    _parseMovieList(URL_DEUTSCH, Page, Search)

def showGenreFetish():
    Page = 1
    Search = False
    _parseMovieList(URL_FETISH, Page, Search)

def showGenreGroupsex():
    Page = 1
    Search = False
    _parseMovieList(URL_GROUPSEX, Page, Search)

def showGenreHardcore():
    Page = 1
    Search = False
    _parseMovieList(URL_HARDCORE, Page, Search)

def showGenreLesbien():
    Page = 1
    Search = False
    _parseMovieList(URL_LESBIEN, Page, Search)

def showGenreMasturbation():
    Page = 1
    Search = False
    _parseMovieList(URL_MASTURBATION, Page, Search)

def showGenreMature():
    Page = 1
    Search = False
    _parseMovieList(URL_MATURE, Page, Search)

def showGenreOral():
    Page = 1
    Search = False
    _parseMovieList(URL_ORAL, Page, Search)

def showGenrePornstars():
    Page = 1
    Search = False
    _parseMovieList(URL_PORNSTARS, Page, Search)

def showGenreTeens():
    Page = 1
    Search = False
    _parseMovieList(URL_TEENS, Page, Search)

def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False and sSearchText != ''):
        Page = 1
        searchtext = sSearchText.replace (' ', '+')
        searchUrl = '?s=' + searchtext + "&submit=Search"
        _parseMovieList(URL_MAIN + searchUrl, Page, searchUrl)   
    else:
        return
    oGui.setEndOfDirectory()
	
def _parseMovieList(url, page, search): 
    oGui = cGui()  
    params = ParameterHandler()
    iTotalPages = __getTotalPages(url, page)
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    # parse movie entries
    pattern = 'class="photo-thumb-image".*?<a href="([^"]+)" title="([^"]+)".*? src="([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, pattern)
    if not aResult[0]:
        return
    total = len(aResult[1]) # Anzahl der Treffer
    for link, title, img in aResult[1]:
        movieTitle = cUtil().unescape(title.decode('utf-8')).encode('utf-8') # encoding anpassen wegen Umlauten
        guiElement = cGuiElement(movieTitle, SITE_IDENTIFIER, 'getHosters')
        guiElement.setThumbnail(img) #Cover als Thumbnail setzen
        guiElement.setMediaType('movie')
        params.setParam('movieUrl',str(link))
        oGui.addFolder(guiElement, params, bIsFolder = False, iTotal = total)
    
    param = ParameterHandler()
    param.setParam('iPage', int(page))
    param.setParam('iTotalPages', iTotalPages)
    if (search != False and search != ''):
        param.setParam('searchUrl', str(search))
        oGuiElement = cGuiElement('Zu Seite X von '+str(iTotalPages),SITE_IDENTIFIER,'gotoPageSearch')
        oGui.addFolder(oGuiElement, param)
        if not int(page) == int(iTotalPages):
            oGui.addNextPage(SITE_IDENTIFIER,'__nextPageSearch', param)
    else:
        if int(page) == 1:
            param.setParam('siteUrl', str(url))
        oGuiElement = cGuiElement('Zu Seite X von '+str(iTotalPages),SITE_IDENTIFIER,'gotoPage')
        oGui.addFolder(oGuiElement, param)
        if not int(page) == int(iTotalPages):
            oGui.addNextPage(SITE_IDENTIFIER,'__nextPage', param)
    
    oGui.setView('movies') #diese Liste unterliegt den automatisch ViewSettings für Filmlisten 
    oGui.setEndOfDirectory()
    
def __nextPageSearch():
    oParams = ParameterHandler()
    Page = oParams.getValue('iPage')
    sUrle = oParams.getValue('searchUrl')
    Page = int(Page) + 1
    sUrl = URL_MAIN +'page/'+str(Page)+'/' + str(sUrle)
    _parseMovieList(sUrl, Page, sUrle)
    
def __nextPage():
    oParams = ParameterHandler()
    Page = oParams.getValue('iPage')
    sUrle = oParams.getValue('siteUrl')
    Page = int(Page) + 1
    sUrl = sUrle+'page/'+str(Page)+'/'
    Search = False
    _parseMovieList(sUrl, Page, Search)
	
def __getTotalPages(url, Page):
    oRequestHandler = cRequestHandler(url)
    sHtmlContent = oRequestHandler.request()
    sPattern = '<span.class=.pages.>Page.*?of.([0-9,]+)<'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        iTotalCount = str(aResult[1][0])
        iTotalCount = iTotalCount.replace (',', '')
    return iTotalCount
    return 0
	
def gotoPage():
    oGui = cGui()
    params = ParameterHandler()
    iTotalPages = params.getValue('iTotalPages')
    sUrle = params.getValue('siteUrl')
    
    pageNum = oGui.showNumpad()
    if (not pageNum) or (int(pageNum) > int(iTotalPages)):
        return
    sUrl = sUrle+'page/'+str(pageNum)+'/'
    Search = False
    _parseMovieList(sUrl, int(pageNum), Search)
    oGui.setEndOfDirectory()
    
def gotoPageSearch():
    oGui = cGui()
    params = ParameterHandler()
    iTotalPages = params.getValue('iTotalPages')
    sUrle = params.getValue('searchUrl')
    
    pageNum = oGui.showNumpad()
    if (not pageNum) or (int(pageNum) > int(iTotalPages)):
        return
    sUrl = URL_MAIN +'page/'+str(pageNum)+'/' + str(sUrle)
    _parseMovieList(sUrl, int(pageNum), str(sUrle))
    oGui.setEndOfDirectory()	
#---------------------------------------------------------------------   
  
def getHosters():
    oParams = ParameterHandler() #Parameter laden
    sUrl = oParams.getValue('movieUrl') # Weitergegebenen Urlteil aus den Parametern holen
  
    oRequestHandler = cRequestHandler(sUrl) # gesamte Url zusammesetzen
    sHtmlContent = oRequestHandler.request()         # Seite abrufen

    # andere Links sPattern = '<iframe src="([^"]+)"'
    sPattern = '(?:all/.file=|<iframe src="|<embed src=")([^"]+)"'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    hosters = []                                     # hosterliste initialisieren
    sFunction='getHosterUrl'                         # folgeFunktion festlegen
    if (aResult[0] == True):
        for aEntry in aResult[1]:
            hoster = {}
            hoster['link'] = aEntry
            # extract domain name
            temp = aEntry.split('//')
            temp = str(temp[-1]).split('/')
            temp = str(temp[0]).split('.')
            hoster['name'] = temp[-2]
            hosters.append(hoster)
        hosters.append(sFunction)
    return hosters
  
def getHosterUrl(sStreamUrl = False):

   if not sStreamUrl:
       params = ParameterHandler()
       sStreamUrl = oParams.getValue('url')
   results = []
   result = {}
   result['streamUrl'] = sStreamUrl
   result['resolved'] = False
   results.append(result)
   return results