For Japanese version see README.jp.txt

Plugin is more general than gtags - it also can use etags, python-jedi and python-symtable

## --- Fly with the gtags "tagJump" ---

## Installation

```
cd ~/.local/share/gedit/plugins/
git clone https://github.com/utisam/gtagJump.git
```

Then start gedit and click "Preferences"->"Plugins" and check "gtagJump"

The plugin should be ticked then (not red). If it is red - check gedit version (current master branch requires 3.14+) and also run gedit from command line to see errors in the console.

## Configuration

Configuration is done in gtagJump/settings.py file

Plugin has 4 "navigators" e.g. methods used to detect definitions and references

1. python jedi only for python files

2. gtags - this is the recomended way - it requires creations of GTAGS file in the directory in which file resides or in one of the parents:
```
gtags -v
```

3. etags - this is when gtags can not be used (often in custom case like XML/XSD navigation) - it requires TAGS file in the directory of the file or one of its parents
create with either
```
etags -R
```
or
```
ctags -e -R
```

4. Python navigator based on symtable more info needed

## Usage

Position the cursor on the name and use the keys defined in settings.py to:

* jump to definition

* jump to the reference

* go back in jump history

* go forward in jump history


## Credits

Author: Masatoshi Tsushima, Twitter: @utisam

Porting to GNOME 3: Jacek Pliszka


