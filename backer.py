import sublime, sublime_plugin
import os, stat
import shutil

class BackupFileCommand(sublime_plugin.TextCommand):
    def run(self, view):
        thisFile = self.view.file_name()

        # Get backup file extension from User Settings
        # Default to '.bak' if not specified
        backup_file_extension = self.view.settings().get('backer_file_extension', '.bak')

        try:
            backup_file_name = ''.join([thisFile, backup_file_extension])
            shutil.copy2(thisFile, backup_file_name)
            print 'Created backup file as {0}'.format(backup_file_name)
        except IOError as e:
            print 'Failed to make backup copy of file with error: ', e

        try:
            os.chmod(thisFile, stat.S_IWRITE)
            print 'Set {0} to writable'.format(thisFile)
        except OSError as e:
            print 'Failed to set current file to writable with error: ', e

class BackupFileEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        thisFile = view.file_name()

        if os.access(thisFile, os.W_OK):
            return

        view.run_command('backup_file')
