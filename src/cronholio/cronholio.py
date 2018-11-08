# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Cronholio
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.7


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import getText, tooltip, showText
from codecs import open
from anki.utils import json
from datetime import datetime
import time

from .lib.croniter import croniter
from .lib.dateutil.tz import tz
from .crontab import Crontab
from .util import loadFile
from .const import *


class Cronholio(object):
    tagNote   = False
    hotkey    = None
    macros    = {}

    crontab   = Crontab()
    cronCard  = False
    cronDue   = ''
    cronExp   = ''


    def __init__(self):
        addHook("Reviewer.contextMenuEvent", self.showContextMenu)
        addHook('showQuestion', self.onShowQuestion)
        addHook('profileLoaded', self._loadMacros)

    def showContextMenu(self, r, m):
        a=m.addAction("Add Cron Task")
        a.setShortcut(QKeySequence(self.hotkey))
        a.triggered.connect(lambda:self.set(r.card))

    def onShowQuestion(self):
        card=mw.reviewer.card
        conf=mw.col.decks.confForDid(card.did)
        if (not card.odid or conf['resched']) and \
        self.crontab.contains(card.id):
            self.cronCard=True
            self.cronDue=self.nextDue(card.id)
            self.cronExp=self.crontab.contains(card.id)
        else:
            self.cronCard=False

    def set(self, card):
        task=self.crontab.contains(card.id)
        if not task: task='0 0 * * *'
        exp, ok = getText("m  h  dom  mon  dow | @daily | @hourly", default=task)
        if ok:
            exp=self.checkMacro(exp)
            if self.crontab.set(card.id,exp):
                if self.tagNote:
                    n=card.note()
                    n.addTag('@cronCard')
                    n.flush()
                tooltip(_("Cron card created"), period=1000)
                mw.reset()

    def checkMacro(self, exp):
        exp=exp.strip()
        if not exp.startswith('@') and '*' not in exp:
            e=self.macros.get(exp, None)
            if e: return e

            exp=exp.lower()
            e='0 0 * * %s'%exp #mon,wed,fri
            if croniter.is_valid(e): return e
            e='0 0 %s *'%exp #jan,feb
            if croniter.is_valid(e): return e
        return exp

    def unset(self, card):
        self.crontab.unset(card.id)
        self.cronCard=False
        if self.tagNote:
            n=card.note()
            n.delTag('@cronCard')
            n.flush()
        tooltip(_("Cron card removed"), period=1000)

    def nextDue(self, cid):
        dt=self.crontab.getDateTime(cid)
        tm=self._getTime(dt)
        tod=time.localtime(tm)
        if not self._getDueDay(dt):
            return time.strftime(_("%H:%M"), tod)
        return time.strftime(_("%m/%d/%Y"), tod)

    def setCardDue(self, card):
        dt=self.crontab.getDateTime(card.id)
        dd=self._getDueDay(dt)
        if not dd: #same day delays
            tm=self._getTime(dt)
            card.due=int(tm)
            card.queue=1
            card.left=1001
        else:
            card.due=dd+mw.col.sched.today
            card.type=card.queue=2
        card.flushSched()

    def _getDueDay(self, dt):
        d=datetime.today()
        today=datetime(d.year, d.month, d.day)
        due=datetime(dt.year, dt.month, dt.day)
        diff=(due-today).days
        return diff

    def _getTime(self, dt):
        tm=time.mktime(dt.timetuple())
        return tm

    def _loadMacros(self, config=None):
        if not config:
            try:
                config=mw.addonManager.getConfig(__name__)
            except AttributeError:
                data=loadFile('','config.json')
                config=json.loads(data)

        self.hotkey=config['hotkey']
        self.tagNote=config['add_tag_to_notes_even_multi_cards']
        self.macros=config['macros']

        try: #Must be loaded after profile loads, after addonmanger21 loads.
            mw.addonManager.setConfigUpdatedAction(__name__, self._loadMacros) 
        except AttributeError: pass

