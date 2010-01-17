# -*- mode: python; coding: utf-8; -*-
# vim: sw=4:expandtab:foldmethod=marker
#
# Copyright (c) 2003, Mathieu Fenniak
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
# * The name of the author may not be used to endorse or promote products
# derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
A simple library that implements a pingback client.  The library supports
version 1.0 of the pingback library, based upon the specification published
at http://www.hixie.ch/specs/pingback/pingback.

Implementing a pingback server is beyond the scope of this library simply
because of the very application-specific nature of a server.  However, it is
also trivially easy to create a pingback server by using Python's
SimpleXMLRPCServer module.  The following simple framework could be used
by a CGI script to implement a pingback server::

    def pingback(sourceURI, targetURI):
        '''Do something interesting!'''
        return "arbitrary string return value."

    import SimpleXMLRPCServer
    handler = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()
    handler.register_function(pingback, "pingback.ping")
    handler.handle_request()

It would still be necessary to provide an X-Pingback HTTP header which pointed
at the given CGI script.
"""
__author__ = "Mathieu Fenniak <laotzu@pobox.com>"
__date__ = "2003-01-26"
__version__ = "2003.01.26.01"

import re
import urllib2
import xmlrpclib
from HTMLParser import HTMLParser

def _reSTLinks(txt):
    reSTLink = re.compile("\n\\.\\.\\s+[^\n:]+:\s+(http://[^\n]+)", re.I)
    linkMatches = reSTLink.findall(txt)
    return linkMatches


class _LinkExtractor(HTMLParser, object):
    def __init__(self, links):
        super(_LinkExtractor, self).__init__()
        self.links = links

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for key, value in attrs:
                if key == "href" and value.startswith("http://"):
                    self.links.append(value)


def _htmlLinks(txt):
    links = []
    le = _LinkExtractor(links)
    le.feed(txt)
    le.close()
    return links


def _htmlPingbackURI(fileObj):
    """Given an interable object returning text, search it for a pingback URI
    based upon the search parameters given by the pingback specification.

    Namely, it should match the regex:
      <link rel="pingback" href="([^"]+)" ?/?>
    (source: http://www.hixie.ch/specs/pingback/pingback)

    We could search the text using an actual HTML parser easily enough, or
    expand the regex to be a little more forgiving, but for the moment we'll
    follow the spec."""
    regex = re.compile('<link rel="pingback" href="([^"]+)" ?/?>', re.I) # might as well be case-insensitive
    for line in fileObj:
        m = regex.search(line)
        if m != None:
            uri = m.group(1)
            # The pingback spec demands we expand the four allowed entities,
            # but no more.
            uri = uri.replace("&lt;", "<")
            uri = uri.replace("&gt;", ">")
            uri = uri.replace("&quot;", '"')
            uri = uri.replace("&amp;", "&")
            return uri
    return None


def _determinePingbackURI(uri):
    """Attempt to determine the pingback URI of the given url object.  First
    we try to find the X-Pingback server header, and then we resort to
    messier means if necessary.  See _htmlPingbackURI for those means."""
    try:
        pingbackURI = uri.info()['X-Pingback']
        return pingbackURI
    except KeyError:
        return _htmlPingbackURI(uri)


def _performXMLRPCQuery(sourceURI, targetURI, serverURI):
    rpcserver = xmlrpclib.ServerProxy(serverURI)
    rpcserver.pingback.ping(sourceURI, targetURI)


def pingback(sourceURI, targetURI):
    """Attempts to notify the server of targetURI that sourceURI refers to
    it."""
    url = urllib2.urlopen(targetURI)
    pingback = _determinePingbackURI(url)
    if pingback == None:
        return
    _performXMLRPCQuery(sourceURI, targetURI, pingback)


def autoPingback(sourceURI, reST = None, HTML = None):
    """Scans the input text, which can be in either reStructuredText or HTML
    format, pings every linked website for auto-discovery-capable pingback
    servers, and does an appropriate pingback.

    The following specification details how this code should work:
        http://www.hixie.ch/specs/pingback/pingback"""
    assert reST != None or HTML != None

    if reST != None:
        links = _reSTLinks(reST)
    else:
        links = _htmlLinks(HTML)

    for link in links:
        pingback(sourceURI = sourceURI, targetURI = link)


