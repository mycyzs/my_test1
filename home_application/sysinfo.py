# -*- coding:utf-8 -*-
import cStringIO
import codecs
import datetime
import json

from django.http import StreamingHttpResponse

from blueking.component.shortcuts import get_client_by_request
from common.log import logger
from common.mymako import render_json
from home_application.all_api import install_mysql_by_script
from home_application.models import Host, Task


def test(request):
    return render_json({"username":request.user.username,'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})


def search_sys_info(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        templates = Host.objects.filter(biz_name__contains=request_data['biz_name'], name__contains=request_data["template"])
        return_data = []
        for t in templates:
            return_data.append({
                "id": t.id,
                "name": t.name,
                "biz_name": t.biz_name,
                "script": t.script,
                "max_num": t.max_num,
                "create_time": t.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "comment": t.comment,
            })

        return render_json({"result": True, "data": return_data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询模板信息失败!!"]})


def search_task_info(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        templates = Task.objects.filter(task_name__contains=request_data['task_name'], task_type__contains=request_data['task_type'])
        return_data = []
        for t in templates:
            return_data.append({
                "id": t.id,
                "task_name": t.task_name,
                "host": t.host,
                "template": t.tem.name,
                "task_type": u'立即' if t.task_type == 'now' else u'周期',
                "create_time": t.create_time.strftime("%Y-%m-%d %H:%M:%S"),

            })

        return render_json({"result": True, "data": return_data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询任务信息失败!!"]})


def search_template(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        biz_list = request_data['biz_l']
        biz_name = ''
        for biz in biz_list:
            if biz['id'] == int(request_data['biz']):
                biz_name = biz['text']
        templates = Host.objects.filter(biz_name=biz_name)

        return_data = []
        for t in templates:
            return_data.append({
                "id": t.id,
                "text": t.name

            })

        return render_json({"result": True, "data": return_data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"查询模板信息失败!!"]})

def add_sys(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        biz_list = request_data['biz_l']
        biz_name = ''
        for biz in biz_list:
            if biz['id'] == int(request_data['biz']):
                biz_name = biz['text']

        data = {
            "name": request_data['template'],
            "biz_name": biz_name,
            "script": request_data['script'],
            "max_num": request_data['max_num'],
            "create_time": datetime.datetime.now(),
            "comment": request_data['comment'],

        }

        template = Host.objects.create(**data)
        data['id'] = template.id
        data['create_time'] = template.create_time.strftime("%Y-%m-%d %H:%M:%S")
        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"新增模板失败!!"]})


def add_task(request):
    try:
        username = request.user.username
        request_data = json.loads(request.body)
        biz_list = request_data['biz_l']
        tem = Host.objects.get(id=request_data['template'])
        etra = {}
        if request_data['task_type'] == 'set_time':
            etra['time'] = request_data['time']
            etra['late_time'] = request_data['late_time']

        data = {
            "task_name": request_data['task_name'],
            "host": request_data['host'],
            "task_type": request_data['task_type'],
            "create_time": datetime.datetime.now(),
            "etra": etra,
            "tem": tem
        }
        task = Task.objects.create(**data)
        script = tem.script
        #执行脚本
        if request_data['task_type'] == 'now':
            install_mysql_by_script(username, int(request_data['biz']), [request_data['host']], script)

        del data['tem']
        data['id'] = task.id
        data['create_time'] = task.create_time.strftime("%Y-%m-%d %H:%M:%S")
        data['template'] = task.tem.name
        data['task_type'] = u'立即' if task.task_type == 'now' else u"周期"
        data['biz'] = request_data['biz']
        data['tem_id'] = tem.id
        return render_json({"result": True, "data": data})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"新增任务失败!!"]})


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
        Host.objects.filter(id=request_data['id']).delete()

        return render_json({"result": True, "data": {}})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"删除失败!!"]})


def parse_time():
    # 今天的日期字符串： 2019-05-30  ,hours 表示小时，days表示天数
    start_time = (datetime.date.today() - datetime.timedelta(days=0)).strftime('%Y-%m-%d')

    # 转换成今天凌晨字符串
    start_t = start_time + " 00:00:00"
    start_end = start_time + " 23:59:59"

    # 转成datetime格式，可以跟数据库date类型的字段相比较
    start_ts = datetime.datetime.strptime(start_t, "%Y-%m-%d %H:%M:%S")
    start_end = datetime.datetime.strptime(start_end, "%Y-%m-%d %H:%M:%S")

    # 获取一个小时前的date类型
    one_hours_before = datetime.datetime.now() - datetime.timedelta(hours=1)

    my_data = {
        'name': "dd",
        'is_success': True,
        'text': "DKDKDKDK",
        'when_created': "DJDJDJDJ",
        'create_time': datetime.datetime.now()
    }
    # new_obj = Host.objects.create(**my_data)

    # 查询数据库
    obj = Host.objects.filter(create_time__gt=start_ts)

    # 查询出来的时间转成字符串展示
    for o in obj:
        str_time = o.create_time.strftime("%Y-%m-%d %H:%M:%S")


def down_loa():
    # rows = ["dev", "info", "error", "2019-2-2", "data"]
    def DownLoadLog(rows, fname="log-info.csv"):
        headers = ["环境", "类型", "日志级别", "时间", "日志信息"]

        def getContent(fileObj):
            fileObj.seek(0)
            data = fileObj.read()
            fileObj.seek(0)
            fileObj.truncate()
            return data

        def genCSV(rows, headers):
            # 准备输出
            output = cStringIO.StringIO()
            # 写BOM
            output.write(bytearray([0xFF, 0xFE]))
            if headers is not None and isinstance(headers, list):
                headers = codecs.encode("\t".join(headers) + "\n", "utf-16le")
                output.write(headers)
                yield getContent(output)
            for row in rows:
                rowData = codecs.encode("\t".join(row) + "\n", "utf-16le")
                output.write(rowData)
                yield getContent(output)  # 因为StreamingHttpResponse需要一个Iterator
            output.close()

        resp = StreamingHttpResponse(genCSV(rows, headers))
        resp["Content-Type"] = "application/vnd.ms-excel; charset=utf-16le"
        resp["Content-Type"] = "application/octet-stream"
        resp["Content-Disposition"] = "attachment;filename=" + fname
        resp["Content-Transfer-Encoding"] = "binary"
        return resp

    # def download_file(file_path, file_name):
    #     try:
    #         file_path = file_path
    #         file_buffer = open(file_path, 'rb').read()
    #         response = HttpResponse(file_buffer, content_type='APPLICATION/OCTET-STREAM')
    #         response['Content-Disposition'] = 'attachment; filename=' + file_name
    #         response['Content-Length'] = os.path.getsize(file_path)
    #         return response
    #     except Exception as e:
    #         logger.exception("download file error:{0}".format(e.message))
    #
    #
    # def download_log(log_list):
    #     f = codecs.open('Log-Info.csv', 'wb', "gbk")
    #     writer = csv.writer(f)
    #     writer.writerow(["环境", "类型", "日志级别", "时间", "日志信息"])
    #     writer.writerows(log_list)
    #     f.close()
    #     file_path = "{0}/Log-Info.csv".format(PROJECT_ROOT).replace("\\", "/")
    #     file_name = "Log-Info.csv"
    #     return download_file(file_path, file_name)


def exute_script(request):
    try:
        request_data = json.loads(request.body)
        username = request.user.username
        task = Task.objects.get(request_data['id'])
        tem = Host.objects.get(id=request_data['tem_id'])
        result = install_mysql_by_script(username, int(request_data['biz']), task.host, tem.script)

        return render_json({"result": True, "data": {}})
    except Exception as e:
        logger.error(e)
        return render_json({"result": False, "msg": [u"执行任务失败!!"]})