from core import MainApplication
import os
import signal

def system_kill_interrupt_handler(self, signal, frame):
    raise SystemExit('Catch ternimate signal')

signal.signal(signal.SIGTERM, system_kill_interrupt_handler)

def write_pid():
    pid = str(os.getpid())
    with open("deamon.pid", "w") as f:
        f.write(pid)

if __name__=='__main__':
    write_pid()

    app = MainApplication()
    app.test_tempo()

