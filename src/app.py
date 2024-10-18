from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import os
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

USERS_CSV = 'users.csv'
ADMISSION_CSV = 'admission_requests.csv'
ITEMS_CSV = 'items.csv'
MESSAGES_CSV = 'messages.csv'
ITEMS_FOLDER = os.path.join('static', 'items')
USER_ACADEMIC_FOLDER = os.path.join('static', 'user_academic')

if not os.path.exists(ITEMS_FOLDER):
    os.makedirs(ITEMS_FOLDER)
if not os.path.exists(USER_ACADEMIC_FOLDER):
    os.makedirs(USER_ACADEMIC_FOLDER)

# CSV 파일 초기화
def init_csv():
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'student_id', 'user_id', 'user_pw', 'user_email'])

    if not os.path.exists(ADMISSION_CSV):
        with open(ADMISSION_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['name', 'student_id', 'user_id', 'user_pw', 'user_email'])

    if not os.path.exists(ITEMS_CSV):
        with open(ITEMS_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['item_id', 'user_id', 'item_name', 'item_price', 'item_description', 'item_photo'])

    if not os.path.exists(MESSAGES_CSV):
        with open(MESSAGES_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['message_id', 'to_user', 'from_user', 'message'])

init_csv()

def get_user_items_csv(user_id):
    return f'user_items_{user_id}.csv'

@app.route('/') #메인화면
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST']) #로그인 화면
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        if user_id == 'admin' and password == 'aicarrot':
            session['user_id'] = user_id
            return redirect(url_for('admin'))

        with open(USERS_CSV, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id and row['user_pw'] == password:
                    session['user_id'] = user_id
                    session['name'] = row['name']
                    flash('로그인 되었습니다.', 'success')
                    return redirect(url_for('main'))
            flash('아이디 또는 비밀번호가 잘못되었습니다.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST']) #회원가입 화면
def register():
    if request.method == 'POST':
        name = request.form['name']
        student_id = request.form['student_id']
        user_id = request.form['user_id']
        password = request.form['password']
        email = request.form['email']
        academic_info = request.files['academic_info']

        with open(USERS_CSV, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id:
                    flash('이미 가입된 회원입니다.', 'error')
                    return redirect(url_for('login'))

        with open(ADMISSION_CSV, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id:
                    flash('이미 회원가입 요청이 접수되었습니다.', 'error')
                    return redirect(url_for('login'))

        academic_info_filename = f"{student_id}.jpg"
        academic_info_path = os.path.join(USER_ACADEMIC_FOLDER, academic_info_filename)
        academic_info.save(academic_info_path)

        with open(ADMISSION_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, student_id, user_id, password, email])

        flash('회원가입 요청이 접수되었습니다. 관리자의 승인을 기다려주세요.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/main') #메인, 판매 페이지
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    items = []
    users = {}
    with open(USERS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row['user_id']] = row['name']

    with open(ITEMS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['seller_name'] = users.get(row['user_id'], 'Unknown')
            items.append(row)

    return render_template('main.html', name=session['name'], items=items)

@app.route('/item/<item_id>', methods=['GET', 'POST']) #개별 물품들의 판매 페이지, 세부사항
def item_detail(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    item = None
    seller_name = None
    with open(ITEMS_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['item_id'] == item_id:
                item = row
                break

    if item:
        with open(USERS_CSV, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == item['user_id']:
                    seller_name = row['name']
                    break

    if request.method == 'POST':
        message = request.form['message']
        to_user = item['user_id']
        from_user = session['user_id']

        with open(MESSAGES_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([str(uuid.uuid4()), to_user, from_user, message])

        flash('쪽지가 전송되었습니다.', 'success')
        return redirect(url_for('item_detail', item_id=item_id))

    return render_template('item_detail.html', item=item, seller_name=seller_name)

@app.route('/sell', methods=['GET', 'POST']) #물품 등록 페이지
def sell():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        item_name = request.form['item_name']
        item_price = request.form['item_price']
        item_description = request.form['item_description']
        item_photo = request.files['item_photo']

        if item_photo and item_photo.filename != '':
            item_id = f"{item_name}_{session['user_id']}"  # 물품 이름과 사용자 ID를 결합하여 아이템 ID 생성
            photo_filename = f"{item_id}_{item_photo.filename}"
            photo_path = os.path.join(ITEMS_FOLDER, photo_filename)
            item_photo.save(photo_path)

            item_data = [item_id, session['user_id'], item_name, item_price, item_description, photo_filename]

            user_items_csv = get_user_items_csv(session['user_id'])
            if not os.path.exists(user_items_csv):
                with open(user_items_csv, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['item_id', 'user_id', 'item_name', 'item_price', 'item_description', 'item_photo'])

            with open(user_items_csv, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(item_data)

            with open(ITEMS_CSV, 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(item_data)

            flash('물품이 성공적으로 등록되었습니다.', 'success')
            return redirect(url_for('main'))
        else:
            flash('물품 사진을 등록해주세요.', 'error')

    return render_template('sell.html', name=session.get('name'))


@app.route('/mypage') #마이페이지, 물품 삭제, 쪽지확인
def mypage():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_items_csv = get_user_items_csv(session['user_id'])
    items = []
    messages = []
    if os.path.exists(user_items_csv):
        with open(user_items_csv, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                items.append(row)

    with open(MESSAGES_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['to_user'] == session['user_id']:
                messages.append(row)

    return render_template('mypage.html', name=session['name'], items=items, messages=messages)

@app.route('/delete_item/<item_id>')
def delete_item(item_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_items_csv = get_user_items_csv(session['user_id'])
    items = []
    with open(user_items_csv, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['item_id'] != item_id:
                items.append(row)
            else:
                if row['user_id'] == session['user_id']:
                    os.remove(os.path.join(ITEMS_FOLDER, row['item_photo']))

    with open(user_items_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['item_id', 'user_id', 'item_name', 'item_price', 'item_description', 'item_photo'])
        writer.writeheader()
        writer.writerows(items)

    with open(ITEMS_CSV, 'r', encoding='utf-8') as file:
        items = [row for row in csv.DictReader(file) if row['item_id'] != item_id]

    with open(ITEMS_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['item_id', 'user_id', 'item_name', 'item_price', 'item_description', 'item_photo'])
        writer.writeheader()
        writer.writerows(items)

    flash('물품이 삭제되었습니다.', 'success')
    return redirect(url_for('mypage'))

@app.route('/admin') #관리자 페이지
def admin():
    if 'user_id' not in session or session['user_id'] != 'admin':
        return redirect(url_for('login'))

    with open(ADMISSION_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        requests = [row for row in reader]

    return render_template('admin.html', requests=requests, user_academic_folder=USER_ACADEMIC_FOLDER)

@app.route('/approve/<user_id>') #회원가입 승인
def approve(user_id):
    if 'user_id' not in session or session['user_id'] != 'admin':
        return redirect(url_for('login'))

    requests = []
    approved_request = None
    with open(ADMISSION_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] == user_id:
                approved_request = row
            else:
                requests.append(row)

    if approved_request:
        with open(USERS_CSV, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'student_id', 'user_id', 'user_pw', 'user_email'])
            writer.writerow({'name': approved_request['name'], 'student_id': approved_request['student_id'], 'user_id': approved_request['user_id'], 'user_pw': approved_request['user_pw'], 'user_email': approved_request['user_email']})

        with open(ADMISSION_CSV, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'student_id', 'user_id', 'user_pw', 'user_email'])
            writer.writeheader()
            writer.writerows(requests)

        flash(f"{approved_request['user_id']}님의 회원가입 요청이 승인되었습니다.", 'success')
    return redirect(url_for('admin'))

@app.route('/send_message/<to_user>', methods=['POST']) #메시지 보내기
def send_message(to_user):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    from_user = session['user_id']
    message_content = request.form['message']

    with open(MESSAGES_CSV, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([str(uuid.uuid4()), to_user, from_user, message_content])

    flash('쪽지가 전송되었습니다.', 'success')
    return redirect(url_for('mypage'))


@app.route('/reject/<user_id>')
def reject(user_id):
    if 'user_id' not in session or session['user_id'] != 'admin':
        return redirect(url_for('login'))

    requests = []
    with open(ADMISSION_CSV, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['user_id'] != user_id:
                requests.append(row)

    with open(ADMISSION_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['name', 'student_id', 'user_id', 'user_pw', 'user_email'])
        writer.writeheader()
        writer.writerows(requests)

    flash('회원가입 요청이 거절되었습니다.', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
