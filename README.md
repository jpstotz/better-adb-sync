# Better ADB Sync

An [rsync](https://wiki.archlinux.org/title/rsync)-like program to sync files between a computer and an Android device

## Installation

Preparation: Make sure BetterADBSync version from PyPi.org is no longer installed:
```
$ pip uninstall BetterADBSync
```

Download and install BetterADBSync fork from GitHub 

```
$ git clone https://github.com/jpstotz/better-adb-sync.git
$ pip install better-adb-sync/
```

## How to use

To push from your computer to your phone use
```
$ adbsync push LOCAL ANDROID
```

To pull from your phone to your computer use
```
$ adbsync pull ANDROID LOCAL
```

Full help is available with `$ adbsync --help`:

```
adbsync --help
usage: adbsync [-h] [--version] [--no-color] [-v | -q] [-n] [-L] [--exclude EXCLUDE] [--exclude-from EXCLUDE_FROM] [--del] [--delete-excluded] [--force] [--show-progress]
               [--adb-encoding ADB_ENCODING] [--adb-bin ADB_BIN] [--adb-flag ADB_FLAG] [--adb-option OPTION VALUE]
               {push,pull} ...

Sync files between a computer and an Android device

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -n, --dry-run         Perform a dry run; do not actually copy and delete etc
  -L, --copy-links      Follow symlinks and copy their referent file / directory
  --exclude EXCLUDE     fnmatch pattern to ignore relative to source (reusable)
  --exclude-from EXCLUDE_FROM
                        Filename of file containing fnmatch patterns to ignore relative to source (reusable)
  --del                 Delete files at the destination that are not in the source
  --delete-excluded     Delete files at the destination that are excluded
  --force               Allows files to overwrite folders and folders to overwrite files. This is false by default to prevent large scale accidents
  --show-progress       Show progress from 'adb push' and 'adb pull' commands
  --adb-encoding ADB_ENCODING
                        Which encoding to use when talking to adb. Defaults to UTF-8. Relevant to GitHub issue #22

logging:
  --no-color            Disable colored logging (Linux only)
  -v, --verbose         Increase logging verbosity: -v for debug
  -q, --quiet           Decrease logging verbosity: -q for warning, -qq for error, -qqq for critical, -qqqq for no logging messages

ADB arguments:
  By default ADB works for me without touching any of these, but if you have any specific demands then go ahead. See 'adb --help' for a full list of adb flags and options

  --adb-bin ADB_BIN     Use the given adb binary. Defaults to 'adb' ie whatever is on path
  --adb-flag ADB_FLAG   Add a flag to call adb with, eg '--adb-flag d' for adb -d, that is return an error if more than one device is connected
  --adb-option OPTION VALUE
                        Add an option to call adb with, eg '--adb-option P 5037' for adb -P 5037, that is use port 5037 for the adb server

direction:
  {push,pull}
    push                Push from computer to phone
    pull                Pull from phone to computer
```

## Intro

This is a (pretty much from scratch) rewrite of Google's [adbsync](https://github.com/google/adb-sync) repo.

The reason for the rewrite is to

1. Update the repo to Python 3 codestyle (strings are by default UTF-8, no more `b""` and `u""`, classes don't need to inherit from object, 4 space indentation etc)
2. Add in support for `--exclude`, `--exclude-from`, `--del`, `--delete-excluded` like `rsync` has (this required a complete rewrite of the diffing algorithm)

## Additions

- `--del` will delete files and folders on the destination end that are not present on the source end. This does not include excluded files.
- `--delete-excluded` will delete excluded files and folders on the destination end.
- `--exclude` can be used many times. Each should be a `fnmatch` pattern relative to the source. These patterns will be ignored unless `--delete-excluded` is specified.
- `--exclude-from` can be used many times. Each should be a filename of a file containing `fnmatch` patterns relative to the source.

## Possible future TODOs

I am satisfied with my code so far, however a few things could be added if they are ever needed

- `--backup` and `--backup-dir-local` or `--backup-dir-android` to move outdated / to-delete files to another folder instead of deleting

---

## Related Projects

Before getting used to this, please review this list of projects that are
somehow related to adb-sync and may fulfill your needs better:

* [rsync](https://rsync.samba.org/) is a file synchronization tool for local
  (including FUSE) file systems or SSH connections. 
* [adbfs-rootless](https://github.com/spion/adbfs-rootless) is a fork of adbfs
  that requires no root on the device. Does not play very well with rsync.
* [go-mtpfs](https://github.com/hanwen/go-mtpfs) is a FUSE file system to
  connect to Android devices via MTP. Due to MTP's restrictions, only a certain
  set of file extensions is supported. To store unsupported files, just add
  .txt! Requires no USB debugging mode.

# Setup

## Android Side

First you need to enable USB debugging mode. This allows authorized computers
(on Android before 4.4.3 all computers) to perform possibly dangerous
operations on your device. If you do not accept this risk, do not proceed and
try using [go-mtpfs](https://github.com/hanwen/go-mtpfs) instead!

On your Android device:

* Go to the Settings app.
* If there is no "Developer Options" menu:
  * Select "About".
  * Tap "Build Number" seven times.
  * Go back.
* Go to "Developer Options".
* Enable "USB Debugging".

## PC Side

* Install the [Android SDK](https://developer.android.com/studio) which is included in Android Studio. Android SDK will
  be installed upon first start of Android Studio.    
  If you don't want to install a Android Studio you can try to download 
  [command-line-tools](https://developer.android.com/studio/index.html#command-line-tools-only).
  Some Linux distributions come with a package named like "android-tools-adb"
  that contains the required tool.
* Make sure `adb` is in your PATH. If you use a package from your Linux
  distribution, this should already be the case; if you used the SDK, you
  probably will have to add an entry to PATH in your ~/.profile file, log out
  and log back in.
* `git clone https://github.com/jpstotz/better-adb-sync.git
* `pip install better-adb-sync/`

On modern Android device the device need to be unlocked (display on and lock screen is 
not active) when connecting with an USB cable to the PC.   

## Usage

To get a full help, type:

```
adbsync --help
```

### Usage examples

To synchronize your music files from ~/Music to your device, type one of:

```
adbsync push ~/Music /sdcard
adbsync push ~/Music/ /sdcard/Music
```

---
To synchronize your music files from ~/Music to your device, deleting files you
removed from your PC, type one of:

```
adbsync push --del ~/Music /sdcard
adbsync push --del ~/Music/ /sdcard/Music
```

---
To copy all downloads from your device to your PC, type:

```
adbsync pull /sdcard/Download/ ~/Downloads
```

---
Backup all data from external storage to your PC:
```
adbsync pull -L --show-progress pull /sdcard/ ./BackupAndroid
```
* `-L` is required to follow the symlink `/sdcard` 
* `--show-progress` is optional but recommended as depending on the data on the phone the operation can take quite a while