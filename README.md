# Hugo Helper 

A [Sublime Text 2/3](http://www.sublimetext.com/) plugin for assiting in writing posts for a Hugo blog.

# Installation

 ## Package Control

Currently doesn't exist in Package Control
<!--
Install [Package Control](http://wbond.net/sublime_packages/package_control). HugoHelper will show up in the package list. This is the recommended installation method.
-->
## Manual installation

Go to the "Packages" directory (`Preferences` / `Browse Packages…`). Then clone this repository:

    git clone git://github.com/srgrn/HugoHelper

# Usage

Currently this plugin contains two commands both in the command palette under Hugo Helper:

1. hugo_helper_insert_summary_break - inserts a summary break (<!--more-->) to a post 
1. hugo_helper_publish_post - change post draft status to false and updates the date to current time.

# Default key bindings:

## Insert Summary break ( <!--more-->) to current line

* Windows and Linux: `Ctrl+B` `Ctrl+C`
* OS X: `Super+B` `Super+C`

## Change a post front matter so it has draft=false and updates the date.

* Windows and Linux: `Ctrl+B` `Ctrl+P`
* OS X: `Super+B` `Super+P`

# Information

Source: https://github.com/csrgrn/HugoHelper

Author: [Eran Zimbler](https://github.com/srgrn/)