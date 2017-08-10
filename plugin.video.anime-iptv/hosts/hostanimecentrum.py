# -*- coding: utf-8 -*-
###############################################################################
###############################################################################
# Anime-Centrum
# THANKS for support to samsamsam !!!!
# Some part of code comes from iptvplugin https://gitlab.com/iptvplayer-for-e2/iptvplayer-for-e2
###############################################################################
###############################################################################
### Imports ###
import re
import xbmcaddon
import os
import sys
import requests

from common import (_addon, addpr, nURL, eod, set_view, addst, addonPath, GetDataBeetwenMarkers, tfalse, ParseDescription)
from contextmenu import ( ContextMenu_Series, ContextMenu_Episodes)
try:
    import json
except:
    import simplejson as json

__settings__ = xbmcaddon.Addon(id="plugin.video.anime-iptv")
addonPath = __settings__.getAddonInfo('path')
sys.path.append(os.path.join(addonPath, 'crypto'))


### ##########################################################################
### ##########################################################################
site = addpr('site', '')
section = addpr('section', '')
url = addpr('url', '')
mainSite = 'http://anime-centrum.pl'
fanartAol = addonPath + '/art/japan/fanart.jpg'
nexticon = addonPath + '/art/next.png'
host = 'animecentrum'


def Pageanimecentrum(url, page, metamethod=''):
    headers = {
        'Pragma': 'no-cache',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
    }
    s = requests.Session()
    r = s.get('http://anime-centrum.pl/', headers=headers)
    lista = re.compile('<meta name="csrf-token" content="(.+?)">').findall(r.text)
    for item in lista:
        token = item
    headers = {
            'Pragma': 'no-cache',
            'Origin': 'http://anime-centrum.pl',
            'Accept-Encoding': 'gzip, deflate',
            'X-CSRF-TOKEN': token,
            'Accept-Language': 'pl-PL,pl;q=0.8,en-US;q=0.6,en;q=0.4',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Cache-Control': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Referer': 'http://anime-centrum.pl/',
    }
    data = [
          ('title', 'none'),
          ('letter', page),
          ('species', 'none'),
          ('type', 'none'),
          ('season', 'none'),
          ('year', 'none'),
        ]
    r = requests.post('http://anime-centrum.pl/anime/online/pl/list/search', headers=headers, cookies=s.cookies, data=data)
    r = r.text
    r = r.replace('\\n', '')
    r = r.replace('\\t', '')
    r = r.replace('\\', '')
    Browse_ItemAnimecentrum(r, url, metamethod)
    eod()


def Browse_ItemAnimecentrum(html, url, metamethod='', content='movies', view='515'):
    if (len(html) == 0):
        return
    data = re.findall('tb-cell"><a href="(.+?)"><img src="(.+?)" alt="(.+?)"><\/a>', html)
    ItemCount = len(data)
    for item in data:
        strona = mainSite + item[0]
        strona = strona + '?page=1'
        name = item[2].encode("utf-8")
        name = ParseDescription(name)
### scraper
        if (tfalse(addst("acentr-thumbs")) == True):
            import scraper
            scrap = scraper.scraper_check(host, name)
            try:
                if (name not in scrap):
                    html = nURL(strona)
                    html = GetDataBeetwenMarkers(html, '<article class="content-1">', '<section class="gap-2">', False)[1]
                    data = re.findall('<img src="(.+?)" alt=', html)
                    ItemCount = len(data)
                    if len(data) > 0:
                        for item in data:
                            img = item
                    else:
                        img = ''
                    data = re.findall('<p>(.+?)</p>', html)
                    ItemCount = len(data)
                    if len(data) > 0:
                        for item in data:
                            plot = item
                            plot = ParseDescription(item)
                    else:
                        plot = ''
                    scraper.scraper_add(host, name, img, plot, '')
                    scrap = scraper.scraper_check(host, name)
            except:
                scrap = ''
            try:
                img = scrap[1]
            except:
                img = ''
            try:
                plot = scrap[2]
            except:
                plot = ''
        else:
            img = ''
            plot = ''
        fanart = fanartAol
        labs = {}
        try:
            labs['plot'] = plot
        except:
            labs['plot'] = ''
###
        pars = {'mode': 'EpisodesAnimecentrum', 'site': site, 'section': section, 'title': name, 'url': strona, 'img': img, 'fanart': fanart}
        contextLabs = {'title': name, 'url': strona, 'img': img, 'fanart': fanart, 'todoparams': _addon.build_plugin_url(pars), 'site': site, 'section': section, 'plot': labs['plot']}
        if section == 'animecentrum':
            contextMenuItems = ContextMenu_Series(contextLabs)
        else:
            contextMenuItems = []
        labs['title'] = name
        _addon.add_directory(pars, labs, is_folder=True, fanart=fanart, img=img, contextmenu_items=contextMenuItems, total_items=ItemCount)
    set_view(content, view_mode=addst('tvshows-view'))


def Browse_EpisodesAnimecentrum(url, page='', content='episodes', view='515'):
    if url == '':
        return
    html = nURL(url)
    data = re.findall('<a href="(.+?)" title="(.+?)"><h2>', html)
    ItemCount = len(data)
    for item in data:
        url2 = mainSite + item[0]
        name = item[1].encode("utf-8")
        name = ParseDescription(name)
        img = ""
        fanart = fanartAol
        plot = ""
        labs = {}
        try:
            labs['plot'] = plot
        except:
            labs['plot'] = ''
###
        contextLabs = {'title': name, 'year': '0000', 'url': url2, 'img': img, 'fanart': fanart, 'DateAdded': '', 'plot': labs['plot']}
        contextMenuItems = ContextMenu_Episodes(labs=contextLabs)
        pars = {'mode': 'PlayAnimecentrum', 'site': site, 'section': section, 'title': name, 'url': url2, 'img': img, 'fanart': fanart}
        labs['title'] = name
        _addon.add_directory(pars, labs, is_folder=False, fanart=fanart, img=img, contextmenu_items=contextMenuItems, total_items=ItemCount)
# next page
    npage = url[:-1] + str(int(url[-1:]) + 1)
    if -1 != html.find("pagination"):
        _addon.add_directory({'mode': 'EpisodesAnimecentrum', 'site': site, 'section': section, 'url': npage, 'page': npage}, {'title': "Next page"}, is_folder=True, fanart=fanartAol, img=nexticon)
    eod()


def getItemTitles(table):
    out = []
    for i in range(len(table)):
        value = table[i]
        out.append(value[0])
    return out


def Browse_PlayAnimecentrum(url, page='', content='episodes', view='515'):
    if url == '':
        return
    html = nURL(url)
    lista = re.compile('<source src="(.+?)" type="(.+?)">').findall(html)
    lista = [tuple(reversed(t)) for t in lista]
    import xbmcgui
    d = xbmcgui.Dialog()
    item = d.select("Wybór źrodła", getItemTitles(lista))
    if item != -1:
        player = str(lista[item][1])
        url = player
        from common import PlayFromHost
        PlayFromHost(url)
    eod()
