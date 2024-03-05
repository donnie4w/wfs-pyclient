"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
"""
import random

from wfsclient import *

import pytest


def newClient() -> WfsClient:
    client = WfsClient()
    wa = client.newConnect(False, "127.0.0.1", 6802, "admin", "123")
    print(wa)
    return client


def test_Append():
    client = newClient()
    wf = WfsFile()
    wf.name = "test/py/1.jpeg"
    wf.data = open('1.jpeg', 'rb').read()
    client.Append(wf)


def test_Delete():
    client = newClient()
    ack = client.Delete("test/py/1.jpeg")
    print("delete ack:", ack)


def test_Get():
    client = newClient()
    wd = client.Get("test/py/1.jpeg")
    if wd.data is not None:
        length = len(wd.data)
        print("file length:", length)
    else:
        print("file not exist")
