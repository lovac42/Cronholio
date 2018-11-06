# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Cronholio
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.5


from aqt import mw
from anki.hooks import wrap
from aqt.reviewer import Reviewer
from .cronholio import Cronholio
from .const import *
import anki.sched
import time


cronholio = Cronholio()


################################################################
#  Monkey Patchers Below
################################################################

#Saved crontab whenever col is saved
def col_save(self, name=None, mod=None):
    cronholio.crontab.dumpTab()


#Handing keybinds Anki2.0
def keyHandler(self, evt, _old):
    if unicode(evt.text()) == cronholio.hotkey:
        cronholio.set(mw.reviewer.card)
    else: _old(self, evt)

#Handing keybinds Anki2.1
def shortcutKeys(self, _old): 
    ret=_old(self)
    ret.append((cronholio.hotkey,lambda:cronholio.set(mw.reviewer.card)))
    return ret


def answerButtonList(self, _old):
    if not cronholio.cronCard:
        return _old(self)
    return ((1, _('UnCron')),
            (2, _('NxCron')),
            (3, _('Skip'))  )


def buttonTime(self, i, _old):
    if not cronholio.cronCard:
        return _old(self, i)
    if i==1: return "<i>%s&nbsp;&nbsp;</i><br>"%cronholio.cronExp
    if i==2: return "[<b>%s</b>]<br>"%cronholio.cronDue
    if i==3: return "10m<br>"


def answerButtons(self, card, _old):
    if not cronholio.cronCard:
        return _old(self, card)
    return 3


def answerCard(self, card, ease, _old):
    if not cronholio.cronCard:
        return _old(self, card, ease)

    self.col.log()
    assert ease >= 1 and ease <= 3
    self.col.markReview(card) #for undo

    if ease==1:
        cronholio.unset(card)
    elif ease==2:
        #initialize new cards just in case
        if card.type!=2:
            card.ivl=1
            card.factor=2500
        cronholio.setCardDue(card) #flushed()
    else: #pass for later
        card.due=int(time.time()+600) #10m
        card.left=1001
        card.queue=1
        card.flushSched()

    #No logging since IVL is unchanged


anki.collection._Collection.save = wrap(anki.collection._Collection.save, col_save, 'after')
Reviewer._answerButtonList = wrap(Reviewer._answerButtonList, answerButtonList, 'around')
Reviewer._buttonTime = wrap(Reviewer._buttonTime, buttonTime, 'around')
anki.sched.Scheduler.answerButtons = wrap(anki.sched.Scheduler.answerButtons, answerButtons, 'around')
anki.sched.Scheduler.answerCard = wrap(anki.sched.Scheduler.answerCard, answerCard, 'around')
if ANKI21:
    import anki.schedv2
    anki.schedv2.Scheduler.answerCard = wrap(anki.schedv2.Scheduler.answerCard, answerCard, 'around')
    anki.schedv2.Scheduler.answerButtons = wrap(anki.schedv2.Scheduler.answerButtons, answerButtons, 'around')
    Reviewer._shortcutKeys = wrap(Reviewer._shortcutKeys, shortcutKeys, 'around')
else:
    Reviewer._keyHandler = wrap(Reviewer._keyHandler, keyHandler, 'around')

