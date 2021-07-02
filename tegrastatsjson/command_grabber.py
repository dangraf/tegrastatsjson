# AUTOGENERATED! DO NOT EDIT! File to edit: 00_command_grabber.ipynb (unless otherwise specified).

__all__ = ['CommandGrabber']

# Cell
import threading
import time
import os, sys, select, subprocess

# Cell
class CommandGrabber:
    def __init__(self, subprocess_cmd, line_callback=None):
        # subprocess_cmd: list of strings, the same as the subprosess command would take to execute it.
        # line_callback: function callback that takes the string as an input to handle it.
        super().__init__()
        self.subprocess_cmd = subprocess_cmd
        self.line_callback = line_callback
        self.running = False
        self.t = threading.Thread(target=self.run)
        self.t.start()

    def run(self):
        p1 = subprocess.Popen(self.subprocess_cmd, stdout=subprocess.PIPE)
        self.running=True
        while self.running:
            rlist, wlist, xlist = select.select([p1.stdout], [], [])
            time.sleep(0.1)
            for stdout in rlist:
                text = os.read(stdout.fileno(), 1024)
                if self.line_callback is not None:
                    text = text.decode("utf-8")
                    self.line_callback(text)
        try:
            p1.kill()
            print("Successfully stopped subprocess!")
        except subprocess.CalledProcessError:
            print(f"Unable to kill subprocess (pid={p1.pid}) successfully...")
            return False
        return True

    def stop(self):
        self.running= False

    def wait_until_finished(self):
        self.t.join()