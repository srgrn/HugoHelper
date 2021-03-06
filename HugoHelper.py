import os
from datetime import datetime

import ast
import sublime
import sublime_plugin

DEFAULT_CONTENTS_DIR = "content"


def plugin_loaded():
    print('HugoHelper plugin_loaded')
    settings = sublime.load_settings('Hugo Helper.sublime-settings')


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

    def fix_title(self, edit):
        region = self.view.find('title\s=\s.*$', 0)
        if not region.empty():
            current = self.view.substr(region)
            title = current.split("=")[1].strip().replace('"', '')
            if " " not in title:
                title = " ".join(title.split('_'))
                title = title.capitalize()
                self.view.replace(edit, region, 'title = "' + title + '"')

    def run(self, edit):
        self.set_draft_status(edit, 'false')
        self.set_date(edit)
        self.fix_title(edit)


class HugoHelperInsertSummaryBreakCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        for region in self.view.sel():
            if region.empty():
                line = self.view.line(region)
                self.view.insert(edit, line.begin(), '<!--more-->\n')


class HugoHelperAddContentCommand(sublime_plugin.WindowCommand):

    def run(self, paths=[], name=""):
        import functools
        window = sublime.active_window()
        window.run_command('hide_panel')
        window.show_input_panel("post path:", name, functools.partial(self.on_done, paths), None, None)

    def on_done(self, paths, name):
        path = None
        cwd = None
        settings = sublime.load_settings('Hugo Helper.sublime-settings')
        hugoPath = settings.get('HugoPath', 'hugo')
        if name == "" or name is None:
            print ("You must supply a name")
            return
        if len(paths) > 0 and DEFAULT_CONTENTS_DIR in paths[0]:
            if not os.path.isdir(paths[0]):
                paths[0] = os.path.dirname(paths[0])
            splitted_paths = paths[0].split(os.path.sep)
            path = os.path.join("", *splitted_paths[splitted_paths.index(DEFAULT_CONTENTS_DIR) + 1:])
            cwd = os.path.join("/", *splitted_paths[:splitted_paths.index(DEFAULT_CONTENTS_DIR)])
        if not name.endswith(".md"):
            name += ".md"
        import subprocess
        index = 1
        import re
        while os.path.exists(os.path.join(paths[0], name)):
            exp = r'_\d*.md$'
            if index == 1:
                exp = r'.md$'
            name = re.sub(exp, '_' + str(index) + '.md', name)
            index += 1
        target = os.path.join(path, name)

        args = [hugoPath, "new", target]
        print (args, cwd)
        subprocess.Popen(args, cwd=cwd)
        return


class HugoHelperInsertCategory(sublime_plugin.TextCommand):
    def update_categories(self, edit, categories):
        region = self.view.find('categories\s=\s.*$', 0)
        if not region.empty():
            # self.view.run_command("insert", {"characters": str(categories)})
            self.view.replace(edit, region, 'categories = {}'.format(str(categories).replace("'", '"')))

    def run(self, edit, categories=None):
        if categories is None:
            return
        self.update_categories(edit, categories)
        return


class HugoHelperAddCategories(sublime_plugin.TextCommand):

    def get_categories(self, edit):
        region = self.view.find('categories\s=\s.*$', 0)
        if not region.empty():
            current = self.view.substr(region)
            categories = ast.literal_eval("".join(current.split("=")[1:]).lstrip().strip())
            return categories
        return []

    def on_done(self, edit, new_category):
        categories = self.get_categories(edit)
        print (new_category, categories)
        categories.append(new_category)
        categories = list(set(categories))  # remove duplicates
        # self.update_categories(edit,categories)
        self.view.run_command('hugo_helper_insert_category', {"categories": categories})
        return

    def run(self, edit):
        import functools
        new_category = ""
        window = sublime.active_window()
        window.run_command('hide_panel')
        window.show_input_panel("category name:", new_category, functools.partial(self.on_done, edit), None, None)
