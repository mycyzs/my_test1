# -*- coding:utf-8 -*-
import json

from blueking.component.shortcuts import get_client_by_request
from common.log import logger
from common.mymako import render_json


def test(request):
    return render_json({"username":request.user.username,'result':'ok'})


def search_sys_info(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        return_data = []
        data = {
            "id": "1",
            "sys_name": "test",
            "sys_code": "te",
            "owners": "dd",
            "is_control": "否",
            "department": "dd",
            "comment": "dja",
            "first_owner": "cyz"
        }
        return_data.append(data)
        return render_json({"result": True, "data": return_data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询系统信息失败!!"]})


def add_sys(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        data = {
            "id": "1",
            "sys_name": "test1",
            "sys_code": "te1",
            "owners": "dd",
            "is_control": "否",
            "department": "dd",
            "comment": "dja",
            "first_owner": "lhf"
        }
        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询系统信息失败!!"]})


def modify_sys(request):
    try:
        request_data = json.loads(request.body)
        username = request.user.username
        data = {
            "id": "1",
            "sys_name": request_data['sys_name'],
            "sys_code": request_data['sys_code'],
            "owners": "dkdkdkd",
            "is_control": request_data['is_control'],
            "department": "dd",
            "comment": "dja",
            "first_owner": request_data['first_owner']
        }

        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"添加信息失败!!"]})


def delete_sys(request):
    try:
        request_data = json.loads(request.body)
        username = request.user.username

        return render_json({"result": True, "data": {}})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"添加信息失败!!"]})


