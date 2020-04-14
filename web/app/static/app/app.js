function setCookie(key, value, iDay) {
    var oDate = new Date();
    oDate.setDate(oDate.getDate() + iDay);
    document.cookie = key + '=' + value + ';expires=' + oDate;
}
function removeCookie(key) {
    setCookie(key, '', -1)
}
function getCookie(key) {
    var cookieArr = document.cookie.split('; ');
    for (var i = 0; i < cookieArr.length; i++) {
        var arr = cookieArr[i].split('=');
        if (arr[0] === key) {
            return arr[1];
        }
    }
    return false;
}
function Timer(time) {
    var timer = null;
    var t = time;
    var m = 0;
    var s = 0;
    m = Math.floor(t / 60 % 60);
    m < 10 && (m = '0' + m);
    s = Math.floor(t % 60);
    function countDown() {
        s--;
        s < 10 && (s = '0' + s);
        if (s.length >= 3) {
            s = 59;
            m = "0" + (Number(m) - 1);
        }
        if (m.length >= 3) {
            m = '00';
            s = '00';
            clearInterval(timer);
        }
        $('#remainTime').html(m + ":" + s)
        if (m == 0 && s == 0) {
            clearInterval(timer);
            // console.log("cleared");
            refreshStatus();
        }
    }
    timer = setInterval(countDown, 1000);
    // console.log("start timer " + time);
}
var historyData = {
    type: 'line',
    data: {
        labels: ['1', '2', '3', '4', '5', '6', '7', '8'],
        datasets: [{
            label: '黄金点',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [38.7, 19.3, 10.4, 26.7, 14.3, 8.2, 18, 10],
            fill: false,
        }]
    },
    options: {
        legend: false,
        responsive: true,
        title: {
            display: true,
            text: '黄金点历史'
        },
        tooltips: {
            mode: 'index',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '回合数'
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '数值'
                },
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 20,
                }
            }]
        }
    },
    customOption: {
        amount: 10,
        history: []
    }
};
var rankData = {
    type: 'horizontalBar',
    data: {
        labels: ['alice', 'steve', 'notch', 'herobrine', 'winnie', 'tiger'],
        datasets: [{
            label: '分数',
            backgroundColor: 'rgb(0, 123, 255)',
            borderColor: 'rgb(0, 123, 255)',
            data: [107, 35, 70, -10, -20, 60],
            fill: false,
        }]
    },
    options: {
        elements: {
            rectangle: {
                borderWidth: 2,
            }
        },
        maintainAspectRatio: false,
        responsive: true,
        legend: false,
        title: {
            display: true,
            text: '排行榜'
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: '分数'
                },
                ticks: {
                    suggestedMin: 0,
                    suggestedMax: 20,
                }
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: false,
                    labelString: '用户名'
                },
            }]
        }
    },
    customOption: {
        lastLength: 4,
        lastScore: 0
    }
};
function refreshHistory() {
    var len = historyData.customOption.history.length;
    var i = 0;
    var i_start = historyData.customOption.amount;
    if (i_start >= len || i_start == 0) {
        i_start = 0;
    } else {
        i_start = len - i_start;
    }
    historyData.data.labels = [];
    historyData.data.datasets[0].data = [];
    for (i = i_start; i < len; i++) {
        historyData.data.labels.push(i + 1);
        historyData.data.datasets[0].data.push(historyData.customOption.history[i]);
    }
    // prompt_info("Last goldennum:"+historyData.customOption.history[len-1], 2000);
    window.myLineHistory.update();
}
function refreshRank(scores) {
    let userCount = Object.keys(scores).length;
    let scoreLast = scores[getCookie('username')];
    if (scoreLast) {
        let scoreGain = scoreLast - rankData.customOption.lastScore;
        prompt_info(`你在上回合获得了 ${scoreGain} 分. 当前总分 ${scoreLast} 分.`, 2000);
        rankData.customOption.lastScore = scoreLast;
    }
    rankData.data.labels = [];
    rankData.data.datasets[0].data = [];
    for (let [name, score] of Object.entries(scores).sort((a, b) => b[1] - a[1])) {
        rankData.data.labels.push(name);
        rankData.data.datasets[0].data.push(score);
    }
    if (rankData.customOption.lastLength == userCount) {
        window.myLineRank.update();
    } else {
        rankData.customOption.lastLength = userCount;
        $("#rankDiv").attr("style", `height: ${50 * userCount}px`)
        window.myLineRank.destroy();
        let ctxRank = document.getElementById('rankChart').getContext('2d');
        window.myLineRank = new Chart(ctxRank, rankData);
    }
}
function refreshStatus() {
    let json = { roomid: getCookie("roomid") }
    $.get("roomStatus/", json, function (data, status) {
        if (data == "on") {
            $.ajax({
                url: "getStatus/",
                data: json,
                method: "GET",
                statusCode: {
                    404: function () {
                        prompt_fail("房间不存在", 5000);
                        Timer(7);
                    },
                    400: function () {
                        prompt_fail("请求非法", 5000);
                        Timer(7);
                    },
                    500: function () {
                        prompt_fail("房间错误，7 秒后自动重试", 5000);
                        Timer(7);
                    }
                },
                success: function (data) {
                    let json = JSON.parse(data);
                    historyData.customOption.history = json.history.goldenNums;
                    refreshHistory();
                    refreshRank(json.scores);
                    Timer(json.time + 1);
                }
            })
        }
    })
}
$(document).ready(function () {
    $.ajax({
        url: "userStatus/",
        method: "GET",
        // statusCode: {
        //     404: function () {
        //     }
        // },
        success: function (data) {
            $('#pUsername').html("当前登陆：" + data)
            $('#login-panel').css("display", "none")
            $('#user-info').css("display", "block")
            setCookie("username", data, 1);
        }
    })
    $('#pRoomid').html(getCookie('roomid'))
    var ctxHistory = document.getElementById('historyChart').getContext('2d');
    window.myLineHistory = new Chart(ctxHistory, historyData);
    var ctxRank = document.getElementById('rankChart').getContext('2d');
    window.myLineRank = new Chart(ctxRank, rankData);
    Timer(1);
})
function tryChgLen(len) {
    historyData.customOption.amount = len;
    refreshHistory();
    // console.log("set " + len);
}
$('#setLenBtn1').click(
    function tryChg() {
        tryChgLen(10);
    }
)
$('#setLenBtn2').click(
    function tryChg() {
        tryChgLen(30);
    }
)
$('#setLenBtn3').click(
    function tryChg() {
        tryChgLen(100);
    }
)
$('#setLenBtn4').click(
    function tryChg() {
        tryChgLen(0);
    }
)
$('#setRoomBtn').click(
    function trySetRoom() {
        var roomid = $('input[name="roomid"]').val();
        var json = { "roomid": roomid }
        // console.log(roomid);
        $.get('roomStatus/', json, function (data, status) {
            if (data == "on") {
                setCookie('roomid', roomid, 1);
                $('#pRoomid').html(roomid)
                prompt_success("成功加入房间", 2000);
                location.reload();
            } else {
                prompt_fail("房间已关闭", 2000);
            }
        })
    }
)
$('#loginBtn').click(
    function tryLogin() {
        var uname = $('input[name="username"]').val();
        var json = { "name": uname }
        $.ajax({
            url: "userReg/",
            data: json,
            method: "GET",
            statusCode: {
                400: function () {
                    prompt_fail("用户名非法", 5000);
                    Timer(7);
                }
            },
            success: function (data) {
                setCookie("username", data, 1);
                $('#pUsername').html("当前登陆：" + uname)
                $('#login-panel').css("display", "none")
                $('#user-info').css("display", "block")
                switch (data) {
                    case "exist":
                        prompt_info("用户已存在", 2000);
                        break;
                    case "success":
                        prompt_success("操作成功", 2000);
                        break;
                    default:
                        prompt_fail(data, 2000);
                }
            }
        })
    }
)
$('#logoutBtn').click(
    function tryLogout() {
        $.ajax({
            url: "userOut/",
            method: "GET",
            statusCode: {
                400: function () {
                    prompt_fail("用户状态错误", 5000);
                    Timer(7);
                },
                404: function () {
                    prompt_fail("无用户数据", 5000);
                    Timer(7);
                },
            },
            success: function (data) {
                switch (data) {
                    case "success":
                        prompt_success("注销成功", 2000);
                        break;
                    default:
                        console.log(data);
                        prompt_fail("未知错误", 2000);
                }
            }
        })
        removeCookie("username");
        $('#pUsername').html("")
        $('#login-panel').css("display", "block")
        $('#user-info').css("display", "none")
    }
)
$('#submitNumBtn').click(
    function sumbitNum() {
        var num1 = $('input[name="num1"]').val();
        var num2 = $('input[name="num2"]').val();
        var roomid = getCookie("roomid");
        var json = { "roomid": roomid, "num1": num1, "num2": num2 }
        // console.log(json);
        $.ajax({
            url: "userAct/",
            method: "GET",
            data: json,
            statusCode: {
                400: function () {
                    prompt_fail("参数错误，请检查数字范围等", 2000);
                },
                403: function () {
                    prompt_warning("请先登录", 5000);
                    Timer(7);
                },
            },
            success: function () {
                prompt_success("提交成功", 2000);
            }
        })
    }
)
var prompt = function (message, style, time) {
    style = (style === undefined) ? 'alert-success' : style;
    time = (time === undefined) ? 1200 : time;
    $('<div>')
        .appendTo('body')
        .addClass('alert-prompt ' + style)
        .html(message)
        .show()
        .delay(time)
        .fadeOut();
};

var prompt_success = function (message, time) {
    prompt(message, 'alert-success-prompt', time);
};
var prompt_fail = function (message, time) {
    prompt(message, 'alert-danger-prompt', time);
};
var prompt_warning = function (message, time) {
    prompt(message, 'alert-warning-prompt', time);
};

var prompt_info = function (message, time) {
    prompt(message, 'alert-info-prompt', time);
};
