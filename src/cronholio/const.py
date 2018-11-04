# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/Cronholio
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.1



# == User Config =========================================

HOTKEY = ''

#Tags are applied to notes, multi cron cards could be affected.
#Only use this if you have one card per note.
AUTO_ADD_RM_TAGS = False


# == End Config ==========================================
##########################################################

from anki import version
ANKI21 = version.startswith("2.1.")
