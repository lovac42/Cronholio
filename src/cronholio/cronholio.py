# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Cronholio
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1


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
    today_crt = None #init to 12:00 AM of localtime
    crontab   = Crontab()
    cronCard  = False
    cronDue   = ''
    cronExp   = ''

    def __init__(self):
        addHook("Reviewer.contextMenuEvent", self.showContextMenu)
        addHook('showQuestion', self.onShowQuestion)

        d=datetime.today()
        d=datetime(d.year, d.month, d.day)
        self.today_crt=int(time.mktime(d.timetuple()))

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
        delay=self.crontab.getTime(cid)
        date=self._getDueDate(delay)
        tod=time.localtime(delay)
        if not date:
            return time.strftime(_("%H:%M"), tod)
        return time.strftime(_("%m/%d/%Y"), tod)

    def setCardDue(self, card):
        card.type=card.queue=2
        delay=self.crontab.getTime(card.id)
        card.due=self._getDueDate(delay)
        if not card.due: #same day delays
            card.due=delay
            card.queue=1
        card.flushSched()

    def _getDueDate(self, time):
        due=int(time-self.today_crt)//86400+mw.col.sched.today
        if due==mw.col.sched.today:
            return 0
        return due

