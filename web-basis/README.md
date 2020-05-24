
## v0.5
routes/todo
* 显示所有 todo
* 增加 todo
* 编辑 todo
* 删除 todo

models/todo
* todo 数据 class

templates/todo
* todo_index.html
* todo_edit.html
    

点击添加按钮增加一个新的 todo 的时候，程序流程如下：
* 1. 浏览器提交一个表单给服务器（POST 请求）
```
POST /todo/add HTTP/1.1
Content-Type: application/x-www-form-urlencoded

title=xxx
```
* 2. 服务器解析表单数据，并增加一条新数据，并返回 302 响应
```
HTTP/1.1 302 REDIRECT
Location: /todo
```
* 3. 浏览器根据 302 中的地址（Location），发送一条新的 GET 请求
```
GET /todo HTTP/1.1
Host: xxx
```
4. 服务器给浏览器一个页面响应
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>
...
</html>
```
5. 浏览器把新的页面显示出来


TODO 带用户验证功能

## v0.6
用 jinja 模板实现 todo 程序

用 jinja 模板实现注册/登录
