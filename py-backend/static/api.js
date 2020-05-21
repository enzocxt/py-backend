var log = function() {
    console.log.apply(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

/*
 ajax 函数
*/
var ajax = function(method, path, data, responseCallback) {
    var r = new XMLHttpRequest()
    // 设置请求方法和请求地址
    r.open(method, path, true)
    // 设置发送的数据的格式为 application/json
    // 这个不是必须的
    r.setRequestHeader('Content-Type', 'application/json')
    // 注册响应函数
    r.onreadystatechange = function() {
        if(r.readyState === 4) {
            // r.response 存的就是服务器发过来的放在 HTTP BODY 中的数据
            responseCallback(r.response)
        }
    }
    // 把数据转换为 json 格式字符串
    data = JSON.stringify(data)
    // 发送请求
    r.send(data)
}

// TODO API
// 获取所有 routes
var apiTodoAll = function(callback) {
    var path = '/api/routes/all'
    ajax('GET', path, '', callback)
}

// 增加一个 routes
var apiTodoAdd = function(form, callback) {
    var path = '/api/routes/add'
    ajax('POST', path, form, callback)
}

// 删除一个 routes
var apiTodoDelete = function(id, callback) {
    var path = '/api/routes/delete?id=' + id
    ajax('GET', path, '', callback)
    // get(path, callback)
}

// 更新一个 routes
var apiTodoUpdate = function(form, callback) {
    var path = '/api/routes/update'
    ajax('POST', path, form, callback)
    //    post(path, form, callback)
}

// load weibo all
var apiWeiboAll = function(callback) {
    var path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 routes
var apiWeiboAdd = function(form, callback) {
    var path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}
