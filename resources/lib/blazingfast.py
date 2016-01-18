# -*- coding: utf-8 -*-
import urllib2, re
from binascii import unhexlify
from binascii import hexlify
from Crypto.Cipher import AES
from resources.lib import logger

COOKIE_NAME = 'BLAZINGFAST-WEB-PROTECT'

def check(content):
    '''
    returns True if there seems to be a protection 
    '''
    return COOKIE_NAME in content

#not very robust but lazieness...
def getCookie(content):
    vars = re.findall('toNumbers\("([^"]+)"',content)
    if not vars:
        logger.info('vars not found')
        return False
    print vars
    value = _decrypt(vars[2], vars[0], vars[1])
    if not value:
        logger.info('value decryption failed')
        return False
    pattern = '"%s=".*?";([^"]+)"' % COOKIE_NAME
    cookieMeta = re.findall(pattern,content)
    if not cookieMeta:
        logger.info('cookie meta not found')
    cookie = "%s=%s;%s" % (COOKIE_NAME, value, cookieMeta)
    return cookie
    # + toHex(BFCrypt.decrypt(c, 2, a, b)) +

def _decrypt(t, o, n):
    t = unhexlify(t)
    o = unhexlify(o)
    n = unhexlify(n)
    if len(n) != 16:
        print"iv length is" + str(len(n)) +" must be 16."
        return False
    aes = AES.new(o, AES.MODE_CBC, n)
    f = hexlify(aes.decrypt(t[0:16]))
    return f 