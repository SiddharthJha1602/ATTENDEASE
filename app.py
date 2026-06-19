from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from datetime import datetime, date
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'attendease_secret_2024'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    db = sqlite3.connect('database.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            department TEXT
        );

        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            check_in TEXT,
            status TEXT DEFAULT 'Present',
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            leave_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            reason TEXT NOT NULL,
            document_path TEXT,
            status TEXT DEFAULT 'Pending',
            applied_date TEXT NOT NULL,
            reviewed_by INTEGER,
            reviewed_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Insert predefined users
    try:
        db.execute("INSERT INTO users (username, password, role, full_name, email, department) VALUES (?, ?, ?, ?, ?, ?)",
                   ('admin', 'admin123', 'admin', 'Admin User', 'admin@attendease.com', 'HR'))
        db.execute("INSERT INTO users (username, password, role, full_name, email, department) VALUES (?, ?, ?, ?, ?, ?)",
                   ('employee', 'employee123', 'employee', 'John Doe', 'john.doe@attendease.com', 'Engineering'))
        db.execute("INSERT INTO users (username, password, role, full_name, email, department) VALUES (?, ?, ?, ?, ?, ?)",
                   ('sarah', 'sarah123', 'employee', 'Sarah Smith', 'sarah@attendease.com', 'Marketing'))
        db.execute("INSERT INTO users (username, password, role, full_name, email, department) VALUES (?, ?, ?, ?, ?, ?)",
                   ('mike', 'mike123', 'employee', 'Mike Johnson', 'mike@attendease.com', 'Sales'))
    except:
        pass

    # Sample attendance data
    from datetime import timedelta
    today = date.today()
    emp_id = db.execute("SELECT id FROM users WHERE username='employee'").fetchone()
    if emp_id:
        emp_id = emp_id['id']
        for i in range(20, 0, -1):
            d = today - timedelta(days=i)
            if d.weekday() < 5:
                try:
                    db.execute("INSERT INTO attendance (user_id, date, check_in, status) VALUES (?,?,?,?)",
                               (emp_id, d.isoformat(), '09:00', 'Present'))
                except:
                    pass

    # Sample leave requests
    sarah_id = db.execute("SELECT id FROM users WHERE username='sarah'").fetchone()
    mike_id = db.execute("SELECT id FROM users WHERE username='mike'").fetchone()
    emp2_id = db.execute("SELECT id FROM users WHERE username='employee'").fetchone()

    if sarah_id and mike_id and emp2_id:
        try:
            db.execute("INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, reason, status, applied_date) VALUES (?,?,?,?,?,?,?)",
                       (sarah_id['id'], 'Casual Leave', '2024-06-15', '2024-06-17', 'Family function', 'Approved', '2024-06-10'))
            db.execute("INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, reason, status, applied_date) VALUES (?,?,?,?,?,?,?)",
                       (mike_id['id'], 'Sick Leave', '2024-06-18', '2024-06-19', 'Fever and cold', 'Pending', '2024-06-17'))
            db.execute("INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, reason, status, applied_date) VALUES (?,?,?,?,?,?,?)",
                       (emp2_id['id'], 'Emergency Leave', '2024-06-20', '2024-06-20', 'Personal emergency', 'Rejected', '2024-06-19'))
        except:
            pass

    db.commit()
    db.close()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Access denied.', 'danger')
            return redirect(url_for('employee_dashboard'))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('employee_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()
        db.close()
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            session['department'] = user['department']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('employee_dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))

# ─── EMPLOYEE ROUTES ───────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def employee_dashboard():
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    db = get_db()
    user_id = session['user_id']
    today = date.today()
    month_start = today.replace(day=1).isoformat()

    attendance_this_month = db.execute(
        "SELECT COUNT(*) as cnt FROM attendance WHERE user_id=? AND date>=? AND date<=?",
        (user_id, month_start, today.isoformat())
    ).fetchone()['cnt']

    leaves_applied = db.execute(
        "SELECT COUNT(*) as cnt FROM leave_requests WHERE user_id=?", (user_id,)
    ).fetchone()['cnt']

    pending_leaves = db.execute(
        "SELECT COUNT(*) as cnt FROM leave_requests WHERE user_id=? AND status='Pending'", (user_id,)
    ).fetchone()['cnt']

    approved_leaves = db.execute(
        "SELECT COUNT(*) as cnt FROM leave_requests WHERE user_id=? AND status='Approved'", (user_id,)
    ).fetchone()['cnt']

    today_att = db.execute(
        "SELECT * FROM attendance WHERE user_id=? AND date=?", (user_id, today.isoformat())
    ).fetchone()

    recent_attendance = db.execute(
        "SELECT * FROM attendance WHERE user_id=? ORDER BY date DESC LIMIT 5", (user_id,)
    ).fetchall()

    recent_leaves = db.execute(
        "SELECT * FROM leave_requests WHERE user_id=? ORDER BY applied_date DESC LIMIT 5", (user_id,)
    ).fetchall()

    # Monthly attendance chart data
    monthly_data = []
    for i in range(1, today.day + 1):
        d = today.replace(day=i)
        row = db.execute("SELECT * FROM attendance WHERE user_id=? AND date=?",
                         (user_id, d.isoformat())).fetchone()
        monthly_data.append({'day': i, 'present': 1 if row else 0})

    leave_stats = db.execute(
        "SELECT leave_type, COUNT(*) as cnt FROM leave_requests WHERE user_id=? GROUP BY leave_type",
        (user_id,)
    ).fetchall()

    db.close()
    return render_template('employee/dashboard.html',
        attendance_this_month=attendance_this_month,
        leaves_applied=leaves_applied,
        pending_leaves=pending_leaves,
        approved_leaves=approved_leaves,
        today_att=today_att,
        recent_attendance=recent_attendance,
        recent_leaves=recent_leaves,
        monthly_data=monthly_data,
        leave_stats=leave_stats,
        today=today
    )

@app.route('/attendance', methods=['GET', 'POST'])
@login_required
def attendance():
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    user_id = session['user_id']
    today = date.today()
    db = get_db()

    if request.method == 'POST':
        existing = db.execute("SELECT * FROM attendance WHERE user_id=? AND date=?",
                              (user_id, today.isoformat())).fetchone()
        if existing:
            flash('Attendance already marked for today.', 'warning')
        else:
            now = datetime.now().strftime('%H:%M')
            db.execute("INSERT INTO attendance (user_id, date, check_in, status) VALUES (?,?,?,?)",
                       (user_id, today.isoformat(), now, 'Present'))
            db.commit()
            flash('Attendance marked successfully!', 'success')
        db.close()
        return redirect(url_for('attendance'))

    today_att = db.execute("SELECT * FROM attendance WHERE user_id=? AND date=?",
                           (user_id, today.isoformat())).fetchone()
    history = db.execute("SELECT * FROM attendance WHERE user_id=? ORDER BY date DESC LIMIT 30",
                         (user_id,)).fetchall()
    db.close()
    return render_template('employee/attendance.html', today_att=today_att, history=history, today=today)

@app.route('/apply-leave', methods=['GET', 'POST'])
@login_required
def apply_leave():
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        leave_type = request.form.get('leave_type')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason', '').strip()
        doc_path = None

        if not all([leave_type, start_date, end_date, reason]):
            flash('All fields are required.', 'danger')
            return redirect(url_for('apply_leave'))
        if start_date > end_date:
            flash('End date cannot be before start date.', 'danger')
            return redirect(url_for('apply_leave'))
        if len(reason) < 10:
            flash('Reason must be at least 10 characters.', 'danger')
            return redirect(url_for('apply_leave'))

        if 'document' in request.files:
            file = request.files['document']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                doc_path = filename

        db = get_db()
        db.execute(
            "INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, reason, document_path, applied_date) VALUES (?,?,?,?,?,?,?)",
            (session['user_id'], leave_type, start_date, end_date, reason, doc_path, date.today().isoformat())
        )
        db.commit()
        db.close()
        flash('Leave request submitted successfully!', 'success')
        return redirect(url_for('leave_status'))
    return render_template('employee/apply_leave.html')

@app.route('/leave-status')
@login_required
def leave_status():
    if session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    db = get_db()
    leaves = db.execute(
        "SELECT * FROM leave_requests WHERE user_id=? ORDER BY applied_date DESC",
        (session['user_id'],)
    ).fetchall()
    db.close()
    return render_template('employee/leave_status.html', leaves=leaves)

# ─── ADMIN ROUTES ──────────────────────────────────────────────────────────────

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    db = get_db()
    today = date.today().isoformat()

    total_employees = db.execute("SELECT COUNT(*) as cnt FROM users WHERE role='employee'").fetchone()['cnt']
    attendance_today = db.execute("SELECT COUNT(*) as cnt FROM attendance WHERE date=?", (today,)).fetchone()['cnt']
    pending_requests = db.execute("SELECT COUNT(*) as cnt FROM leave_requests WHERE status='Pending'").fetchone()['cnt']
    approved_requests = db.execute("SELECT COUNT(*) as cnt FROM leave_requests WHERE status='Approved'").fetchone()['cnt']

    recent_attendance = db.execute(
        "SELECT a.*, u.full_name, u.department FROM attendance a JOIN users u ON a.user_id=u.id ORDER BY a.date DESC LIMIT 8"
    ).fetchall()
    recent_leaves = db.execute(
        "SELECT lr.*, u.full_name FROM leave_requests lr JOIN users u ON lr.user_id=u.id ORDER BY lr.applied_date DESC LIMIT 5"
    ).fetchall()

    leave_dist = db.execute(
        "SELECT leave_type, COUNT(*) as cnt FROM leave_requests GROUP BY leave_type"
    ).fetchall()

    db.close()
    return render_template('admin/dashboard.html',
        total_employees=total_employees,
        attendance_today=attendance_today,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        recent_attendance=recent_attendance,
        recent_leaves=recent_leaves,
        leave_dist=leave_dist,
        today=today
    )

@app.route('/admin/attendance')
@admin_required
def admin_attendance():
    db = get_db()
    search = request.args.get('search', '')
    date_filter = request.args.get('date', '')
    query = "SELECT a.*, u.full_name, u.department FROM attendance a JOIN users u ON a.user_id=u.id WHERE 1=1"
    params = []
    if search:
        query += " AND u.full_name LIKE ?"
        params.append(f'%{search}%')
    if date_filter:
        query += " AND a.date=?"
        params.append(date_filter)
    query += " ORDER BY a.date DESC"
    records = db.execute(query, params).fetchall()
    db.close()
    return render_template('admin/attendance.html', records=records, search=search, date_filter=date_filter)

@app.route('/admin/leaves')
@admin_required
def admin_leaves():
    db = get_db()
    leaves = db.execute(
        "SELECT lr.*, u.full_name, u.department FROM leave_requests lr JOIN users u ON lr.user_id=u.id ORDER BY lr.applied_date DESC"
    ).fetchall()
    db.close()
    return render_template('admin/leaves.html', leaves=leaves)

@app.route('/admin/leave/action/<int:leave_id>/<action>')
@admin_required
def leave_action(leave_id, action):
    if action not in ['approve', 'reject']:
        flash('Invalid action.', 'danger')
        return redirect(url_for('admin_leaves'))
    status = 'Approved' if action == 'approve' else 'Rejected'
    db = get_db()
    db.execute("UPDATE leave_requests SET status=?, reviewed_by=?, reviewed_date=? WHERE id=?",
               (status, session['user_id'], date.today().isoformat(), leave_id))
    db.commit()
    db.close()
    flash(f'Leave request {status.lower()} successfully.', 'success')
    return redirect(url_for('admin_leaves'))

@app.route('/admin/attendance/export')
@admin_required
def export_attendance():
    db = get_db()
    records = db.execute(
        "SELECT u.full_name, u.department, a.date, a.check_in, a.status FROM attendance a JOIN users u ON a.user_id=u.id ORDER BY a.date DESC"
    ).fetchall()
    db.close()
    csv_data = "Name,Department,Date,Check-In,Status\n"
    for r in records:
        csv_data += f"{r['full_name']},{r['department']},{r['date']},{r['check_in']},{r['status']}\n"
    from flask import Response
    return Response(csv_data, mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=attendance_report.csv'})

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    init_db()
    app.run(debug=True, port=5000)
