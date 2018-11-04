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
<b>&ast; &ast; 1 &ast; &ast;</b>: Every 1st of the month.  
<b>&ast; &ast; &ast; &ast; 1</b>: Every Monday.  

Reviews will be scheduled based on Anki's notion of time and timezones. And currently, Anki does not keep time delays beyond the cutoff limit. So any specific time set beyond 1 day is discarded. Also, scheduling a card at 12:20 AM will not show up until 4 AM under Anki's default config settings. This can be changed under the "Next day starts at" option in preferences.

## Settings:
Cron table is saved in user's media folder in a file called "_crontab".  
Backups are named "_crontab.bak" and "_crontab.ba2"  

## Conflicts:
Problems with other button timer manipulation addons could be resolved by changing the addon file/folder name so that cronholio gets loaded first before any other addons.

## Screenshots:
<img src="https://github.com/lovac42/Cronholio/blob/master/screenshots/menuoptions.png?raw=true"/>  
<img src="https://github.com/lovac42/Cronholio/blob/master/screenshots/menuoptions21.png?raw=true"/>

## API Used:
croniter: https://github.com/taichino/croniter
