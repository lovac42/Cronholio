# Cronholio: Cron Task Scheduler (beta)

Labeled as beta due to timezone/locale/DST uncertainties. But otherwise, <i>fairly harmless.</i>


## About:
This addon designates the current card in the reviewer as a cron card. A cron card follows a schedule from the assigned expression. This is useful for reminders and small notes kept in flashcards.  

<b>Expression Syntax:</b>  
<b>@daily</b>: Repeats the card once per day.  
<b>@hourly</b>: Repeats the card every hour.  

<i>min hrs dom mon dow</i>  
<b>&ast;/15 &ast; &ast; &ast; &ast;</b>: Every 15 minutes.  
<b>&ast;  &ast;/3 &ast; &ast; &ast;</b>: Every 3 hours.  
<b>0 0 1 &ast; &ast;</b>: Every 1st of the month.  
<b>0 0 &ast; &ast; 1</b>: Every Monday.  
<b>0 0 &ast; &ast; 2,4,6</b>: Every Tue, Thur, Sat.  
<b>0 0 &ast; &ast; 1-3,5</b>: Every Mon to Wed and Fri.  
<b>0 0 &ast; &ast; 5#3</b>: 3rd Fri of the month.  
<b>0 0 L &ast; &ast;</b>: Last day of the month.  

For more info see here: https://en.wikipedia.org/wiki/Cron


## Schedules:
Reviews will be scheduled based on Anki's notion of time and timezones. Day scheduled cards are converted to review cards (Anki-time) and intraday scheduled cards are converted to learning cards following Unix Epoch time. Any time specific information beyond "today" is discarded, as Anki-time only records dates.

Also, scheduling a card for the next day will not show up until 4 AM under Anki's default config settings. This can be changed under the "Next day starts at" option in preferences.


## User Data:
Cron table is saved in user's media folder in a file called "_crontab".  
Backups are named "_crontab.bak" and "_crontab.ba2"  


## Conflicts:
Problems with other button timer manipulation addons could be resolved by changing the addon file/folder name so that cronholio gets loaded first before any other addons.


## Logging:
Since these are scheduled task without any changes to interval, no logging methods are coded in this addon.


## Screenshots:
<img src="https://github.com/lovac42/Cronholio/blob/master/screenshots/menuoptions.png?raw=true"/>  
  
<img src="https://github.com/lovac42/Cronholio/blob/master/screenshots/menuoptions21.png?raw=true"/>  


## API Used:
croniter: https://github.com/taichino/croniter

