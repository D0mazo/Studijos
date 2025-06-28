// Task Management Dashboard
class TaskManager {
    constructor() {
        this.tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        this.currentFilter = 'all';
        this.taskList = document.getElementById('taskList');
        this.taskInput = document.getElementById('taskInput');
        this.init();
    }

    // Initialize the app
    init() {
        this.renderTasks();
        this.setupEventListeners();
    }

    // Add a new task
    addTask() {
        const taskText = this.taskInput.value.trim();
        if (!taskText) return;

        const task = {
            id: Date.now(),
            text: taskText,
            completed: false
        };

        this.tasks.push(task);
        this.saveTasks();
        this.renderTasks();
        this.taskInput.value = '';
    }

    // Edit an existing task
    editTask(id) {
        const newText = prompt('Edit task:', this.tasks.find(task => task.id === id).text);
        if (newText?.trim()) {
            this.tasks = this.tasks.map(task =>
                task.id === id ? { ...task, text: newText.trim() } : task
            );
            this.saveTasks();
            this.renderTasks();
        }
    }

    // Delete a task
    deleteTask(id) {
        this.tasks = this.tasks.filter(task => task.id !== id);
        this.saveTasks();
        this.renderTasks();
    }

    // Toggle task completion
    toggleTask(id) {
        this.tasks = this.tasks.map(task =>
            task.id === id ? { ...task, completed: !task.completed } : task
        );
        this.saveTasks();
        this.renderTasks();
    }

    // Filter tasks
    filterTasks(filter) {
        this.currentFilter = filter;
        this.updateFilterButtons();
        this.renderTasks();
    }

    // Save tasks to localStorage
    saveTasks() {
        localStorage.setItem('tasks', JSON.stringify(this.tasks));
    }

    // Render tasks based on current filter
    renderTasks() {
        this.taskList.innerHTML = '';
        const filteredTasks = this.tasks.filter(task => {
            if (this.currentFilter === 'active') return !task.completed;
            if (this.currentFilter === 'completed') return task.completed;
            return true; // 'all'
        });

        filteredTasks.forEach(task => {
            const li = document.createElement('li');
            li.className = `task-item ${task.completed ? 'completed' : ''}`;
            li.innerHTML = `
                <span onclick="taskManager.toggleTask(${task.id})">${task.text}</span>
                <div>
                    <button class="edit" onclick="taskManager.editTask(${task.id})">Edit</button>
                    <button onclick="taskManager.deleteTask(${task.id})">Delete</button>
                </div>
            `;
            this.taskList.appendChild(li);
        });
    }

    // Update filter button styles
    updateFilterButtons() {
        document.querySelectorAll('.filter-buttons button').forEach(btn => {
            btn.classList.toggle('active', btn.textContent.toLowerCase() === this.currentFilter);
        });
    }

    // Setup event listeners
    setupEventListeners() {
        this.taskInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addTask();
        });
    }
}

// Global functions for HTML button events
const taskManager = new TaskManager();
window.addTask = () => taskManager.addTask();
window.filterTasks = (filter) => taskManager.filterTasks(filter);