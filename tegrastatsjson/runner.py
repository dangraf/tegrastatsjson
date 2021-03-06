# AUTOGENERATED! DO NOT EDIT! File to edit: 02_runner.ipynb (unless otherwise specified).

__all__ = ['tegrastats_callback', 'tegrastatsjson']

# Cell
import fire
from pathlib import Path
from datetime import datetime
from pathlib import Path
from functools import partial
from fastcore.script import *
from .command_grabber import *
from .parser import *
from nbdev.imports import *
from nbdev.export import *

# Cell
def tegrastats_callback(tegra_line, filename='/var/output/tegra.json'):
    timestamp = str(datetime.now())
    d = ParseTegrastats.parse_line(tegra_line)
    d['timestamp'] = timestamp
    filename = filename
    with open(filename, 'a') as f:
        json.dump(d, f)
        f.write('\n')

# Cell
@call_parse
def tegrastatsjson(log_file:Param("path to filename to log to", str)=None,
                   interval:Param("in ms", int)=1000,
                   add_date_to_logfile:Param('adds timestamp to filename help distinguish between different runs',bool)=True):
    p = Path(log_file)
    if add_date_to_logfile:
        fname = p.stem+ datetime.now().strftime("-%Y-%m-%d %H:%M:%S") + p.suffix
        p = p.parent / fname

    tegrastats_c = partial(tegrastats_callback, filename=str(p))
    args = ['sh', '-c', f"tegrastats --interval {interval}"]

    task = CommandGrabber(args, tegrastats_c)
    task.wait_until_finished()
    return
