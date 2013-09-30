#aponxi
import sys
import os
from os import path
from subprocess import Popen, PIPE
from sublime_plugin import TextCommand
from sublime_plugin import WindowCommand
import sublime_plugin
import sublime
import functools
import locale
import threading
import tempfile
from .sourcemap import load


def settings_get(name, default=None):
    # load up the plugin settings
    plugin_settings = sublime.load_settings('TypeScript.sublime-settings')
    # project plugin settings? sweet! no project plugin settings? ok, well promote plugin_settings up then
    if sublime.active_window() and sublime.active_window().active_view():
        project_settings = sublime.active_window().active_view().settings().get("TypeScript")
    else:
        project_settings = {}

    # what if this isn't a project?
    # the project_settings would return None (?)
    if project_settings is None:
        project_settings = {}

    setting = project_settings.get(name, plugin_settings.get(name, default))
    return setting


def run(cmd, args=[], source="", cwd=None, env=None, callback=None):
    """
    Run command. "tsc", "cake", etc.
    Will run on thread if callback function is passed.
    """
    if callback:
        threading.Thread(target=lambda cb: cb(_run(cmd, args=args, source=source, cwd=cwd, env=env)), args=(callback,)).start()
    else:
        res = _run(cmd, args=args, source=source, cwd=cwd, env=env)
        return res


def _run(cmd, args=[], source="", cwd=None, env=None):
    if not type(args) is list:
        args = [args]
    if sys.platform == "win32":
        args = [cmd] + args
        if sys.version_info[0] == 2:
            for i in range(len(args)):
                args[i] = args[i].encode(locale.getdefaultlocale()[1])
        proc = Popen(args, env=env, cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
        try:
            stat = proc.communicate(input=source)
        except:
            stat = proc.communicate(input=source.encode("utf8"))
        okay = proc.returncode == 0
        return {"okay": okay, "out": stat[0].decode(locale.getdefaultlocale()[1]), "err": stat[1].decode(locale.getdefaultlocale()[1])}
    else:
        if env is None:
            env = {"PATH": settings_get('binDir', '/usr/local/bin')}

        # adding custom PATHs from settings
        customEnv = settings_get('envPATH', "")
        if customEnv:
            env["PATH"] = env["PATH"]+":"+customEnv
        args += ["--module", settings_get("module")]
        if source == "":
            command = [cmd] + args
        else:
            command = [cmd] + args + [source]
        proc = Popen(command, env=env, cwd=cwd, stdout=PIPE, stderr=PIPE)
        stat = proc.communicate()
        okay = proc.returncode == 0
        return {"okay": okay, "out": stat[0].decode('utf-8'), "err": stat[1].decode('utf-8')}


def brew(args, source, cwd=None, callback=None):
    """
    Compile command
    """
    # if sys.platform == "win32":
    #     args.append("-s")
    # else:
    #     args.append("-e")
    tempTSFile = path.join(tempfile.gettempdir(), "temp.ts")
    with open(tempTSFile, 'w') as f:
        f.write(source)
    res = run("tsc", [tempTSFile])
    res["out"] = open(path.join(tempfile.gettempdir(), 'temp.js')).read()
    return res


def isTypescript(view=None):
    if view is None:
        view = sublime.active_window().active_view()
    return 'source.ts' in view.scope_name(0)

class Text():
    @staticmethod
    def all(view):
        return view.substr(sublime.Region(0, view.size()))

    @staticmethod
    def sel(view):
        text = []
        for region in view.sel():
            if region.empty():
                continue
            text.append(view.substr(region))
        return "".join(text)

    @staticmethod
    def get(view):
        text = Text.sel(view)
        if len(text) > 0:
            return text
        return Text.all(view)


class CompileCodeCommand(TextCommand):
    def is_enabled(self):
        return isTypescript(self.view)

    def on_done(self, result):
        if result['okay'] is True:
            status = 'Compilation Succeeded'
        else:
            errorFirstLine = result['err'].splitlines()[0]
            status = 'Compilation FAILED ' + errorFirstLine
            sublime.error_message(errorFirstLine)

        later = lambda: sublime.status_message(status)
        sublime.set_timeout(later, 300)

    def run(self, *args, **kwargs):
        # no_wrapper = settings_get('noWrapper', True)
        compile_dir = settings_get('compileDir')
        source_file = self.view.file_name()
        source_dir = os.path.normcase(os.path.dirname(source_file))
        compile_paths = settings_get('compilePaths')
        sourcemaps = settings_get('sourceMaps', True)

        args = ['-c', source_file]
        if sourcemaps:
            args = ['--sourcemap'] + args

        # check instance of compile_paths
        if isinstance(compile_paths, dict):
            appendix_len = None
            for key_path in compile_paths:
                norm_path = os.path.normcase(key_path)
                appendix = os.path.relpath(source_dir, norm_path)
                if not appendix.startswith('..') and (appendix_len is None or len(appendix) < appendix_len):
                    appendix_len = len(appendix)
                    compile_dir = compile_paths[key_path]
                    if not os.path.isabs(compile_dir):
                        compile_dir = os.path.join(norm_path, compile_dir)
                    compile_dir = os.path.join(compile_dir, appendix)

        if compile_dir and (isinstance(compile_dir, str)):
            # Check for absolute path or relative path for compile_dir
            if not os.path.isabs(compile_dir):
                compile_dir = os.path.join(source_dir, compile_dir)
            print("Compile to:" + compile_dir)
            # create folder if not exist
            if not os.path.exists(compile_dir):
                os.makedirs(compile_dir)
                print("Compile dir did not exist, created folder: " + compile_dir)
            folder, file_nm = os.path.split(source_file)
            args = ['--outDir', compile_dir] + args
        else:
            compile_dir = source_dir
            print("Compile to same directory")

        if sourcemaps:
            cwd = source_dir
        else:
            cwd = None
        run("tsc", args, cwd=cwd, callback=lambda res: self.on_done(res))
        # resulrun("tsc", args=args, cwd=cwd)

        # if result['okay'] is True:
        #     status = 'Compilation Succeeded'
        # else:
        #     errorFirstLine = result['err'].splitlines()[0]
        #     status = 'Compilation FAILED ' + errorFirstLine
        #     sublime.error_message(errorFirstLine)

        # later = lambda: sublime.status_message(status)
        # sublime.set_timeout(later, 300)


class CompileAndDisplayCodeCommand(TextCommand):
    def is_enabled(self):
        return isTypescript(self.view)

    def on_done(self, res, output):
        if res["okay"] is True:
            self.view.window().open_file(self.view.file_name().split(".")[0]+'.js')
        else:
            output = self.view.window().new_file()
            output.set_scratch(True)
            output.set_syntax_file('Packages/JavaScript/JavaScript.tmLanguage')
            output.run_command('update_watch', {'pos': 0, 'text': res["out"] or res["err"]})
            sublime.status_message("Compiling done.")

    def run(self, edit, **kwargs):
        sublime.status_message("Compiling typescript...")
        args = [self.view.file_name()]
        run("tsc", args, callback=lambda res: self.on_done(res, edit))


class CheckCodeSyntaxCommand(TextCommand):
    def is_enabled(self):
        return isTypescript(self.view)

    def on_done(self, res):
        if res["okay"] is True:
            status = 'Valid'
        else:
            status = res["err"].split("\n")[0]
        sublime.message_dialog('Syntax %s' % status)
        # sublime.status_message()

    def run(self, edit):
        sublime.status_message("Checking syntax...")
        args = [self.view.file_name(), "--outDir", tempfile.gettempdir()]
        run("tsc", args, callback=lambda res: self.on_done(res))


class UpdateWatchCommand(sublime_plugin.TextCommand):
    def run(self, edit, pos, text):
        region = sublime.Region(0, self.view.size())
        self.view.erase(edit, region)
        self.view.insert(edit, pos, text)


class LintCodeCommand(TextCommand):

    def is_enabled(self):
        return isTypescript(self.view)

    def run(self, edit):
        filepath = self.view.file_name()
        res = run("tslint", args=["-f", filepath, "-c", settings_get("lintConfPath") or path.dirname(self.view.file_name())])
        error_list = []
        for line in res["out"].split('\n'):
            if not len(line.split(":"))-1:
                continue
            # lineNum = line.split(",")[1]
            # message = line.split(",")[-1]
            message = line.split(":")[1][1:]
            lineNum = line.split("[")[1].split(",")[0]
            try:
                error_list.append({"message": message, "line": int(lineNum)-1})
            except:
                continue
        if len(error_list):
            self.popup_error_list(error_list)
        else:
            sublime.message_dialog("No lint errors.")

    def popup_error_list(self, error_list):

        panel_items = []

        for error in error_list:
            line_text = self.view.substr(self.view.full_line(self.view.text_point(error['line'], 0)))
            item = [error['message'], '{0}: {1}'.format(error['line'] + 1, line_text.strip())]
            panel_items.append(item)

        def on_done(selected_item):
            if selected_item == -1:
                return

            selected = self.view.sel()
            selected.clear()

            error = error_list[selected_item]
            region_begin = self.view.text_point(error['line'], 0)

            selected.add(sublime.Region(region_begin, region_begin))
            # We have to force a move to update the cursor position
            self.view.run_command('move', {'by': 'characters', 'forward': True})
            self.view.run_command('move', {'by': 'characters', 'forward': False})
            self.view.show_at_center(region_begin)

        self.view.window().show_quick_panel(panel_items, on_done)

watchers = {}


def watched_filename(view):
    if view.file_name() is not None:
        filename = view.file_name().split('/')[-1]
    else:
        filename = "Unsaved File"
    return filename


class Tool():
    @staticmethod
    def get_file_name(file_path):
        if file_path:
            filename = os.path.split(file_path)[-1]
        else:
            filename = "Unsaved File"
        return filename

    @staticmethod
    def get_js_file_name(tsc_file_name):
        fileName, fileExtension = os.path.splitext(tsc_file_name)
        output_filename = fileName + '.js'
        return output_filename


class Watcher():
    def __init__(self, inputView):
        self.inputView = inputView
        print("Now watching " + watched_filename(inputView))
        if self.inputView.window().num_groups() == 1:
            # create new column
            self.inputView.window().run_command('set_layout', {
                "cols": [0.0, 0.5, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1], [1, 0, 2, 1]]
            })
        self.create_output()

    def on_done(self, res):
        if not res["okay"]:
            sublime.message_dialog("Error. See console.")
            print(res["err"])
            return
        # create new tab
        self.outputView = self.inputView.window().open_file(self.outputFilePath)
        # move it to second column
        self.outputView.window().focus_group(1)
        self.outputView.window().set_view_index(self.outputView, self.outputView.window().active_group(), 0)
        # self.outputView.window().focus_group(0)
        self.inputView.window().focus_view(self.inputView)
        mapFile = path.join(self.outputTempDir, self.outputFileName.split(".")[0]+'.js.map')
        (inputRow, inputCol) = self.inputView.rowcol(self.inputView.sel()[0].begin())
        index = load(open(mapFile)).getpos(line=inputRow, column=inputCol)
        if not index:
            return
        (row, col) = index
        row = int(row)

        def goto():
            selected = self.outputView.sel()
            selected.clear()
            region_begin = self.outputView.text_point(row, 0)
            selected.add(sublime.Region(region_begin, region_begin))
            self.outputView.run_command('move', {'by': 'characters', 'forward': True})
            self.outputView.run_command('move', {'by': 'characters', 'forward': False})
            self.outputView.show_at_center(region_begin)
        sublime.set_timeout(goto, 10)

    def create_output(self):
        self.sourceFilePath = self.inputView.file_name()
        self.outputFileName = Tool.get_js_file_name(Tool.get_file_name(self.sourceFilePath))
        self.outputTempDir = tempfile.gettempdir()
        self.outputFilePath = path.join(self.outputTempDir, self.outputFileName)
        args = ["--sourcemap", "--outDir", self.outputTempDir, self.sourceFilePath]
        run("tsc", args, callback=lambda res: self.on_done(res))

    def refresh(self):
        args = ["--sourcemap", "--outDir", self.outputTempDir, self.sourceFilePath]
        run("tsc", args, callback=lambda res: self.on_done(res))

    def stop(self):
        if not self.inputView.id() in watchers:
            return
        print("Stop watching: " + self.inputView.file_name())
        del watchers[self.inputView.id()]
        window = self.outputView.window() or self.inputView.window()
        if self.outputView.window():
            window.focus_view(self.outputView)
            window.run_command("close")

        if len(watchers) == 0 and len(window.views_in_group(1)) == 0:
            window.run_command('set_layout', {
                "cols": [0.0, 1.0],
                "rows": [0.0, 1.0],
                "cells": [[0, 0, 1, 1]]
            })


class ToggleWatchMode(TextCommand):
    views = {}
    outputs = {}

    def is_enabled(self):
        return isTypescript(self.view)

    def run(self, edit):
        viewID = self.view.id()
        if not viewID in watchers:
            watchers[viewID] = Watcher(self.view)
        else:
            watchers[viewID].stop()


class CaptureEditing(sublime_plugin.EventListener):

    def is_enabled(self, view):
        return isTypescript(view)

    def handleTimeout(self, watcher):
        if self._new_modify and not self._refreshed:
            sublime.set_timeout(functools.partial(self.handleTimeout, watcher), 1000)
            self._new_modify = False
        else:
            if self._refreshed:
                return
            self._refreshed = True
            watcher.refresh()

    def on_modified(self, view):
        if not self.is_enabled(view):
            return
        viewID = view.id()
        watch_modified = settings_get('watchOnModified')
        self._new_modify = True
        if watch_modified is not False and viewID in watchers:
            self._refreshed = False
            self.handleTimeout(watchers[viewID])

    def on_post_save(self, view):
        if not self.is_enabled(view):
            return
        compile_on_save = settings_get('compileOnSave', True)
        if compile_on_save is True:
            print("Compiling on save...")
            view.run_command("compile_code")

        watch_save = settings_get('watchOnSave', True)
        if watch_save:
            viewID = view.id()
            if viewID in watchers:
                watchers[viewID].refresh()

    def on_close(self, view):
        viewID = view.id()
        for k, watcher in watchers.items():
            if watcher.outputView.id() == viewID:
                watcher.stop()
                break

        if not self.is_enabled(view):
            return

        if viewID in watchers:
            watchers[viewID].stop()
