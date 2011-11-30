#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import cookielib, re
from urllib import urlencode
from urllib2 import build_opener, HTTPCookieProcessor, HTTPRedirectHandler, Request

from path import path
import lxml, lxml.html
from pyquery import PyQuery

import yaml
def toyaml(*records, **kw):
    if kw: records += (kw,)
    return yaml.safe_dump_all(records, indent=4, default_flow_style=False)



CHROME_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.15 Safari/535.7'
BASE_HEADERS = {
    'User-Agent'      : CHROME_UA,
    'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language' : 'en-us,en;q=0.5',
    'Accept-Charset'  : 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'
}

DOCTYPE_PAT = re.compile(r'<!DOCTYPE[^\>]*>', re.I)

def create(base=None, headers={}, cookies=None, cookie_file=None, debug=False):
    jar = cookielib.LWPCookieJar()
    if cookie_file:
        jar.filepath = cookie_file
        if debug: print 'Loading cookies from %r...' % cookie_file
        jar.load(cookie_file)
        if debug: print repr(jar)
    elif cookies:
        jar._cookies = cookies
    
    o = build_opener( HTTPCookieProcessor(jar), HTTPRedirectHandler )
    
    hds = BASE_HEADERS.copy()
    hds.update(headers)
    o.addheaders = hds.items()
    
    def scrape(url, data=None, method=None, parse=False, pyquery=False):
        fullurl = base/url if base and not (url.startswith('http') or url.startswith(base)) else url
        if method is None:
            method = 'GET' if data is None else 'POST'
        method = str(method).upper()
        
        if data is not None and not isinstance(data, basestring):
            body = urlencode(data)
        else:
            body = data
        
        # Avoid POST request by attaching data
        if method == 'GET' and body is not None:
            fullurl += ('&' if '?' in fullurl else '?') + body
            body = None
        
        # Force POST request by supplying data
        if method == 'POST' and body is None:
            body = ''
        
        if debug:
            print '%s %s \n\t(url=%s, data=%r)...\nHeaders:\n' % (method, fullurl, url, data)
            print '%s %s' % (method, fullurl)
            print toyaml( Request=dict(url=url, data=data, body=body) )
            print toyaml( Headers=dict(o.addheaders) )
            print
        
        req = res = o.open(fullurl, body)
        
        if parse or pyquery:
            text = req.read()
            text = DOCTYPE_PAT.sub('', text)
            res = lxml.html.fromstring(text)
        if pyquery:
            res = PyQuery(res)
        
        return res
    
    def saveCookies(self, cookie_file=None):
        cookie_file = cookie_file or getattr(jar, 'filepath', None)
        if not cookie_file:
            raise Error('Please specify a file to load cookies from!')
        jar.save(cookie_file)
        return jar
    
    o.scrape = scrape
    o.saveCookies = saveCookies
    o.jar = jar
    return o


def scrape(url, data=None, method=None, parse=False, pyquery=False, **create_args):
    return create(**create_args).scrape(url, data, method, parse, pyquery)


