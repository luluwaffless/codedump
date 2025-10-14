from winmsgbox import MessageBox, Buttons, Icon, DefaultButton, Modal, Flags, Response
from os.path import expanduser, basename, splitext, join, exists
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from os import makedirs
from shutil import move
from time import sleep
def isTemp(filepath):
    temp_exts = ('.crdownload', '.part', '.tmp', '.download')
    temp_names = ('Unconfirmed ',)
    filename = basename(filepath)
    return filepath.endswith(temp_exts) or filename.startswith(temp_names)
destination = expanduser("~\\Desktop\\Files\\files\\")
class organizer(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and not isTemp(event.src_path):
            filename = basename(event.src_path)
            name, ext = splitext(filename)
            folder_name = ext.lower() if ext else "no_extension"
            target_directory = join(destination, folder_name)
            response = MessageBox(title="Download Organizer", text=f"File \"{filename}\" has been downloaded. Send it to {target_directory}?", buttons=Buttons.YesNo, icon=Icon.Question, defaultButton=DefaultButton.First, modal=Modal.SystemModal, flags=Flags.SetForeground | Flags.TopMost)
            if response == Response.Yes:
                if not exists(target_directory):
                    makedirs(target_directory)
                destination_path = join(target_directory, filename)
                if exists(destination_path):
                    counter = 1
                    while True:
                        new_filename = f"{name} ({counter}){ext}"
                        destination_path = join(target_directory, new_filename)
                        if not exists(destination_path):
                            break
                        counter += 1
                    filename = new_filename
                move(event.src_path, destination_path)
                MessageBox(title="Download Organizer", text=f"File \"{filename}\" moved to {target_directory}.", buttons=Buttons.Ok, icon=Icon.Information, defaultButton=DefaultButton.First, modal=Modal.SystemModal, flags=Flags.SetForeground | Flags.TopMost)
            else:
                return
observer = Observer()
observer.schedule(organizer(), expanduser("~\\Downloads"), recursive=False)
observer.start()
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()