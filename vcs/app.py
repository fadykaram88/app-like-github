import os
from flask import Flask, render_template, request, redirect, url_for
from vcs import VersionControlSystem

app = Flask(__name__)

# إعداد المستودع
vcs_system = VersionControlSystem('my_repo')
vcs_system.init_repo()

@app.route('/')
def index():
    # عرض الملفات التي تم إضافتها في النظام
    files = [f for f in os.listdir(vcs_system.objects_path)]
    return render_template('index.html', files=files)

@app.route('/add', methods=['GET', 'POST'])
def add_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(vcs_system.repo_path, file.filename)
            file.save(file_path)
            vcs_system.add(file_path)  # إضافة الملف إلى VCS
            vcs_system.commit(f"Added {file.filename}")  # إجراء commit للملف
            return redirect(url_for('index'))
    return render_template('add_file.html')

@app.route('/view/<file_name>')
def view_file(file_name):
    file_path = os.path.join(vcs_system.objects_path, file_name)
    with open(file_path, 'r') as file:
        content = file.read()
    return render_template('view_file.html', file_name=file_name, content=content)

if __name__ == '__main__':
    app.run(debug=True, port=5950)

