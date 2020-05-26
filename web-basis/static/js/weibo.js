let timeString = function(timestamp) {
    let t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

let commentsTemplate = function(comments) {
    let html = ''
    for(let i = 0; i < comments.length; i++) {
        let c = comments[i]
        let t = `
            <div>
                ${c.content}
            </div>
        `
        html += t
    }
    return html
}

let weiboTemplate = function(weibo) {
    let content = weibo.content
    let id = weibo.id
    // let ut = timeString(weibo.ut)
    let comments = commentsTemplate(weibo.comments)
    const t = `
        <div class="weibo-cell" id='weibo-${id}' data-id="${id}">
            <div>
                [WEIBO]: ${content}
            </div>
            <div class="comment-list">
                ${comments}
            </div>
            <div>
                <input type="hidden" name="weibo_id" value="">
                <input name="content">
                <br>
                <button class="comment-add">添加评论</button>
            </div>
            <button class="weibo-edit">编辑</button>
            <button class="weibo-delete">删除</button>
            <span class='weibo-content'>${content}</span>
        </div>
    `
    return t
}

// 接收一个 weibo 参数
// 将其添加到 weibo-list 元素的最后位置
let insertWeibo = function(weibo) {
    let weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    let weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

// 插入一个编辑元素
let insertEditForm = function(cell) {
    let form = `
        <div class='weibo-edit-form'>
            <input class="weibo-edit-input">
            <button class='weibo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('beforeend', form)
}

let loadWeibos = function() {
    apiWeiboAll(function(r) {
        let weibos = JSON.parse(r)
        for(let i = 0; i < weibos.length; i++) {
            let weibo = weibos[i]
            insertWeibo(weibo)
        }
    })
}

// 为 todo add button 添加事件
let bindEventTodoAdd = function() {
    let b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        let input = e('#id-input-todo')
        let title = input.value
        log('click add', title)
        const form = {
            'title': title,
        }
        apiTodoAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            let todo = JSON.parse(r)
            insertTodo(todo)
        })
    })
}

let bindEventTodoDelete = function() {
    let todoList = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function(event){
        // 获得被点击的元素
        let self = event.target
        if(self.classList.contains('todo-delete')){
            // [套路] 删除这个 todo
            let todoCell = self.parentElement
            const todo_id = todoCell.dataset.id
            apiTodoDelete(todo_id, function(r){
                log('删除成功', todo_id)
                todoCell.remove()
            })
        }
    })
}

let bindEventTodoEdit = function() {
    let todoList = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function(event){
        let self = event.target
        if(self.classList.contains('todo-edit')){
            // 删除这个 todo
            let todoCell = self.parentElement
            insertEditForm(todoCell)
        }
    })
}

let bindEventTodoUpdate = function() {
    let todoList = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    todoList.addEventListener('click', function(event){
        let self = event.target
        if(self.classList.contains('todo-update')){
            log('点击了 update ')
            // 找到父节点 edit 元素
            let editForm = self.parentElement
            // querySelector 是 DOM 元素的方法
            // document.querySelector 中的 document 是所有元素的祖先元素
            let input = editForm.querySelector('.todo-edit-input')
            let title = input.value
            // 用 closest 方法可以找到最近的直系父节点
            let todoCell = self.closest('.todo-cell')
            let todo_id = todoCell.dataset.id
            let form = {
                'id': todo_id,
                'title': title,
            }
            apiTodoUpdate(form, function(r){
                log('更新成功', todo_id)
                let todo = JSON.parse(r)
                let selector = '#todo-' + todo.id
                let todoCell = e(selector)
                let titleSpan = todoCell.querySelector('.todo-title')
                titleSpan.innerHTML = todo.title
                // TODO: 更新时间
                editForm.remove()
            })
        }
    })
}

let bindEvents = function() {
    // bindEventTodoAdd()
    // bindEventTodoDelete()
    // bindEventTodoEdit()
    // bindEventTodoUpdate()
}

let __main = function() {
    bindEvents()
    loadWeibos()
}

__main()
