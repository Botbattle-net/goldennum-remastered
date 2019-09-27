

import json
import random
import os
import sys
import time

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from importlib import import_module

import web.secret_key as secret_key
# from . import datamaker

from app.models import User, Room
# Create your views here.


def index(request):
    return render(request, 'app/game.html')


def help(request):
    return render(request, 'app/help.html')


def admin(request):
    if not request.user.is_staff:
        return HttpResponseRedirect("/admin/login/?next=/goldennum/admin/")
    rooms = Room.objects.all()
    return render(request, 'app/admin.html', {'rooms': rooms})


def getStatus(request):
    retval = {
        "status": "200",
        "roomid": "",
        "history": [],
        "scores": {},
        "time": 0
    }
    roomid = request.GET.get('roomid', None)
    if not roomid:
        return HttpResponseBadRequest()

    if roomid == 'false':
        return HttpResponseBadRequest()

    for c in roomid:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponseBadRequest()

    room = get_object_or_404(Room, roomid=roomid)

    users = User.objects.filter(room=roomid)

    retval['roomid'] = roomid
    retval['history'] = json.loads(room.history)
    retval['time'] = int(room.time) - (int(time.time()) - int(room.lastTime))
    retval['scores'] = {user.name: int(user.score) for user in users}

    if retval['time'] <= 0:
        room.status = "off"
        room.save()
        return HttpResponseServerError()

    return HttpResponse(json.dumps(retval))


def userReg(request):
    # print(request.GET['name'])
    name = request.GET.get('name', None)

    if name == 'false':
        return HttpResponseBadRequest()
    if len(name) > 20 or len(name) < 1:
        return HttpResponseBadRequest()
    for c in name:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponseBadRequest()

    if request.session.get("name") is None:
        users = User.objects.filter(name=name).filter(room="NULL")
        if users:
            user = users[0]
            if user.status == "on":
                return HttpResponse("exist")
            else:
                request.session['name'] = name
                user.status = "on"
                user.save()
                return HttpResponse("success")
        else:
            newUser = User()
            newUser.name = name
            newUser.room = "NULL"
            newUser.score = "0"
            newUser.act = ""
            newUser.status = "on"
            newUser.useScript = str()
            newUser.save()
            request.session['name'] = name
            return HttpResponse("success")
    else:
        return HttpResponse("success")


def userOut(request):
    name = request.session.get('name', None)
    if name is None:
        return HttpResponseBadRequest

    user = get_object_or_404(User, name=name, room="NULL")

    user.status = "off"
    user.save()
    del request.session['name']
    return HttpResponse("success")


def userAct(request):
    name = request.session.get('name', None)
    if name is None:
        return HttpResponseForbidden()

    try:
        roomid = request.GET['roomid']
        num1 = float(request.GET['num1'])
        num2 = float(request.GET['num2'])
    except:
        return HttpResponseBadRequest()

    if roomid == 'false':
        return HttpResponseBadRequest()

    for c in roomid:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponseBadRequest()

    if num1 >= 100 or num1 <= 0 or num2 >= 100 or num2 <= 0:
        return HttpResponseBadRequest()

    users = User.objects.filter(name=name).filter(room=roomid)
    if users:
        user = users[0]
    else:
        user = User()
        user.name = name
        user.room = roomid
        user.score = "0"
        user.useScript = str()

    user.act = str(num1) + " " + str(num2)
    user.save()

    return HttpResponse("success")


def userStatus(request):
    name = request.session.get('name', None)
    if name is None:
        return HttpResponseNotFound()
    return HttpResponse(name)


def getAct(request):
    try:
        key = request.GET['key']
        roomid = request.GET['roomid']
    except:
        return HttpResponseBadRequest()

    if key != secret_key.secret_key:
        return HttpResponseForbidden()

    room = get_object_or_404(Room, roomid=roomid)

    # retjson = datamaker.randomUsers()
    print(f"Get getAct from room {roomid}")

    users = User.objects.filter(room=roomid)
    retjson = {
        "userNum": len(users),
        "users": []
    }
    for user in users:
        nums = [float(n) for n in user.act.split()]
        user.act = "0 0"
        user.save()

        # Update user act history of this room
        # print(json.loads(room.history))
        history = json.loads(room.history)
        if user.name not in history["userActs"]:
            history["userActs"][user.name] = []
        history["userActs"][user.name].append(nums)
        room.history = json.dumps(history)

        retjson["users"].append({
            "userName": user.name,
            "userAct": nums
        })
    room.save()
    print(retjson)
    return HttpResponse(json.dumps(retjson))


def submitResult(request):
    try:
        key = request.GET['key']
        roomid = request.GET['roomid']
    except:
        return HttpResponseBadRequest()

    if key != secret_key.secret_key:
        return HttpResponseForbidden()

    print(f"Get submitResult from room {roomid}")

    try:
        result = json.loads(request.body.decode('utf-8'))
    except:
        try:
            result = json.loads(request.body)
        except:
            return HttpResponseBadRequest()

    room = Room.objects.get(roomid=roomid)

    # Update golden number history of this room
    if result['goldenNum'] != 0:
        history = json.loads(room.history)
        history['goldenNums'].append(result['goldenNum'])
        room.history = json.dumps(history)
    # print(json.loads(room.history))

    room.time = str(result['roundTime'])
    room.lastTime = str(int(time.time()))
    room.save()

    for userInfo in result['users']:
        userName = userInfo['userName']
        user = User.objects.get(name=userName, room=roomid)
        user.score = str(int(user.score) + userInfo['userScore'])
        user.save()

    print(result)

    return HttpResponse("success")


def roomStatus(request):
    roomid = request.GET.get('roomid', None)
    if roomid is None:
        return HttpResponseBadRequest()

    for c in roomid:
        if not ('0' <= c <= '9' or 'a' <= c <= 'z' or 'A' <= c <= 'Z'):
            return HttpResponseBadRequest()

    rooms = Room.objects.filter(roomid=roomid)
    if not rooms:
        return HttpResponse("off")
    else:
        return HttpResponse("on")


def startRoom(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    try:
        roomid = request.GET['roomid']
        timer = request.GET['time']
    except:
        return HttpResponseBadRequest()

    cmd = f'python3 plug-ins/goldennum.py "{secret_key.secret_key}" {roomid} {timer}'
    cmd_run = f'nohup {cmd} > tmp/logs/{roomid}.out 2>&1'

    if sys.platform == "win32":
        cmd_run = f'start /b {cmd_run}'
    else:
        cmd_run = f'{cmd_run} &'

    rooms = Room.objects.filter(roomid=roomid)
    if not rooms:
        newRoom = Room()
        newRoom.status = "on"
        newRoom.roomid = roomid
        newRoom.time = timer
        newRoom.cmd = cmd.replace('"', '')
        newRoom.lastTime = str(int(time.time()))
        newRoom.history = json.dumps({
            "goldenNums": [],
            "userActs": {}
        })
        newRoom.save()
        os.makedirs("./tmp/logs", exist_ok=True)
        os.system(cmd_run)
        return HttpResponse("Room started new")
    else:
        room = rooms[0]
        # flag = os.system('ps axu | grep "' + room.cmd +'" | grep -v "grep" | wc -l')
        # print(json.dumps(flag))
        if room.status != "on":
            room.status = "on"
            room.time = timer
            room.cmd = cmd.replace('"', '')
            room.lastTime = str(int(time.time()))
            room.save()
            os.makedirs("./tmp/logs", exist_ok=True)
            os.system(cmd_run)
            return HttpResponse("Room restarted")
        else:
            return HttpResponse("Room have started")


def stopRoom(request):
    if not request.user.is_staff:
        return HttpResponseForbidden()

    try:
        # key = request.GET['key']
        roomid = request.GET['roomid']
    except:
        HttpResponseBadRequest()

    try:
        room = Room.objects.get(roomid=roomid)
    except:
        return HttpResponseNotFound()

    if sys.platform == "win32":
        room_cmd = room.cmd[len("python3 "):]  # skip 'python3 ' prefix
        cmd_kill = f'wmic process where "COMMANDLINE LIKE \'%{room_cmd}%\'" call terminate'
    else:
        cmd_kill = f'pkill -f "{room.cmd}"'
    os.system(cmd_kill)
    room.status = "off"
    room.save()
    return HttpResponse("Room stopped")
