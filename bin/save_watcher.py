#!/usr/bin/env python

import sys
from pathlib import Path

sys.path.insert(0, Path(__file__).resolve().parents[1].joinpath('lib').as_posix())
import _venv  # This will activate the venv, if it exists and is not already active

import logging
from hashlib import sha256

from watchdog.observers import Observer

from nier.cli import ArgParser, get_path
from nier.utils import unique_path

log = logging.getLogger(__name__)


def parser():
    parser = ArgParser(description='Nier Replicant ver.1.22474487139... Save File Watcher')
    parser.add_argument('--path', '-p', help='Save file path to watch')
    parser.add_argument('--backups', '-b', metavar='PATH', help='Path to the directory in which backups should be saved (default: same dir as save files)')
    parser.add_argument('--verbose', '-v', action='count', default=0, help='Increase logging verbosity')
    return parser


def main():
    args = parser().parse_args()
    log_fmt = '%(asctime)s %(levelname)s %(name)s %(lineno)d %(message)s' if args.verbose else '%(asctime)s %(message)s'
    logging.basicConfig(level=(12 - args.verbose) if args.verbose else 20, format=log_fmt)
    logging.addLevelName(11, 'VERBOSE')

    path = get_path(args.path)
    backup_dir = Path(args.backups) if args.backups else path.parent
    if backup_dir.exists() and not backup_dir.is_dir():
        raise ValueError(f'Invalid backup_dir={backup_dir.as_posix()} - it is not a directory')
    elif not backup_dir.exists():
        log.debug(f'Creating backup_dir={backup_dir.as_posix()}')
        backup_dir.mkdir(parents=True)

    FSEventHandler(path, backup_dir).run()


class FSEventHandler:
    def __init__(self, path: Path, backup_dir: Path):
        self.path = path
        self.backup_dir = backup_dir
        self.observer = Observer()
        self.observer.schedule(self, path.parent.as_posix())
        self.last_hash = None

    def run(self):
        log.info(f'Watching {self.path.as_posix()} with observer={self.observer}')
        self.observer.start()
        try:
            while True:
                self.observer.join(0.5)
        except KeyboardInterrupt:
            self.observer.stop()
            self.observer.join()

    def dispatch(self, event):
        what = 'directory' if event.is_directory else 'file'
        path = Path(event.src_path).resolve()
        path_match = path == self.path
        if path_match and event.event_type == 'modified':
            log.log(11, f'Detected modified event for {path.as_posix()}')
            self.save_backup()
        else:
            verb, level = ('Detected', 11) if path_match else ('Ignoring', 10)
            suffix = f' -> {event.dest_path}' if event.event_type == 'moved' else ''
            log.log(level, f'{verb} {event.event_type} event for {what}: {path.as_posix()}{suffix}')

    def save_backup(self):
        data = self.path.read_bytes()
        if not data:
            log.log(11, 'Skipping backup of empty file')
            return
        data_hash = sha256(data).hexdigest()
        if data_hash != self.last_hash:
            log.debug(f'Data changed - old={self.last_hash} new={data_hash}')
            self.last_hash = data_hash
            dest_path = unique_path(self.backup_dir, self.path.stem, self.path.suffix)
            log.info(f'Saving backup to {dest_path.as_posix()}')
            dest_path.write_bytes(data)
        else:
            log.log(11, f'There were no changes to {self.path.as_posix()} - sha256={data_hash}')


if __name__ == '__main__':
    main()
