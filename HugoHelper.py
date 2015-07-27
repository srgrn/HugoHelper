import sublime
import sublime_plugin
from datetime import datetime


class HugoHelperPublishPostCommand(sublime_plugin.TextCommand):

    def set_draft_status(self, edit, target):
        region = self.view.find('draft\s=\s.*$', 0)
        if not region.empty():
            self.view.replace(edit, region, 'draft = ' + target)

    def set_date(self, edit):
        region = self.view.find('date\s=\s".*"$', 0)
        if not region.empty():
            now = datetime.now()
            current = self.view.substr(region)
            tz = '+' + current.split('+')[1]
            print (now)
            self.view.replace(edit, region, 'date = "' + now.strftime("%Y-%m-%dT%H:%M:%S") + tz)

    def run(self, edit):
        self.set_draft_status(edit, 'false')
        self.set_date(edit)


class HugoHelperInsertSummaryBreakCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                self.view.insert(edit,line.begin(), '<!--more-->\n')
