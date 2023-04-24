#!/usr/bin/env python3
# coding: utf-8

from pdb import set_trace
# import pprint

import os
import argparse

from ulalib.bottle import Bottle
from ulalib.bottle import request, static_file
from ulalib.save_back import save_text_data_back
from ulalib.save_back import save_corpus_data_back
from ulalib.update_data import UpdateData
from ulalib.ula_setting import *

app = Bottle()

ROOT_PATH = '.'

# def prn_path():
#     print("")
#     cwd = os.getcwd()
#     abspath = os.path.abspath(__file__)
#     dirname = os.path.dirname(abspath)
#     basename = os.path.basename(abspath)
#     print("cwd:%s" % cwd)
#     print("abspath:%s" % abspath)
#     print("dirname:%s" % dirname)
#     print("basename:%s" % basename)


def prn_params(rqs):
    print("===============")
    print("query_string:")
    print(rqs.query_string)
    print("url_args:")
    for k, v in rqs.url_args.items():
        print(k + "  :  " + v)
    print("params:")
    for k, v in rqs.params.items():
        print(k + "  :  " + v)


def request_params(rqs):
    query = rqs.query_string
    if query.strip() == '':
        return {}
    pars = {}
    lst = query.split('&')
    for item in lst:
        kv = item.split('=')
        k = kv[0].strip()
        v = "" if len(kv) < 2 else kv[1]
        pars[k] = v
    return pars


def request_data(rqs):
    d = dict(rqs.headers.items())
    cl = d['Content-Length'].strip()
    le = int(cl)
    data = rqs.body.read(le)
    return data


@app.route('/', method='GET')
def hello():
    # prn_params(request)
    # pars = request_params(request)
    # print("hello")
    # print(request.url)
    # print(pars)
    return static_file("index.html", root=ROOT_PATH)


@app.route('/<filepath:path>', nethod='GET')
def server_static(filepath):
    if 'favicon' in filepath:
        return
    # prn_params(request)
    # pars = request_params(request)
    # print("server_static")
    # print(request.url)
    # print(pars)
    s = static_file(filepath, root=ROOT_PATH)
    return s

@app.route('/diff', method='GET')
def diff_text_corpus():
    try:
        # prn_params(request)
        pars = request_params(request)
        name = pars.get("name", None)
        if name is None:
            return ""
        text_name = os.path.basename(name)
        upd_data = UpdateData()
        upd_data.set_text_name(text_name)
        upd_data.read_corpus_form_csv()
        upd_data.read_text_form_csv()
        upd_data.set_text_flled_idx_lst()
        rows = upd_data.set_text_corpus_diff_lst()
        data = {"data": rows}
    except IOError as e:
        msg = f"ERRORO diff_text_corpus()"
        raise Exception(f"{msg}\n{e}")
    return data


@app.route('/write/<filepath:path>', method='POST')
def write(filepath=""):
    data = request_data(request)
    try:
        fpath = os.path.join(ROOT_PATH, filepath)
        fw = open(fpath, "wb")
        fw.write(data)
        fw.close()
        os.chmod(fpath, 0o777)
        save_text_data_back(fpath)
    except IOError as e:
        msg = f"ERRORO write()"
        raise Exception(f"{msg}\n{e}")
    return "1"


@app.route('/updatecorpus/<filepath:path>', method='POST')
def update_corpus(filepath=""):
    try:
        #aggiorna corpus.form.csv
        #         corpus.omogr.json
        save_corpus_data_back(CORPUS_NAME)
        text_name = os.path.basename(filepath)
        upd_data = UpdateData()
        upd_data.set_text_name(text_name)
        rows = upd_data.update_corpus_forms()
        # righe del corpus sovrascritte con valori diversi
        # form_text$form_corpus
        # row=form|formkey...$forma|formakey|..
        data = {"data": rows}
    except IOError as e:
        msg = f"ERRORO update_corpus()"
        raise Exception(f"{msg}\n{e}")
    return data


@app.route('/updatetext/<filepath:path>', method='POST')
def update_text(filepath=""):
    try:
        text_name = os.path.basename(filepath)
        upd_data = UpdateData()
        upd_data.set_text_name(text_name)
        upd_data.update_text_forms()
    except IOError as e:
        msg = f"ERRORO update_text()"
        raise Exception(f"{msg}\n{e}")
    return "1"



@app.error(403)
def mistake403(code):
    return f'Error 403 There is a mistake in your url! '


@app.error(404)
def error404(error):
    return 'Erro 404 Nothing here, sorry'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        dest="ip",
        required=False,
        metavar="",
        default="0.0.0.0",
        help="-i <ip> (Default 0.0.0.0")
    parser.add_argument(
        '-p',
        dest="port",
        required=False,
        metavar="",
        default="8080",
        help="-p <port> (Default 80")
    parser.add_argument(
        '-r',
        dest="root",
        required=False,
        metavar="",
        default=".",
        help="-r <root> (Default . ")
    parser.add_argument(
        '-d',
        dest="debug",
        required=False,
        metavar="",
        default="0",
        help="-d 0/1 (Default 0 ")
    args = parser.parse_args()
    ip = args.ip
    port = int(args.port)
    ROOT_PATH = args.root
    print(f"{ip} {port} {ROOT_PATH}")
    if args.debug == '1':
        app.run(host=ip, port=port, debug=True, quiet=False, reload=False)
    else:
        print("Hit Ctrl-C to quit.")
        app.run(host=ip, port=port, debug=False, quiet=True)
else:
    application = app
