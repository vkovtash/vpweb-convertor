#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'kovtash'

POSTER_DIR = '/Users/kovtash/vpweb/poster'

import os,re

class vpwebFileInfo():
    def __init__(self,filePath):

        self._name=None
        self._season=None
        self._episode=None

        fileName=os.path.splitext(os.path.basename(filePath))[0]


        patterns=[re.compile('(?P<name>.*)S(?P<season>[\d]+)E(?P<episode>[\d]+)'),
                  re.compile('(?P<name>.*)S(?P<season>[\d]+).*'),
                  re.compile('(?P<name>.*)E(?P<episode>[\d]+).*')]

        fileInfo =None
        for pattern in patterns:
            fileInfo=pattern.search(fileName)

            if fileInfo is not None:
                break


        if fileInfo is not None:
            name=fileInfo.group('name')
            try:
                self._season=fileInfo.group('season')
            except IndexError:
                pass
            try:
                self._episode=fileInfo.group('episode')
            except IndexError:
                pass

        else:
            name=fileName


        currentName=str(name)
        currentName=currentName.replace('_',' ')
        currentName=currentName.strip(' ')
        self._name=currentName


    @property
    def name(self):
        return self._name

    @property
    def season(self):
        return self._season

    @property
    def episode(self):
        return self._episode

    @property
    def poster(self):
        posterPath=os.path.join(POSTER_DIR,self.name.replace(' ','_'))
        if os.path.exists(posterPath):
            return posterPath
        else:
            return None