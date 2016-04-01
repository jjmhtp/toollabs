#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Bot to import KMSKA stuff

The bot takes three csv files:
* One with the artists
* One with the type of works
* One with all the works

Combines these and uploads the data to Wikidata
"""
import artdatabot
#import json
import pywikibot
#from pywikibot import pagegenerators
#import urllib2
#import re
#import pywikibot.data.wikidataquery as wdquery
#import datetime
#import HTMLParser
#import posixpath
#from urlparse import urlparse
#from urllib import urlopen
#import hashlib
#import io
#import base64
#import upload
#import tempfile
import os
import csv



def getKMSKAGenerator():
    '''
    Generator that combines 3 csv files and returns dicts
    '''

    artists = {}
    objectnames = {}
    
    # Open the artists and dump it in a dict id -> qid

    with open('kmska_artist_completed.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            artists[row.get('creatorId')] = row.get('creatorWikidataPid').replace('http://www.wikidata.org/entity/', '').replace('http://www.wikidata.org/wiki/', '')

    #print artists
    with open('KMSKA objectnames gematched met Wikidata.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            objectnames[row.get('objectNameId')] = row.get('Wikidata Q')

    foundit=True
    #print objectnames
    with open('KMSKA_import_wikidata_29102015-bd-corrected poetsbeurt 2 SF.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            metadata = {}

            metadata['collectionqid'] = u'Q1471477'
            metadata['collectionshort'] = u'KMSKA'
            metadata['locationqid'] = u'Q1471477'
            
            metadata['id'] = unicode(row.get('objectNumber'), u'utf-8')
            metadata['idpid'] = u'P217'
            metadata['title'] = { u'nl' : unicode(row.get('title'), u'utf-8') } # Hier iets met Nederlands doen

            # Welcome in URL hell.
            # Data url in the reference
            metadata['refurl'] = unicode(row.get('dataPid'), u'utf-8')
            # The Pid url for described by url
            metadata['describedbyurl'] = unicode(row.get('workPid'), u'utf-8')
            # The Pid url for the inventory number reference
            metadata['idrefurl'] = unicode(row.get('workPid'), u'utf-8')
            # This shouldn't actually be used
            metadata['url'] = unicode(row.get('workPid'), u'utf-8')

            metadata['creatorname'] = unicode(row.get('creator'), u'utf-8')
            metadata['objectname'] = unicode(row.get('objectName'), u'utf-8')
            if metadata['creatorname'] and metadata['objectname']:
                metadata['description'] = { u'nl' : u'%s van %s' % (metadata['objectname'], metadata['creatorname']) }
                if metadata['objectname']==u'schilderij':
                    metadata['description']['en'] = u'painting by %s' % (metadata['creatorname'],)
                elif metadata['objectname']==u'beeldhouwwerk':
                    metadata['description']['en'] = u'sculpture by %s' % (metadata['creatorname'],)
                elif metadata['objectname']==u'aquarel':
                    metadata['description']['en'] = u'watercolor painting by %s' % (metadata['creatorname'],)
                    
            if row.get('creatorId') in artists:
                metadata['creatorqid'] = artists.get(row.get('creatorId'))
            metadata['objectname'] = unicode(row.get('objectName'), u'utf-8')
            if row.get('objectNameId') in objectnames:
                metadata['instanceofqid'] = objectnames.get(row.get('objectNameId'))

            if row.get('dateIso8601'):
                metadata['inception'] = unicode(row.get('dateIso8601'), u'utf-8')

            # Start with only paintings
            #workwork = [#u'schilderij',
            #            u'beeldhouwwerk',
            #            u'aquarel',
            #            ]
            #if metadata['objectname'] in workwork:
            if metadata['id']=='11075-11090':
                foundit=True
            if foundit:
                yield metadata
            
        

def main():
    dictGen = getKMSKAGenerator()

    #for painting in dictGen:
    #    print painting

    artDataBot = artdatabot.ArtDataBot(dictGen, create=True)
    artDataBot.run()
    
    

if __name__ == "__main__":
    main()
