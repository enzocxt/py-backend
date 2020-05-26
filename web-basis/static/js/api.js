let log = function() {
    console.log.apply(console, arguments)
}

let e = function(sel) {
    // 选择器封装
    return document.querySelector(sel)
}

/*
 [------- ajax 函数 套路 -------]
*/
let ajax = function(method, path, data, responseCallback) {
    let r = new XMLHttpRequest()
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

// ------- TODO API -------
// 获取所有 todo
let apiTodoAll = function(callback) {
    let path = '/api/todo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 todo
let apiTodoAdd = function(form, callback) {
    let path = '/api/todo/add'
    ajax('POST', path, form, callback)
}

// 删除一个 todo
let apiTodoDelete = function(id, callback) {
    let path = '/api/todo/delete?id=' + id
    ajax('GET', path, '', callback)
    // 可以进一步封装 get 请求
    // get(path, callback)
}

// 更新一个 todo
let apiTodoUpdate = function(form, callback) {
    let path = '/api/todo/update'
    ajax('POST', path, form, callback)
    // 可以进一步封装 post 请求
    // post(path, form, callback)
}

// ------- weibo api -------
// load weibo all
let apiWeiboAll = function(callback) {
    let path = '/api/weibo/all'
    ajax('GET', path, '', callback)
}

// 增加一个 weibo
let apiWeiboAdd = function(form, callback) {
    let path = '/api/weibo/add'
    ajax('POST', path, form, callback)
}
