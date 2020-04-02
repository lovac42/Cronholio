# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/Cronholio
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os, time
from aqt import mw
from anki.hooks import addHook
from datetime import datetime
from codecs import open
from shutil import copyfile

from .util import loadFile
from .lib.com.lovac42.anki.version import ANKI20
from .lib.croniter import croniter

# from aqt.utils import showWarning, showInfo, showText, getText, tooltip


class Crontab(object):
    _modified=False
    _entries={}

    def __init__(self):
        addHook('profileLoaded', self.initTab)
        addHook('unloadProfile', self.dumpTab)

    def getTime(self, cid):
        dt=self.getDateTime(cid)
        # py3.3+: datetime.timestamp
        return time.mktime(dt.timetuple())

    def getDateTime(self, cid):
        exp=self.get(cid)
        c=croniter(exp, datetime.now())
        return c.get_next(datetime)

    def get(self, cid):
        exp=self._entries[cid]
        return self.decode(exp)

    def set(self, cid, exp):
        if self.check(exp):
            if self.contains(cid): #clear double entries in _crontab
                self._modified=True
            self._entries[cid]=exp
            self.recordTask(cid,exp)
            return exp

    def unset(self, cid):
        self._entries.pop(cid, None)
        self._modified=True

    def contains(self, cid):
        return self._entries.get(cid, False)

    def recordTask(self, cid, exp):
        "Write single exp to file"
        mediaFolder=os.path.join(mw.pm.profileFolder(), 'collection.media')
        fname=mediaFolder+'/_crontab'
        if not os.path.exists(fname):
            self._modified=True
            self.dumpTab()
        else:
            with open(fname, 'a', encoding='utf-8') as f:
                f.write('%s cid_%s\n'%(exp,cid))
                f.close()

    def dumpTab(self):
        "Dump data to file"
        if not self._modified: return
        mediaFolder=os.path.join(mw.pm.profileFolder(), 'collection.media')
        fname=mediaFolder+'/_crontab'
        if os.path.exists(fname):
            copyfile(fname, fname+'.ba2') #2nd backup

        with open(fname, 'w', encoding='utf-8') as f:
            #load template from addon folder
            header=loadFile('template','_crontab')
            f.write(header)

            if ANKI20: #python 2.x 
                for k,v in self._entries.viewitems():
                    f.write('%s cid_%s\n'%(v,k))
            else: #python 3.3+
                for k,v in self._entries.items():
                    f.write('%s cid_%s\n'%(v,k))

            f.close()
        self._modified=False

    def initTab(self):
        "Read data from file"
        self._entries={}
        mediaFolder=os.path.join(mw.pm.profileFolder(), 'collection.media')
        data=loadFile(mediaFolder,'_crontab')
        if data:
            for line in data.split('\n'):
                if not line: continue
                if line.lstrip().startswith('#'): continue
                v,k = line.split(' cid_')
                self._entries[int(k)]=v

            #Make backup on load
            fname=mediaFolder+'/_crontab'
            copyfile(fname, fname+'.bak') #init backup

    def check(self, exp):
        exp=self.decode(exp)
        return croniter.is_valid(exp)

    def decode(self, exp):
        if '@' in exp:
            exp=exp.strip().lower()
            if exp == "@hourly": return "0 * * * *"
            if exp == "@daily":  return "0 0 * * *"
        return exp

