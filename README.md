conky_wunderlist
================

conky_wunderlist is a simple python script to sync a to-do list from wunderlist to your linux machine and have it display, sorted by due date, in a crunchbang-styled conky configuration (I am using Arch linux with conky closely modeled after crunchbang).

[Here](http://imgur.com/TRO4a9K) is an example of how it looks on my machine:

**Requirements:**

Python 3.3

[Wunderpy] (https://github.com/bsmt/wunderpy) (Makes all this possible!): 

Here's how to set it up:

**[1]** Place the get_wunderlist_tasks.py script in a directory called ~/.conky_wunderlist (must be called this!)

**[2]** Have the script start at system startup as a background process.
For example, for my openbox setup, I add the following line to /.config/openbox/autostart:

```
python ~/conky_wunderlist/get_wunderlist_tasks.py <email> <password> <name of list to sync> <time in seconds between updates> <time in seconds to retry sync after a failed ping> &
```

(Don't forget the &, its really important. For my purposes I used 3600 and 600 for the time parameters, so that it will sync every hour but retry every 10 minutes if a sync fails.)

**[3]** Every time the script syncs your list, it writes it to the file ~/conky_wunderlist/task_list. Since we want this displayed in conky, add the following 3 lines to the TEXT section of your conkyrc file (normally located at ~/.conkyrc):
```
H O M E W O R K # or whatever title you want
${hr}
${execp cat ~/.conky_wunderlist/task_list}
```
**[4]** Now, the only thing left to do is make sure that conky has enough space to display what you want. I changed my conkyrc to include the following:

```
text_buffer_size 3000
minimum_size 280 1000
maximum_width 280
```

(you may have to screw around with this to get things to display properly)

**[5]** ta-da! Wunderlist task lists synced and displayed to your conky.
