#!/usr/bin/python

import re, sys

"""
    Process dot file and categorize gems.
    Usage : ./process_dot.py file_name.dot
"""

dot_file_name = sys.argv[1]
dot_file = open(dot_file_name)
gem_list = set() # empty set
#color of node and status
colors = {\
'black': 'unpackaged',\
'orange': "ITP",\
'purple': "RFP",\
'yellow': "new",\
'green': "present"\
}

#add anything is quotes to set
matches=re.findall(r'\"(.+?)\"',dot_file.read())
for match in matches:
    gem_list.add(match)

# Remove colors, which is also in quotes
for color in colors:
    try:
        gem_list.remove(color)
    except KeyError: # if specific color is not defined, skip
        pass

dot_file.seek(0) # reset

#regular expression to match 
#"gem" [color="color"];
re1='.*?'	# Non-greedy match on filler
re2='((?:[a-z][a-z0-9_\-]+))'	# Word 1
re3='.*?'	# Non-greedy match on filler
re4='(color)'	# Variable Name 1
re5='.*?'	# Non-greedy match on filler
re6='((?:[a-z][a-z]+))'	# Word 2
regexp = re1+re2+re3+re4+re5+re6

matches=re.findall(regexp,dot_file.read())

gem_status = {}

#add gems who has color now
for match in matches:
    gem = match[0]
    color = match[-1]
    status = colors[color]
    gem_status[gem] = status

#Add unpackaged gems
for gem in gem_list:
    if gem not in gem_status:
        gem_status[gem] = colors['black']
        #print gem

# Calculate Completion. Those who are already packaged
# or waiting in new is in.
gem_done = 0
gem_not_done = 0
for gem in gem_list:
    if gem_status[gem] in ['new', 'present']:
        gem_done = gem_done + 1
    else:
        gem_not_done = gem_not_done + 1
total = gem_done+gem_not_done
percent_complete = (float(gem_done)/float(total))*100.0


status_file = open("status.html", "w")
status_file.write("<html>")
status_file.write("<head><link rel=\"stylesheet\" href=\"style.css\" type=\"text/css\"/><title>Debian Diaspora packaging status</title></head><body><div id=\"percent\">Progress : "+str(percent_complete)+"<br/>Done: "+str(gem_done)+"<br/>Not Done: "+str(gem_not_done)+"</div>")
for color in colors:
    status = colors[color]
    status_file.write("\n<table id="+status+"><tr><td class=\"title\">"+status+"</td></tr>")
    #if status is of current color, write
    for gem in gem_status:
        if gem_status[gem] == status:
            status_file.write('<tr><td class="gem">' + gem + '</tr></td>')
    status_file.write('\n</table>')
status_file.write("</body></html>")
status_file.close()
