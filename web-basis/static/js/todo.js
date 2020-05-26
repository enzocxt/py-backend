let timeString = function(timestamp) {
    let t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

let todoTemplate = function(todo) {
    let title = todo.title
    let id = todo.id
    let ut = timeString(todo.ut)
    // data-xx 是自定义标签属性的语法
    // 通过这样的方式可以给任意标签添加任意属性
    // 假设 d 是 这个 div 的引用
    // 这样的自定义属性通过  d.dataset.xx 来获取
    // 在这个例子里面, 是 d.dataset.id
    let t = `
        <div class="todo-cell" id='todo-${id}' data-id="${id}">
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">删除</button>
            <span class='todo-title'>${title}</span>
            <time class='todo-ut'>${ut}</time>
        </div>
    `
    return t
    /*
    上面的写法在 python 中是这样的
    t = """
    <div class="todo-cell">
        <button class="todo-delete">删除</button>
        <span>{}</span>
    </div>
    """.format(todo)
    */
}

let insertTodo = function(todo) {
    let todoCell = todoTemplate(todo)
    // 插入 todo-list
    let todoList = e('.todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

let insertEditForm = function(cell) {
    let form = `
        <div class='todo-edit-form'>
            <input class="todo-edit-input">
            <button class='todo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('beforeend', form)
}

let loadTodos = function() {
    // 调用 ajax api 来载入数据
    apiTodoAll(function(r) {
        // console.log('load all', r)
        // 解析为 数组
        let todos = JSON.parse(r)
        // 循环添加到页面中
        for(let i = 0; i < todos.length; i++) {
            let todo = todos[i]
            insertTodo(todo)
        }
    })
}

let bindEventTodoAdd = function() {
    let b = e('#id-button-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        let input = e('#id-input-todo')
        let title = input.value
        log('click add', title)
        let form = {
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
        let self = event.target
        if(self.classList.contains('todo-delete')){
            // 删除这个 todo
            let todoCell = self.parentElement
            let todo_id = todoCell.dataset.id
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
            //
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
//                todoCell.remove()
            })
        }
    })
}

let bindEvents = function() {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
}

let __main = function() {
    bindEvents()
    loadTodos()
}

__main()


/*
给 删除 按钮绑定删除的事件
1, 绑定事件
2, 删除整个 todo-cell 元素
*/
// let todoList = e('.todo-list')
// // 事件响应函数会被传入一个参数, 就是事件本身
// todoList.addEventListener('click', function(event){
//     // log('click todolist', event)
//     // 我们可以通过 event.target 来得到被点击的元素
//     let self = event.target
//     // log('被点击的元素是', self)
//     // 通过比较被点击元素的 class 来判断元素是否是我们想要的
//     // classList 属性保存了元素的所有 class
//     // 在 HTML 中, 一个元素可以有多个 class, 用空格分开
//     // log(self.classList)
//     // 判断是否拥有某个 class 的方法如下
//     if (self.classList.contains('todo-delete')) {
//         log('点到了 删除按钮')
//         // 删除 self 的父节点
//         // parentElement 可以访问到元素的父节点
//         self.parentElement.remove()
//     } else {
//         // log('点击的不是删除按钮******')
//     }
// })
