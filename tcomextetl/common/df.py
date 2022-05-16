from datetime import datetime
from pathlib import Path

CSV_SEP = ','


def df_last_file(files):
    dates = []
    for f in files:
        fname = Path(f).stem
        _dt = fname.split('_')[3]
        dt = datetime.strptime(_dt, '%Y-%m-%d')
        dates.append((dt, f))

    dates.sort(key=lambda x: x[1])

    return dates[-1][1]