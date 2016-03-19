For Japanese version see README.jp.txt

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

Plugin has 3 "navigators" e.g. methods used to detect definitions and references

1. gtags - this is the recomended way - it requires creations of GTAGS file in the directory in which file resides or in one of the parents:
```
gtags -v
```

2. etags - this is when gtags can not be used (often in custom case like XML/XSD navigation) - it requires TAGS file in the directory of the file or one of its parents
create with either
```
etags -R
```
or
```
ctags -e -R
```

3. Python navigator - more info needed

## Usage

Position the cursor on the name and use the keys defined in settings.py to:

* jump to definition

* jump to the reference

* go back in jump history

* go forward in jump history


## Credits

Author: Masatoshi Tsushima, Twitter: @utisam

Porting to GNOME 3: Jacek Pliszka


