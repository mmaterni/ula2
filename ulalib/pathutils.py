#!/usr/bin/env python3
# coding: utf-8
import os
import pathlib as pth


def cwd():
    pwd = pth.Path().cwd()
    return pwd


def home():
    home = pth.Path().home()
    return home


def abs(path_x):
    try:
        if isinstance(path_x, str):
            path = pth.Path(path_x)
        else:
            path = path_x
        return path.absolute()
    except Exception as e:
        msg = f"ERROR abs() {path_x}\n{e}"
        raise (Exception(msg))


def path2str(path):
    return path.as_posix().strip()


def str2path(path_s):
   return pth.Path(path_s)

def exists(path_s):
    return pth.Path(path_s).exists()

def remove(path_s):
    if not pth.Path(path_s).exists():
        return False
    pth.Path(path_s).unlink()
    return True


def join(path0, path1):
    # TODO verificare tipo
    return pth.Path().joinpath(path0, path1)


def relative(path0, path1):
    print("relative obsolete")
    input("ERROR pathutils.py ")
    input("!!")
    # if path0 is None:
    #     return cwd if path1 is None else path1
    # elif path1 is None :
    #     return cwd if path0 is None else path0
    # else:
    #     return pth.Path(path0).relative_to(path1)
    return None


def relative_to(path_x, to_path_x):
    """
    dir di path relativa a to_path
    restituise una str
    """
    if isinstance(path_x, str):
        path_x = pth.Path(path_x)
    if isinstance(to_path_x, str):
        to_path_x = pth.Path(to_path_x)
    p0 = path2str(path_x.resolve())
    p1 = path2str(to_path_x.resolve())
    pr = p0.replace(f'{p1}/', '')
    return pr


def pathlist2strlist(path_lst):
    path_lst = [] if path_lst is None else path_lst
    lst = [path2str(x) for x in path_lst]
    return lst


def strlist2pathlist(path_s_lst):
    path_s_lst = [] if path_s_lst is None else path_s_lst
    lst = [str2path(x) for x in path_s_lst]
    return lst


# lista ricorsiva
def rlist_path(path, match):
    lst = [x for x in path.rglob(match)]
    return lst


def list_path(path_x, match=None):
    if isinstance(path_x, str):
        path = pth.Path(path_x)
    else:
        path = path_x
    if match is None:
        lst = [x for x in path.iterdir()]
    else:
        lst = [x for x in path.glob(match)]
    return lst


# ritorna una path con path.name modificato
# da replace s0=>s1
def update_path_name(path, s0, s1):
    try:
        name = path.name.replace(s0, s1)
        path_trg = path.with_name(name)
        return path_trg
    except Exception as e:
        msg = f"ERROR update_path_name {os.linesep}{e}"
        raise (Exception(msg))


def chmod(path_x, mode=0o777):
    if isinstance(path_x, str):
        path = pth.Path(path_x)
    else:
        path = path_x
    if not path.exists():
        raise (Exception(f"{path} Not Exists"))
    try:
        #os.chmod(path, stat.S_IRWXG + stat.S_IRWXU + stat.S_IRWXO)
        path.chmod(mode=mode)
    except Exception as e:
        msg = f"chmod() {os.linesep}{e}"
        raise (Exception(msg))


def make_dir(path_x, mode=0o777):
    if isinstance(path_x, str):
        path = pth.Path(path_x)
    else:
        path = path_x
    path.mkdir(exist_ok=True, mode=mode)
    path.chmod(mode=mode)


# crea ricorsivamente le dir
def rmake_dir(path_x, mode=0o777):
    try:
        if isinstance(path_x, str):
            path = pth.Path(path_x)
        else:
            path = path_x
        path_abs = path.absolute()
        ps = path_abs.parts
        path_dir = ps[0]
        for p in ps[1:]:
            path_dir = pth.Path().joinpath(path_dir, p)
            path_dir.mkdir(exist_ok=True, mode=mode)
    except Exception as e:
        msg = f"ERROR rmake_dir() {path_x}\n{e}"
        raise (Exception(msg))


# def rmake_dir(path_x, mode=0o777):
#     try:
#         path = pth.Path(path_x) if isinstance(path_x, str) else path_x
#         path_abs = path.absolute()
#         for p in path_abs.parents:
#             p.mkdir(exist_ok=True, mode=mode)
#         path_abs.mkdir(exist_ok=True, mode=mode)
#     except Exception as e:
#         raise Exception(f"ERROR rmake_dir() {path_x}\n{e}")


def make_dir_of_file(path_x, mode=0o777):
    # crea tutte le dir di un file_path
    try:
        if isinstance(path_x, str):
            path = pth.Path(path_x)
        else:
            path = path_x
        path_abs = path.absolute()
        path_abs_parent = path_abs.parent
        rmake_dir(path_abs_parent, mode)
    except Exception as e:
        msg = f"ERROR make_dir_of_file() {path_x}\n{e}"
        raise (Exception(msg))
