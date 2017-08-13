#!/usr/bin/env python


import fire
import pync
from AppKit import (NSApp, NSApplication, NSObject, NSWorkspace,
                    NSWorkspaceDidWakeNotification)
from PyObjCTools import AppHelper


class App(NSObject):

    def __init__(self, *a, **kw):
        self.reminder = kw.pop('reminder', None)
        App.__init__(self, *a, **kw)

    def quit_(self, notification):
        NSApp().terminate_(self)

    def close_(self, notification):
        NSApp().terminate_(self)

    def applicationDidFinishLaunching_(self, notification):
        workspace = NSWorkspace.sharedWorkspace()
        notificationCenter = workspace.notificationCenter()
        notificationCenter.addObserver_selector_name_object_(
            self,
            self.receiveWakeNotification_,
            NSWorkspaceDidWakeNotification,
            None
        )

    def show_reminder(self):
        pync.Notifier.notify(self.reminder, title='Afk', sender='com.apple.reminders')

    def receiveWakeNotification_(self, notification):
        self.show_reminder()
        NSApp().terminate_(self)


def run(reminder, *reminders):
    reminders = [reminder] + list(reminders)
    sharedapp = NSApplication.sharedApplication()
    app = App.alloc().init()
    app.reminder = " ".join(reminders)
    sharedapp.setDelegate_(app)
    app.applicationDidFinishLaunching_(None)
    print("Reminder saved")
    print("Waiting ...")
    try:
        AppHelper.runConsoleEventLoop(installInterrupt=True)
    except KeyboardInterrupt:
        print('Interrupt, pending reminders:')
        app.show_reminder()


def main():
    return fire.Fire(run)


if __name__ == "__main__":
    main()
