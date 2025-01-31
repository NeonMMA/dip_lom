# from io import StringIO

# from flask import Flask, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
# from flask_cors import CORS, cross_origin
# import csv

# from sqlalchemy import MetaData, Table, insert
# from sqlalchemy.orm import joinedload
# from werkzeug.security import generate_password_hash, check_password_hash
# from dateutil import parser as date_parser  # для автоматического распознавания форматов дат
# from datetime import datetime, timedelta
# from sqlalchemy import extract, func, and_, or_


# app = Flask(__name__)

# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@localhost/newdb"
# app.config['JWT_SECRET_KEY'] = 'your_secret_key'

# db = SQLAlchemy(app)

# jwt = JWTManager(app)




# class Teachers(db.Model):
#     __tablename__ = 'teachers'

#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String, nullable=False)
#     last_name = db.Column(db.String, nullable=False)
#     patronymic = db.Column(db.String, nullable=True)
#     login = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     role = db.Column(db.String, nullable=False)
#     access_token = db.Column(db.String, nullable=True)
#     refresh_token = db.Column(db.String, nullable=True)

#     days_off = db.relationship('DaysOff', backref='teacher', lazy=True)
#     disc_teachers = db.relationship('DiscTeachers', backref='teacher', lazy=True)
#     schedule = db.relationship('Schedule', backref='teacher', lazy=True)
#     duty = db.relationship('Duty', backref='teacher', lazy=True)
#     sent_notifications = db.relationship('Notifications', foreign_keys='Notifications.sender', backref='sender_teacher',
#                                          lazy=True)
#     received_notifications = db.relationship('Notifications', foreign_keys='Notifications.recipient',
#                                              backref='recipient_teacher', lazy=True)


# class DaysOff(db.Model):
#     __tablename__ = 'daysOff'

#     id = db.Column(db.Integer, primary_key=True)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)


# class DiscTeachers(db.Model):
#     __tablename__ = 'disc/teachers'

#     id = db.Column(db.Integer, primary_key=True)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
#     disc_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)


# class Discipline(db.Model):
#     __tablename__ = 'discipline'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)

#     disc_teachers = db.relationship('DiscTeachers', backref='discipline', lazy=True)


# class Schedule(db.Model):
#     __tablename__ = 'schedule'

#     id = db.Column(db.Integer, primary_key=True)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
#     disc_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
#     pair_id = db.Column(db.Integer, db.ForeignKey('pairs.id'), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     auditorium = db.Column(db.String, nullable=False)
#     group = db.Column(db.String, nullable=False)


# class Pairs(db.Model):
#     __tablename__ = 'pairs'

#     id = db.Column(db.Integer, primary_key=True)
#     pair_number = db.Column(db.Integer, nullable=False)
#     pair_start_time = db.Column(db.Time, nullable=False)
#     pair_end_time = db.Column(db.Time, nullable=False)
#     faculty = db.Column(db.String, nullable=False)

#     schedule = db.relationship('Schedule', backref='pair_info', lazy=True)


# class Duty(db.Model):
#     __tablename__ = 'duty'

#     id = db.Column(db.Integer, primary_key=True)
#     teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
#     corpus_id = db.Column(db.Integer, db.ForeignKey('corpus.id'), nullable=False)
#     intercession_date = db.Column(db.Date, nullable=False)


# class Corpus(db.Model):
#     __tablename__ = 'corpus'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     duty_start_time = db.Column(db.Time, nullable=False)
#     duty_end_time = db.Column(db.Time, nullable=False)

#     duties = db.relationship('Duty', backref='corpus', lazy=True)


# class Notifications(db.Model):
#     __tablename__ = 'notifications'

#     id = db.Column(db.Integer, primary_key=True)
#     sender = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
#     recipient = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
#     request_time = db.Column(db.DateTime, nullable=False)
#     response_time = db.Column(db.DateTime, nullable=True)
#     confirmed = db.Column(db.Boolean, nullable=True, default=None)
#     duty_id = db.Column(db.Integer, db.ForeignKey('duty.id'), nullable=False)

#     duty = db.relationship('Duty', backref=db.backref('notifications', lazy=True))


# with app.app_context():
#     db.create_all()


# @app.route('/get_schedule', methods=['POST'])
# def get_schedule():
#     data = request.get_json()

#     start_date = datetime.fromisoformat(data['start_date']).date()
#     end_date = datetime.fromisoformat(data['end_date']).date()

#     # Извлекаем accessToken из заголовков запроса
#     access_token = data['accessToken']

#     # Проверяем, существует ли преподаватель с таким access_token
#     try:
#         teacher = Teachers.query.filter_by(access_token=access_token).one()
#     except:
#         return jsonify({"error": "Invalid access token"}), 401

#     # Определим дни недели для удобства
#     days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

#     # def get_week_start(date):
#     #     return date - timedelta(days=date.weekday())  # Возвращает дату понедельника для любой даты

#     # Создадим словарь для хранения расписания по неделям
#     weeks = []

#     # Получение всех занятий и дежурств в диапазоне дат для конкретного преподавателя
#     schedule_records = Schedule.query.filter(Schedule.teacher_id == teacher.id,
#                                              Schedule.date >= start_date,
#                                              Schedule.date <= end_date).all()

#     duty_records = Duty.query.filter(Duty.teacher_id == teacher.id,
#                                      Duty.intercession_date >= start_date - timedelta(days=1),
#                                      # Нужно проверить предыдущее воскресенье
#                                      Duty.intercession_date <= end_date).all()

#     # Пройдем по каждой неделе от start_date до end_date
#     current_date = start_date
#     while current_date <= end_date:
#         week = {}
#         for i in range(7):  # Проход по дням недели (от понедельника до воскресенья)
#             day_name = days_of_week[i]
#             current_day = current_date + timedelta(days=i)
#             week[day_name] = [{'date': current_day.strftime("%Y-%m-%d")}]

#             # Добавление занятий в этот день
#             lessons = [s for s in schedule_records if s.date == current_day]
#             for lesson in lessons:
#                 pair = Pairs.query.get(lesson.pair_id)
#                 discipline = Discipline.query.get(lesson.disc_id)
#                 lesson_info = {
#                     'type': 'lesson',
#                     'start_time': pair.pair_start_time.strftime("%H:%M"),
#                     'end_time': pair.pair_end_time.strftime("%H:%M"),
#                     'auditorium': lesson.auditorium,
#                     'group': lesson.group,
#                     'faculty': pair.faculty,
#                     'pair_number': pair.pair_number,
#                     'disc_name': discipline.name
#                 }
#                 week[day_name].append(lesson_info)

#             # Добавление дежурств в этот день
#             duties = [d for d in duty_records if d.intercession_date == current_day]
#             if duties:
#                 for duty in duties:
#                     corpus = Corpus.query.get(duty.corpus_id)
#                     duty_info = {
#                         'type': 'duty',
#                         'start_time': corpus.duty_start_time.strftime("%H:%M"),
#                         'end_time': '23:59',
#                     }
#                     week[day_name].append(duty_info)

#             # Проверка дежурства, которое началось накануне (например, в воскресенье)
#             if i == 0:  # Если это понедельник, проверяем воскресенье
#                 previous_sunday = current_day - timedelta(days=1)
#                 sunday_duties = [d for d in duty_records if d.intercession_date == previous_sunday]
#                 if sunday_duties:
#                     for duty in sunday_duties:
#                         corpus = Corpus.query.get(duty.corpus_id)
#                         duty_info = {
#                             'type': 'duty',
#                             'start_time': '00:00',
#                             'end_time': corpus.duty_end_time.strftime("%H:%M"),
#                         }
#                         week[day_name].append(duty_info)

#             # Сортировка событий в хронологическом порядке по start_time
#             week[day_name] = sorted(week[day_name], key=lambda x: x.get('start_time', '00:00'))

#         weeks.append(week)
#         current_date += timedelta(weeks=1)

#     return jsonify(weeks)


# @app.route('/personal_stat', methods=['POST'])
# def personal_stat():
#     data = request.get_json()

#     # Достаем параметры из запроса
#     access_token = data.get('accessToken')
#     month = data.get('month')
#     year = data.get('year')
#     end_time = data.get('endTime')

#     # Получаем информацию о преподавателе по токену
#     teacher = db.session.query(Teachers).filter_by(access_token=access_token).first()
#     if not teacher:
#         return jsonify({"error": "Invalid access token"}), 401

#     teacher_id = teacher.id

#     # Преобразуем end_time в формат datetime
#     try:
#         end_time_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
#     except ValueError:
#         return jsonify({"error": "Invalid end time format. Use ISO 8601 format."}), 400

#     # 1. Получаем статистику за указанный месяц

#     # Количество подтвержденных нарядов по корпусам за месяц до end_time
#     month_duty_stats = db.session.query(
#         Corpus.name.label('corpus_name'),
#         func.count(Duty.id).label('duty_count')
#     ).join(Duty, Duty.corpus_id == Corpus.id) \
#      .join(Notifications, Notifications.duty_id == Duty.id) \
#      .filter(and_(
#          Duty.teacher_id == teacher_id,
#          extract('month', Duty.intercession_date) == month,
#          extract('year', Duty.intercession_date) == year,
#          Notifications.confirmed == True,
#          Duty.intercession_date < end_time_dt.date()
#      )).group_by(Corpus.name).all()

#     # Общее количество подтвержденных нарядов по корпусам за весь месяц
#     month_all_duty_stats = db.session.query(
#         Corpus.name.label('corpus_name'),
#         func.count(Duty.id).label('all_duty')
#     ).join(Duty, Duty.corpus_id == Corpus.id) \
#      .join(Notifications, Notifications.duty_id == Duty.id) \
#      .filter(and_(
#          Duty.teacher_id == teacher_id,
#          extract('month', Duty.intercession_date) == month,
#          extract('year', Duty.intercession_date) == year,
#          Notifications.confirmed == True,
#      )).group_by(Corpus.name).all()

#     # Количество пар за указанный месяц до end_time
#     month_pair_stats = 5
#     month_pair_stats = db.session.query(
#         func.count(Schedule.id).label('pair_count')
#     ).join(Pairs, Pairs.id == Schedule.pair_id) \
#      .filter(and_(
#          Schedule.teacher_id == teacher_id,
#          extract('month', Schedule.date) == month,
#          extract('year', Schedule.date) == year,
#          or_(Schedule.date < end_time_dt.date(), and_(Schedule.date == end_time_dt.date(), Pairs.pair_end_time < end_time_dt.time()))
#      )).scalar()
#         #
#         # # Общее количество пар за месяц
#     month_all_pair_stats = db.session.query(
#         func.count(Schedule.id).label('all_pair')
#     ).filter(and_(
#         Schedule.teacher_id == teacher_id,
#         extract('month', Schedule.date) == month,
#         extract('year', Schedule.date) == year
#     )).scalar()

#     # 2. Получаем статистику за указанный год

#     # Количество подтвержденных нарядов по корпусам за год до end_time
#     year_duty_stats = db.session.query(
#         Corpus.name.label('corpus_name'),
#         func.count(Duty.id).label('duty_count')
#     ).join(Duty, Duty.corpus_id == Corpus.id) \
#      .join(Notifications, Notifications.duty_id == Duty.id) \
#      .filter(and_(
#          Duty.teacher_id == teacher_id,
#          extract('year', Duty.intercession_date) == year,
#          Notifications.confirmed == True,
#          Duty.intercession_date < end_time_dt.date()
#      )).group_by(Corpus.name).all()

#     # Общее количество подтвержденных нарядов за весь год
#     year_all_duty_stats = db.session.query(
#         Corpus.name.label('corpus_name'),
#         func.count(Duty.id).label('all_duty')
#     ).join(Duty, Duty.corpus_id == Corpus.id) \
#      .join(Notifications, Notifications.duty_id == Duty.id) \
#      .filter(and_(
#          Duty.teacher_id == teacher_id,
#          extract('year', Duty.intercession_date) == year,
#          Notifications.confirmed == True
#      )).group_by(Corpus.name).all()

#     # Количество пар за указанный год до end_time
#     year_pair_stats = db.session.query(
#         func.count(Schedule.id).label('pair_count')
#     ).join(Pairs, Pairs.id == Schedule.pair_id) \
#      .filter(and_(
#          Schedule.teacher_id == teacher_id,
#          extract('year', Schedule.date) == year,
#          or_(Schedule.date < end_time_dt.date(), and_(Schedule.date == end_time_dt.date(), Pairs.pair_end_time < end_time_dt.time()))
#      )).scalar()
    
#     # Общее количество пар за год
#     year_all_pair_stats = db.session.query(
#         func.count(Schedule.id).label('all_pair')
#     ).filter(and_(
#         Schedule.teacher_id == teacher_id,
#         extract('year', Schedule.date) == year
#     )).scalar()

#     # Формируем данные для возврата
#     def format_duty_stats(duty_stats, all_duty_stats):
#         result = {}
#         for stat in all_duty_stats:
#             result[stat.corpus_name] = {
#                 'duty_count': 0,
#                 'all_duty': stat.all_duty
#             }

#         for stat in duty_stats:
#             if stat.corpus_name in result:
#                 result[stat.corpus_name]['duty_count'] = stat.duty_count

#         return result

#     month_data = format_duty_stats(month_duty_stats, month_all_duty_stats)
#     month_data['pair_count'] = month_pair_stats
#     month_data['all_pair'] = month_all_pair_stats

#     year_data = format_duty_stats(year_duty_stats, year_all_duty_stats)
#     year_data['pair_count'] = year_pair_stats
#     year_data['all_pair'] = year_all_pair_stats

#     return jsonify({"month": month_data, "year": year_data}), 200





# @app.route('/adstat', methods=['POST'])
# def statistics():
#     data = request.get_json()

#     # Получаем месяц и год из запроса
#     month = data.get('month')
#     year = data.get('year')

#     if not month or not year:
#         return jsonify({"error": "Month and year are required"}), 400

#     # 1. Получаем количество нарядов за указанный месяц
#     month_duty_stats = db.session.query(
#         Teachers.first_name,
#         Teachers.last_name,
#         func.count(Duty.id).label('duty_count'),
#         func.count(Schedule.id).label('pair_count')
#     ).outerjoin(Duty, (Duty.teacher_id == Teachers.id) & (extract('month', Duty.intercession_date) == month) & (extract('year', Duty.intercession_date) == year)) \
#      .outerjoin(Schedule, (Schedule.teacher_id == Teachers.id) & (extract('month', Schedule.date) == month) & (extract('year', Schedule.date) == year)) \
#      .group_by(Teachers.id).all()

#     # 2. Получаем количество нарядов за весь указанный год
#     year_duty_stats = db.session.query(
#         Teachers.first_name,
#         Teachers.last_name,
#         func.count(Duty.id).label('duty_count'),
#         func.count(Schedule.id).label('pair_count')
#     ).outerjoin(Duty, (Duty.teacher_id == Teachers.id) & (extract('year', Duty.intercession_date) == year)) \
#      .outerjoin(Schedule, (Schedule.teacher_id == Teachers.id) & (extract('year', Schedule.date) == year)) \
#      .group_by(Teachers.id).all()

#     # Форматируем данные для месяца
#     month_data = []
#     for stat in month_duty_stats:
#         month_data.append({
#             "first_name": stat.first_name,
#             "last_name": stat.last_name,
#             "pair_count": stat.pair_count,
#             "duty_count": stat.duty_count
#         })

#     # Форматируем данные для года
#     year_data = []
#     for stat in year_duty_stats:
#         year_data.append({
#             "first_name": stat.first_name,
#             "last_name": stat.last_name,
#             "pair_count": stat.pair_count,
#             "duty_count": stat.duty_count
#         })

#     # Возвращаем данные в нужном формате
#     return jsonify({"month": month_data, "year": year_data}), 200


# @app.route('/duty', methods=['POST'])
# def duty():
#     data = request.get_json()

#     # 1. Получаем accessToken и список дежурств
#     access_token = data.get('accessToken')
#     duties = data.get('duties', [])

#     # Проверяем, есть ли хотя бы одно дежурство
#     if not duties:
#         return jsonify({"error": "No duties provided"}), 400

#     # 2. Находим преподавателя (sender) по accessToken
#     sender = db.session.query(Teachers).filter_by(access_token=access_token).first()
#     if not sender:
#         return jsonify({"error": "Invalid access token"}), 401

#     sender_id = sender.id

#     # 3. Обрабатываем каждое дежурство и записываем в таблицы
#     for duty_data in duties:
#         try:
#             # Извлекаем данные для duty
#             teacher_id = duty_data['teacher_id']
#             corpus_id = duty_data['corpus_id']
#             date = datetime.strptime(duty_data['date'], '%Y-%m-%d').date()
#             current_time = datetime.strptime(duty_data['current_time'], '%Y-%m-%d %H:%M:%S')

#             # 4. Запись в таблицу Duty
#             new_duty = Duty(teacher_id=teacher_id, corpus_id=corpus_id, intercession_date=date)
#             db.session.add(new_duty)
#             db.session.commit()  # Коммитим, чтобы получить ID записи

#             # 5. Запись в таблицу Notifications
#             duty_id = new_duty.id  # Получаем ID новой записи duty
#             new_notification = Notifications(
#                 sender=sender_id,
#                 recipient=teacher_id,
#                 request_time=current_time,
#                 duty_id=duty_id,
#                 confirmed=None,  # Оставляем null
#                 response_time=None  # Оставляем null
#             )
#             db.session.add(new_notification)

#         except Exception as e:
#             # Если что-то пошло не так, возвращаем ошибку
#             return jsonify({"error": str(e)}), 400

#     # 6. Финальный коммит
#     db.session.commit()

#     return jsonify({"message": "Duties and notifications recorded successfully"}), 200


# @app.route('/duty_date', methods=['POST'])
# def duty_date():
#     # Получаем дату из тела запроса
#     data = request.get_json()
#     selected_date = data.get('date')

#     # Преобразуем строку в объект datetime
#     try:
#         selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
#     except ValueError:
#         return jsonify({"error": "Неверный формат даты. Ожидается 'YYYY-MM-DD'"}), 400

#     # Определяем границу месяца назад
#     one_month_ago = selected_date - timedelta(days=30)

#     # Запрашиваем всех преподавателей, используя левое соединение с таблицей Duty
#     duties = db.session.query(
#         Teachers.id,
#         Teachers.first_name,
#         Teachers.last_name,
#         db.func.coalesce(db.func.count(Duty.id), 0).label('duty_num')  # Если нет записей, то 0
#     ) \
#         .outerjoin(Duty,
#                    (Duty.teacher_id == Teachers.id) & (Duty.intercession_date.between(one_month_ago, selected_date))) \
#         .group_by(Teachers.id, Teachers.first_name, Teachers.last_name) \
#         .all()

#     # Определяем следующий день от выбранной даты
#     next_day = selected_date + timedelta(days=1)

#     # Формируем ответ
#     result = []
#     for teacher_id, first_name, last_name, duty_num in duties:
#         # Проверяем наличие пары у преподавателя на следующий день
#         lesson_exists = db.session.query(Schedule.id) \
#             .filter(Schedule.teacher_id == teacher_id, Schedule.date == next_day) \
#             .first()

#         lesson_today = True if lesson_exists else False

#         result.append({
#             'teacher_id': teacher_id,
#             'first_name': first_name,
#             'last_name': last_name,
#             'duty_num': duty_num,
#             'lesson_today': lesson_today
#         })

#     # Возвращаем список учителей с количеством нарядов за последний месяц и наличием пары на следующий день
#     return jsonify(result)


# @app.route('/duty_type', methods=['POST'])
# def duty_corpus():
#     corpora = Corpus.query.all()

#     # Формируем массив с именами
#     corpus_names = []
#     for corp in corpora:
#         corpus_names.append({"id": corp.id, "name": corp.name})
#     # Возвращаем массив в формате JSON
#     return jsonify(corpus_names), 200


# @app.route('/not_response', methods=['POST'])
# def confirm():
#     data = request.get_json()
#     notification = Notifications.query.filter_by(id=data['notification_id']).first()
#     notification.response_time = data["response_time"]
#     notification.confirmed = data["confirmed"]
#     db.session.commit()
#     return jsonify({'mess': 'OK'}), 200


# @app.route('/notifications', methods=['POST'])
# def get_notifications():
#     access_token = request.get_json()["tok"]

#     if not access_token:
#         return jsonify({'error': 'Access token is required'}), 401

#     # Поиск пользователя по access_token
#     user = Teachers.query.filter_by(access_token=access_token).first()

#     if not user:
#         return jsonify({'error': 'Invalid access token'}), 403

#     # Получение списка уведомлений, принадлежащих пользователю
#     notifications = Notifications.query \
#         .options(joinedload(Notifications.duty).joinedload(Duty.corpus)) \
#         .filter_by(recipient=user.id) \
#         .all()

#     # Формирование ответа
#     result = []
#     for notification in notifications:
#         result.append({
#             'id': notification.id,
#             'corpus_name': notification.duty.corpus.name,
#             'intercession_date': notification.duty.intercession_date.strftime('%Y-%m-%d'),
#             'request_time': notification.request_time.strftime(
#                 '%Y-%m-%d %H:%M:%S') if notification.request_time else None,
#             'response_time': notification.response_time.strftime(
#                 '%Y-%m-%d %H:%M:%S') if notification.response_time else None,
#             'confirmed': notification.confirmed
#         })

#     return jsonify(result), 200


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     # Проверяем, что файл был отправлен
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['file']  # Получаем файл из запроса
#     table_name = request.form['table_name']  # Получаем имя таблицы
#     csv_data = StringIO(file.read().decode('utf-8-sig'))
#     reader = csv.DictReader(csv_data, delimiter=';')  # Используем DictReader для чтения с заголовками

#     # Получаем таблицу по имени с использованием SQLAlchemy
#     metadata = db.metadata
#     table = Table(table_name, metadata, autoload_with=db.engine)
#     if table is None:
#         return jsonify({"error": "Table not found"}), 404

#     # Получаем список полей из таблицы
#     table_columns = [column.name for column in table.columns]

#     # Проверяем, соответствуют ли заголовки CSV полям таблицы
#     csv_fields = reader.fieldnames
#     if not set(csv_fields).issubset(set(table_columns)):
#         return jsonify({
#             "error": "CSV headers do not match table columns",
#             "csv_fields": csv_fields,
#             "table_columns": table_columns
#         }), 400

#     # Получаем существующие записи из таблицы для сравнения
#     with db.engine.connect() as connection:
#         trans = connection.begin()  # Начинаем транзакцию
#         try:
#             existing_records = connection.execute(table.select()).fetchall()
#             existing_data_set = []
#             for i in existing_records:
#                 existing_data_set.append(dict(zip(table_columns, i)))

#             new_rows = 0
#             faild_rows = 0

#             # Функция для преобразования строки в нужный тип или оставления строки, если тип не подходит
#             def convert_value(value, column_type):
#                 if value == '':
#                     return None
#                 if isinstance(column_type, db.Integer):
#                     try:
#                         return int(value)
#                     except ValueError:
#                         return value  # Оставляем как строку, если не получилось преобразовать
#                 elif isinstance(column_type, db.Float):
#                     try:
#                         return float(value)
#                     except ValueError:
#                         return value  # Оставляем как строку
#                 elif isinstance(column_type, db.Boolean):
#                     if value.lower() in ('true', '1'):
#                         return True
#                     elif value.lower() in ('false', '0'):
#                         return False
#                     else:
#                         return value  # Оставляем как строку, если не соответствует булевым значениям
#                 elif isinstance(column_type, db.Date) or isinstance(column_type, db.DateTime):
#                     try:
#                         parsed_date = date_parser.parse(value)  # Парсим строку с датой
#                         if isinstance(column_type, db.Date):
#                             return parsed_date.date()  # Возвращаем дату без времени
#                         return parsed_date  # Для DateTime возвращаем полную дату и время
#                     except (ValueError, OverflowError):
#                         return value  # Оставляем строку, если не удалось распознать дату
#                 return value  # Оставляем строку, если это не специальный тип

#             # Итерируем по строкам CSV
#             for row in reader:
#                 if row not in existing_data_set:
#                     # Преобразование типов на основе схемы таблицы
#                     for key, value in row.items():
#                         # Получаем тип столбца из модели
#                         column_type = table.columns[key].type
#                         row[key] = convert_value(value, column_type)

#                     # Обработка пароля для таблицы "teachers"
#                     if table_name == "teachers":
#                         row["password"] = generate_password_hash(row["password"])

#                     try:
#                         connection.execute(insert(table), row)
#                         new_rows += 1
#                     except Exception as e:
#                         faild_rows += 1

#             trans.commit()  # Коммитим транзакцию
#         except Exception as e:
#             trans.rollback()  # Откатываем транзакцию в случае ошибки
#         finally:
#             connection.close()

#     return jsonify({"message": f"Added {new_rows} new rows"}), 200


# @app.route('/upload_items', methods=['POST'])
# @cross_origin()
# def upload_items():
#     data = request.get_json()
#     if data['s'] == "q":
#         try:
#             table_names = list(db.metadata.tables.keys())
#         except:
#             table_names = []
#         res = jsonify(names=table_names), 200
#         return res
#     else:
#         return jsonify({"message": "Bad Request"}), 400


# @app.route('/login', methods=['POST'])
# @cross_origin()
# def login():

#     data = request.get_json()
#     if not data or not data.get('username') or not data.get('password'):
#         return jsonify({"message": "Username and password required"}), 400

#     user = Teachers.query.filter_by(login=data['username']).first()
#     if user is None:
#         return jsonify({"message": "Invalid credentials"}), 401

#     hash_pass = generate_password_hash(user.password)
#     print(check_password_hash(hash_pass, data['password']))
#     if user and check_password_hash(user.password, data['password']):
#         # Создаем токены
#         access_token = create_access_token(identity={'username': user.login, 'role': user.role})
#         refresh_token = create_refresh_token(identity={'username': user.login, 'role': user.role})

#         # Сохраняем токены в базе данных
#         user.access_token = access_token
#         user.refresh_token = refresh_token
#         db.session.commit()

#         return jsonify(access_token=access_token, refresh_token=refresh_token), 200
#     return jsonify({"message": "Invalid credentials"}), 401


# @app.route('/refresh', methods=['POST'])
# @jwt_required(refresh=True)
# def refresh():
#     identity = get_jwt_identity()
#     access_token = create_access_token(identity=identity)
#     return jsonify(access_token=access_token), 200


# if __name__ == '__testback__':
#     app.run(debug=True, host='localhost', port=5000)