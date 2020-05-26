
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
* 4. 服务器给浏览器一个页面响应
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>
...
</html>
```
* 5. 浏览器把新的页面显示出来


TODO 带用户验证功能

## v0.6
用 jinja 模板实现 todo 程序

用 jinja 模板实现注册/登录


## v0.7
### 摘要算法/用处/常见套路
摘要算法是一种能产生特殊输出格式的算法  
给定任意长度的数据生成定长的密文  
摘要结果是不可逆的, 不能被还原为原数据  
理论上无法通过反向运算取得原数据内容  
并且, 一个安全的摘要算法是无法找到碰撞的  
碰撞是说, 两个不一样的数据, 产生了一样的结果  
通常只被用来做数据完整性验证
* 比如网站在下载页面公布文件的 sha1 摘要结果
* 你下载后自己生成结果来对比
* 就能知道文件是否被篡改
或者是用来加密用户密码


常用的摘要算法主要有 md5 和 sha1
* md5 的输出结果为 32 字符
* sha1 的输出结果为 40 字符

### 实现一个微博程序
CRUD(CREATE RETRIEVE UPDATE DELETE) 操作


## v0.8
Chrome 浏览器有一个 bug，它在请求一个数据之后，马上回建立一个空的连接，然后挂起占用连接。  
如果是单进程、单线程的连接，就会一直卡住，接收不到新请求。  

前端用 ajax 发送 HTTP 请求到后端  
后端 API  
ajax 跨域  
ajax todo 程序（增强功能）  
ajax weibo 和动态评论  
