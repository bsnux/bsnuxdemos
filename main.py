#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""BSNUX Software Factory Demos (www.bsnux.com)

   Author: Arturo Fernandez (arturo@bsnux.com)
   Date: October, 2009
   License: GPL v3
   
"""
import os
import urllib
import urllib2
import logging
import wsgiref.handlers
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from django.utils import simplejson


class MainHandler(webapp.RequestHandler):
  """MaindHandler to response to requests

  Includes last.fm key to do different request
  
  """
  LASTFM_API_KEY = '03e2166c76b08fceb8284a9823592b61'
  
  def __getTweets(self):
    """Return last 10 tweets from Twitter.com

       If exception return an empty array
    """
    posts = []
    params = {'q' : 'from:arturofm', 'page' : '1', 'rpp': '10'}
    url = 'http://search.twitter.com/search.json?'
    url = url + urllib.urlencode(params)
    
    try:
      res = urllib2.urlopen(url)
      data = simplejson.load(res)
      posts = data['results']
    except Exception:
      posts = []

    return posts

  def __getArtistBio(self, artist):
    """Return a paragraph with information about an artist

    Keyword arguments:
    artist -- Artist name from other different request

    """
    try:
      url = 'http://ws.audioscrobbler.com/2.0/?'
      params = {'method' : 'artist.getinfo', 'artist' : artist,
                'api_key': self.LASTFM_API_KEY, 'format' : 'json'}
      logging.debug(artist)
      url = url + urllib.urlencode(params)
      res = urllib2.urlopen(url)
      data = simplejson.load(res)
      return data['artist']['bio']['summary']
    except:
      raise Exception

  def __getArtists(self):
    """Return an array with most popular artist from Last.fm

    """
    artists = []
    url = 'http://ws.audioscrobbler.com/2.0/?'
    params = {'method' : 'user.gettopartists', 'user' : 'artufm',
              'api_key': self.LASTFM_API_KEY, 'format' : 'json', 'period' : '3month'}

    try:
      url = url + urllib.urlencode(params)
      res = urllib2.urlopen(url)
      data = simplejson.load(res)
      artist = data['topartists']
      theArtists = artist['artist']
      for a in theArtists:
        item = a
        item['imgURL'] = a['image'][2]['#text']
        item['bio'] = self.__getArtistBio(a['name'])
        artists.append(item)
    except Exception:
      artists = []

    return artists

  def get(self):
    """Main entry point for "/"
    
    """
    # Template
    template_values = {'posts': self.__getTweets(),
                       'artists': self.__getArtists()}
    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

def main():
  # Main actions to lauch application
  logging.getLogger().setLevel(logging.DEBUG)
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
