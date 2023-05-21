import os
from pathlib import Path


def cwd() -> Path:
    return Path.cwd()


def home() -> Path:
    return Path.home()


def abs(path_x: Path) -> Path:
    return path_x.absolute()


def path2str(path: Path) -> str:
    return path.as_posix().strip()


def str2path(path_s: str) -> Path:
    return Path(path_s)


def exists(path: Path) -> bool:
    return path.exists()


def remove(path: Path) -> bool:
    if not path.exists():
        return False
    path.unlink()
    return True


def join(path0: Path, path1: Path) -> Path:
    return path0.joinpath(path1)


def relative_to(path_x: Path, to_path_x: Path) -> str:
    p0 = path_x.resolve().as_posix()
    p1 = to_path_x.resolve().as_posix()
    pr = p0.replace(f'{p1}/', '')
    return pr


def pathlist2strlist(path_lst: list) -> list:
    lst = [path.as_posix() for path in path_lst]
    return lst


def strlist2pathlist(path_lst: list) -> list:
    lst = [Path(path_s) for path_s in path_lst]
    return lst


def rlist_path(path: Path, match: str) -> list:
    return list(path.rglob(match))


def list_path(path_x: Path, match: str = None) -> list:
    if match is None:
        lst = [x for x in path_x.iterdir()]
    else:
        lst = [x for x in path_x.glob(match)]
    return lst


def update_path_name(path: Path, s0: str, s1: str) -> Path:
    name = path.name.replace(s0, s1)
    path_trg = path.with_name(name)
    return path_trg


def chmod(path_x: Path, mode: int = 0o777):
    if not path_x.exists():
        raise Exception(f"{path_x} does not exist")
    path_x.chmod(mode=mode)


def make_dir(path: Path, mode: int = 0o777):
    path.mkdir(exist_ok=True, mode=mode)
    path.chmod(mode=mode)


def rmake_dir(path: Path, mode: int = 0o777):
    path_abs = path.absolute()
    for p in path_abs.parents:
        p.mkdir(exist_ok=True, mode=mode)
    path_abs.mkdir(exist_ok=True, mode=mode)


def make_dir_of_file(path: Path, mode: int = 0o777):
    path_abs_parent = path.absolute().parent
    rmake_dir(path_abs_parent, mode)
