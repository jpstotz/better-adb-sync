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

## QRD

To push from your computer to your phone use
```
$ adbsync push LOCAL ANDROID
```

To pull from your phone to your computer use
```
$ adbsync pull ANDROID LOCAL
```

Full help is available with `$ adbsync --help`

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

Related Projects
================

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

Setup
=====

Android Side
------------

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

PC Side
-------

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

Usage
=====

To get a full help, type:

```
adbsync --help
```

To synchronize your music files from ~/Music to your device, type one of:

```
adbsync push ~/Music /sdcard
adbsync push ~/Music/ /sdcard/Music
```

To synchronize your music files from ~/Music to your device, deleting files you
removed from your PC, type one of:

```
adbsync push --del ~/Music /sdcard
adbsync push --del ~/Music/ /sdcard/Music
```

To copy all downloads from your device to your PC, type:

```
adbsync pull /sdcard/Download/ ~/Downloads
```