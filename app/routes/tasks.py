from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.models.task import Task

# 建立 tasks blueprint 模組，用於任務管理的主要路由邏輯
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'])
def index():
    """
    顯示工作清單主頁。
    - 從 request.args 擷取 'status' 參數作為篩選條件 (例如 pending / completed)
    - 呼叫 Task.get_all(status_filter) 獲取符合條件的任務列表
    - 渲染 templates/index.html，將任務資料夾帶給視圖
    """
    status_filter = request.args.get('status')
    tasks = Task.get_all(status_filter=status_filter)
    return render_template('index.html', tasks=tasks, current_status=status_filter)

@tasks_bp.route('/calendar', methods=['GET'])
def calendar():
    """
    顯示行事曆視圖。
    - 呼叫 Task.get_all() 取得所有任務以分布在月曆中
    - 渲染 templates/calendar.html
    """
    tasks = Task.get_all()
    return render_template('calendar.html', tasks=tasks)

@tasks_bp.route('/add', methods=['POST'])
def add_task():
    """
    新增任務。
    - 接收表單欄位 request.form 中的 'title' 以及 'due_date'
    - 若 'title' 為空則中止並回傳錯誤提示 (400) 或導向
    - 呼叫 Task.create() 儲存資料庫
    - 重導向至 index (首頁)
    """
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '').strip() or None
    
    if not title:
        flash('任務標題不能為空！', 'error')
        return redirect(url_for('tasks.index'))
        
    Task.create(title=title, due_date=due_date)
    flash('任務已成功新增。', 'success')
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    """
    更新任務內容。
    - 根據傳入的 task_id，確認任務是否存在 (不存在則 abort(404))
    - 從表單取得新的 'title' 以及 'due_date'
    - 呼叫 Task.update() 更新至資料庫
    - 重導向至 index (首頁)
    """
    task = Task.get_by_id(task_id)
    if not task:
        abort(404)
        
    title = request.form.get('title', '').strip()
    due_date = request.form.get('due_date', '').strip() or None
    
    if not title:
        flash('任務標題不能為空！', 'error')
        return redirect(url_for('tasks.index'))
        
    success = Task.update(task_id, title=title, due_date=due_date)
    if success:
        flash('任務已成功更新。', 'success')
    else:
        flash('任務更新失敗。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    """
    切換任務完成 / 未完成狀態。
    - 根據 task_id 尋找任務 (不存在則 abort(404))
    - 呼叫 Task.toggle_status() 改變資料庫內的 is_completed 標記
    - 重導向至 index (首頁)
    """
    task = Task.get_by_id(task_id)
    if not task:
        abort(404)
        
    success = Task.toggle_status(task_id)
    if success:
        flash('任務狀態已切換。', 'success')
    else:
        flash('切換狀態失敗。', 'error')
        
    return redirect(url_for('tasks.index'))

@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    刪除指定任務。
    - 根據 task_id 尋找該任務 (不存在則 abort(404))
    - 呼叫 Task.delete() 清除記錄
    - 重導向至 index (首頁)
    """
    task = Task.get_by_id(task_id)
    if not task:
        abort(404)
        
    success = Task.delete(task_id)
    if success:
        flash('任務已成功刪除。', 'success')
    else:
        flash('刪除失敗。', 'error')
        
    return redirect(url_for('tasks.index'))
