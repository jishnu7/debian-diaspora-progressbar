#!/usr/bin/python

import re, sys
from jinja2 import Template, Environment, FileSystemLoader

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

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('main.html')
render = template.render(locals())

with open("status.html", "w") as file:
    file.write(render)
