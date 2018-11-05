# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Cronholio
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.3


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from aqt.utils import getText, tooltip
from codecs import open
from datetime import datetime
import time

from .lib.dateutil.tz import tz
from .crontab import Crontab
from .util import loadFile
from .const import *


class Cronholio(object):
    crontab   = Crontab()
    cronCard  = False
    cronDue   = ''
    cronExp   = ''

    def __init__(self):
        addHook("Reviewer.contextMenuEvent", self.showContextMenu)
        addHook('showQuestion', self.onShowQuestion)

    def showContextMenu(self, r, m):
        a=m.addAction("Add Cron Task")
        a.setShortcut(QKeySequence(HOTKEY))
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
        default=self.crontab.contains(card.id)
        if not default: default='* * * * *'
        exp, ok = getText("m  h  dom  mon  dow | @daily | @hourly", default=default)
        if ok and self.crontab.set(card.id,exp):
            if AUTO_ADD_RM_TAGS:
                n=card.note()
                n.addTag('@cronCard')
                n.flush()
            tooltip(_("Cron card created"), period=1000)
            mw.reset()

    def unset(self, card):
        self.crontab.unset(card.id)
        self.cronCard=False
        if AUTO_ADD_RM_TAGS:
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

