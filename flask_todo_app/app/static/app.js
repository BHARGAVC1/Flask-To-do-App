document.addEventListener('DOMContentLoaded', () => {
    const todoForm = document.getElementById('todo-form');
    const todoInput = document.getElementById('todo-input');
    const todoList = document.getElementById('todo-list');
    const filterBtns = document.querySelectorAll('.filter-btn');
    const clearCompletedBtn = document.getElementById('clear-completed-btn');

    let currentFilter = 'all';

    // Fetch initial tasks
    fetchTasks();

    // Filters
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            applyFilter();
        });
    });

    // Add new task
    todoForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = todoInput.value.trim();
        if (!text) return;

        try {
            const res = await fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const newTask = await res.json();
            
            // Sync local storage
            const localTasks = JSON.parse(localStorage.getItem('tasks') || '[]');
            localTasks.push(newTask);
            localStorage.setItem('tasks', JSON.stringify(localTasks));

            renderTask(newTask);
            applyFilter();
            todoInput.value = '';
        } catch (error) {
            console.error('Error adding task:', error);
        }
    });

    // Clear completed
    clearCompletedBtn.addEventListener('click', async () => {
        if (!confirm('Are you sure you want to delete all completed tasks?')) return;
        try {
            await fetch('/api/tasks/clear_completed', { method: 'POST' });
            // Sync local storage
            let localTasks = JSON.parse(localStorage.getItem('tasks') || '[]');
            localTasks = localTasks.filter(t => !t.completed);
            localStorage.setItem('tasks', JSON.stringify(localTasks));

            // update UI
            const completedItems = todoList.querySelectorAll('.task-item.completed');
            completedItems.forEach(item => {
                item.classList.add('removing');
                setTimeout(() => item.remove(), 300);
            });
        } catch (error) {
            console.error('Error clearing completed tasks:', error);
        }
    });

    async function fetchTasks() {
        try {
            const res = await fetch('/api/tasks');
            const tasks = await res.json();
            
            // Sync state to local storage to act as local cache/fallback
            localStorage.setItem('tasks', JSON.stringify(tasks));

            todoList.innerHTML = ''; // clear before rendering
            tasks.forEach(renderTask);
        } catch (error) {
            console.error('Error fetching tasks from server, falling back to local storage:', error);
            const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
            todoList.innerHTML = '';
            tasks.forEach(renderTask);
        }
    }

    function applyFilter() {
        const items = todoList.querySelectorAll('.task-item');
        items.forEach(item => {
            const isCompleted = item.classList.contains('completed');
            if (currentFilter === 'all') {
                item.classList.remove('hidden');
            } else if (currentFilter === 'pending') {
                isCompleted ? item.classList.add('hidden') : item.classList.remove('hidden');
            } else if (currentFilter === 'completed') {
                isCompleted ? item.classList.remove('hidden') : item.classList.add('hidden');
            }
        });
    }

    function renderTask(task) {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''}`;
        li.dataset.id = task.id;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'task-content';
        
        const checkbox = document.createElement('div');
        checkbox.className = 'checkbox';
        
        const textSpan = document.createElement('span');
        textSpan.className = 'task-text';
        textSpan.textContent = task.text;

        contentDiv.appendChild(checkbox);
        contentDiv.appendChild(textSpan);

        // Complete and delete immediately
        contentDiv.addEventListener('click', async () => {
            try {
                li.classList.add('completed');
                
                // Set short delay to let checkmark animation show
                setTimeout(async () => {
                    li.classList.add('removing');
                    try {
                        await fetch(`/api/tasks/${task.id}`, { method: 'DELETE' });
                        
                        // Sync local storage
                        let localTasks = JSON.parse(localStorage.getItem('tasks') || '[]');
                        localTasks = localTasks.filter(t => t.id != task.id);
                        localStorage.setItem('tasks', JSON.stringify(localTasks));

                        setTimeout(() => {
                            li.remove();
                            applyFilter();
                        }, 300); // Wait for slideOut animation
                    } catch (error) {
                        console.error('Error deleting task:', error);
                        li.classList.remove('removing');
                    }
                }, 400); // 400ms delay to admire the checkmark
            } catch (error) {
                console.error('Error marking task complete:', error);
            }
        });

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = '×';
        deleteBtn.title = 'Delete Task';

        // Delete task
        deleteBtn.addEventListener('click', async (e) => {
            e.stopPropagation();
            if (!confirm('Are you sure you want to delete this task?')) return;
            
            li.classList.add('removing');
            try {
                await fetch(`/api/tasks/${task.id}`, { method: 'DELETE' });
                
                // Sync local storage
                let localTasks = JSON.parse(localStorage.getItem('tasks') || '[]');
                localTasks = localTasks.filter(t => t.id != task.id);
                localStorage.setItem('tasks', JSON.stringify(localTasks));

                setTimeout(() => li.remove(), 300); // Wait for animation
            } catch (error) {
                console.error('Error deleting task:', error);
                li.classList.remove('removing');
            }
        });

        li.appendChild(contentDiv);
        li.appendChild(deleteBtn);
        todoList.appendChild(li);
        applyFilter();
    }
});
