# Jump to Section

* [Latest Change Log](#latest-changelog)
* [FAQ](#faq)
* [Installation](#installation)
* [Updating](#updating)
* [Commands/Shortcuts](#commandsshortcuts)
* [Snippets](#snippets)
* [Settings](#settings)

# Overview

**This package is for Sublime Text 3**.

## Description

This is fork of [Better CoffeeScript](https://github.com/aponxi/sublime-better-coffeescript) but adopted for work with Typescript.

# Installation

## via Package Control

> This is the recommended installation method.

If you have Sublime Package Control, you know what to do. If not, well: it's a package manager for Sublime Text 3; it's awesome and you can [read about it here](https://sublime.wbond.net/). Installation guide can be [found here](https://sublime.wbond.net/installation).

The simplest method of installation is through the Sublime Text console. The console is accessed via the ctrl+` shortcut or the View > Show Console menu. Once open, paste the appropriate Python code for your version of Sublime Text into the console.

SUBLIME TEXT 3

```
import urllib.request,os; pf = 'Package Control.sublime-package'; ipp = sublime.installed_packages_path(); urllib.request.install_opener( urllib.request.build_opener( urllib.request.ProxyHandler()) ); open(os.path.join(ipp, pf), 'wb').write(urllib.request.urlopen( 'http://sublime.wbond.net/' + pf.replace(' ','%20')).read())
```

This code creates the Installed Packages folder for you (if necessary), and then downloads the Package Control.sublime-package into it.

After installing the package manager:

* Open the Command Pallete (`ctrl+shift+P` or `cmd+shift+P`).
* Type "Install Package" and hit return.
* Type "Better TypeScript" and hit return.

## via Source Control

> If you plan to contribute, then you should install via this method. Otherwise it is recommended that you install the package via Package Control, see above.

Sublime stores packages in the following locations:

	Nix: ~/.config/sublime-text-3/packages
	Mac: ~/Library/Application\ Support/Sublime\ Text\ 3/Packages
	Win: %APPDATA%\Sublime Text 3\Packages

### As a repository within the packages directory

Open a Terminal/Console and run the following commands, replacing `PACKAGE_PATH` with the path corresponding to your OS above.

	cd PACKAGE_PATH
	git clone https://github.com/lavrton/sublime-better-typescript.git "Better TypeScript"


#### A note on Package Control

When Package Control tries to update your packages, if you have a repository in your packages directory then it will try to pull down and merge any changes. If you don't want this to happen and would rather handle everything yourself, then you can add the following to your settings (Preferences » Package Settings » Package Control » Settings - User):

	"auto_upgrade_ignore": ["Better TypeScript"]

# Updating

If you are using Package Control, updating will be automatic and you don't have to worry about it.

If using Source Control:

	cd "PACKAGE_PATH/Better TypeScript"
	git fetch origin
	git merge origin/master

# Commands/Shortcuts

You can access the commands either using the command palette (`ctrl+shift+P` or `cmd+shift+P`) or via shortcuts.

	alt+shift+s - Run a syntax check
	alt+shift+c - Compile a file
	alt+shift+d - Display compiled JavaScript
	alt+shift+w - Toggle watch mode
	alt+shift+p - Toggle output panel


Context menu has `Compile Output` that compiles the current TypeScript and outputs the javascript code that is run, in a panel.

**Note:** Some of the commands use the Status Bar for output, so you'll probably want to enable it (View » Show Status Bar).



# Snippets

- Use `TAB` to run a snippet after typing the trigger.
- Use `TAB` and `shift+TAB` to cycle forward/backward through fields.
- Use `ESC` to exit snippet mode.

### Snippet Triggers

Not snippets for now. Wait in new version.

# Settings

Go to `Preferences > Package Settings > Better TypeScript > Settings - User` to change settings.

```Javascript
{
	/*
		The directories you would like to include in $PATH environment variable.
		Use this if your node installation is at a separate location and getting errors such as `cannot find node executable`

		example:
		"envPATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

	*/
	"envPATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
	/*
		The directory containing your typescript binary. Usually
		/usr/local/bin.
	*/
	"binDir": "/usr/local/bin"
	/*
		Enable or disable refresh the compiled Output on Save.
		Only available for watch mode.
	*/
,	"watchOnSave": true
	/*
		Enable refreshing compiled JS when CoffeeScript is modified.

		Put false to disable
		Put a number of seconds to delay the refresh
	*/
,	"watchOnModified": 0.5
	/*
		Enable Compiling on save. It will compile into the same folder.
	*/
,	"compileOnSave": true
	/*
		## Enable outputting the results of the compiled typescript in a panel
	*/
,	"showOutputOnSave": false
	/*
		## Enable compiling to a specific directory.
		#### Description

		if it is a string like 'some/directory' then `-o some/directory` will be added to `typescript` compiler.
		if it is false or not string then it will compile your `script.ts` to the directory it is in.

		#### Example:
		Directory is relative to the file you are editing if specified such as
			compileDir": "out"
		Directory is absolute if specified such as
			compileDir": "/home/logan/Desktop/out"

	*/
,	"compileDir": false
	/*
		## Enable compiling to a specific relative directories.

		#### Example:
		Set absolute path for compile dir:
			"compileDir": "/home/user/projects/js"
		And specified folders
			"relativeDir": "/home/user/projects/ts"
			"compilePaths":
			{
				"/home/user/projects/ts": "/home/user/projects/first/js",
				"/home/user/projects/second/ts": "../js",
			}

		So
			"/home/user/projects/ts/app.ts" will compile to "/home/user/projects/first/js/app.js"
			"/home/user/projects/ts/models/prod.ts" will compile to "/home/user/projects/first/js/models/prod.js"
			"/home/user/projects/ts/second/ts/app2.ts" will compile to "/home/user/projects/second/js/app2.js"
			"/home/user/projects/main.ts" will compile to "/home/user/projects/js/main.js"

	*/
,	"compilePaths": false



}


```

## Project settings

Go to `Project > Edit Project` to change project settings.

```Javascript
{
	"folders":
	[
		...
	],
	"settings":
	{
		"TypeScript":
		{
			"compileOnSave": true,
			"compileDir": "out"
		}
	}
}



```

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
