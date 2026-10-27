import datetime
import gzip
import pathlib
import shutil


def rotate(path, max_size_mb=10, keep=5):
    p = pathlib.Path(path)
    if not p.exists():
        return
    if p.stat().st_size < max_size_mb * 1024 * 1024:
        return
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    rotated = p.with_suffix('.' + stamp + p.suffix)
    shutil.move(str(p), str(rotated))
    with open(rotated, 'rb') as fin, gzip.open(str(rotated) + '.gz', 'wb') as fout:
        shutil.copyfileobj(fin, fout)
    rotated.unlink()
    old = sorted(pathlib.Path(path).parent.glob('*' + p.suffix + '.*'), reverse=True)[keep:]
    for f in old:
        f.unlink()
