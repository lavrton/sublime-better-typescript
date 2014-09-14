Better Typescript
================================

# Overview

**This package is for Sublime Text 3**.

## Description

This is fork of [Better CoffeeScript](https://github.com/aponxi/sublime-better-coffeescript) but adopted for work with Typescript.
Also look at this TypeScript plugin for Sublime Text https://github.com/Railk/T3S. It is really awesome.

# Installation

If you have Sublime Package Control, you know what to do. If not, well: it's a package manager for Sublime Text 3; it's awesome and you can [read about it here](https://sublime.wbond.net/). Installation guide can be [found here](https://sublime.wbond.net/installation).

* Open the Command Pallete (`ctrl+shift+P` or `cmd+shift+P`).
* Type "Install Package" and hit return.
* Type "Better TypeScript" and hit return.

# Build File Example

Current package don't have sublime build file. You can create it by yourself and save it (`Preferences - Browse Packages... - User folder`) as `Typescript.sublime-build`. Then use `Cmd + B` to build your file.

```
{
    "cmd": ["tsc", "-d", "-m", "amd", "--sourcemap", "$file"],
    "file_regex": "(.*\\.ts?)\\s\\(([0-9]+)\\,([0-9]+)\\)\\:\\s(...*?)$",
    "selector": "source.ts",
    "osx": {
       "path": "/usr/local/bin:/opt/local/bin"
    },
    "windows": {
        "cmd": ["tsc.cmd", "-d", "-m", "amd", "--sourcemap", "$file"]
    }
}
```

# Commands/Shortcuts

You can access the commands either using the command palette (`ctrl+shift+P` or `cmd+shift+P`) or via shortcuts.

	alt+shift+s - Run a syntax check
	alt+shift+c - Compile a file
	alt+shift+d - Display compiled JavaScript
	alt+shift+w - Toggle watch mode


Context menu has `Compile Output` that compiles the current TypeScript and outputs the javascript code that is run, in a panel.

**Note:** Some of the commands use the Status Bar for output, so you'll probably want to enable it (`View » Show Status Bar`).


# Snippets

- Use `TAB` to run a snippet after typing the trigger.
- Use `TAB` and `shift+TAB` to cycle forward/backward through fields.
- Use `ESC` to exit snippet mode.

Thanks @MattSeen to provide Snippets (https://github.com/MattSeen/Sublime-TypeScript-Snippets)

# Settings

Go to `Preferences > Package Settings > Better TypeScript > Settings - User` to change settings.

See `Preferences > Package Settings > Better TypeScript > Settings - Default` to see all available settings.


# FAQ

Most of the linux terminal commands written here can be run via [cygwin](http://cygwin.com/install.html) - aka Linux Terminal in Windows.

- Most of the problems are related to configurations. Remember to configure `binDir` after you install!


- Do I have `tsc` installed?

Try finding tsc in your global npm list with `npm ls -g | grep tsc` which will output something like:

```bash
npm ls -g | grep tsc
```


- Where can I find out the path to tsc binary?

In Linux `which` command will tell you where a command originates from. In terminal type:

```bash
which tsc
# /usr/bin/tsc
```

This path will go into the `binDir` setting.
