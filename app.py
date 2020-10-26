from flask import Flask, jsonify, request
from student.main import Student
from student.exceptions import InvalidCredentials, ConnectionError, NoDataAvailable, InvalidSubjectOrClassType
from redis_manager.redis_manager import push_get_student_object

app = Flask(__name__)


@app.route('/', methods=['POST'])
def hello_world():
    try:
        credentials_dict = request.form.to_dict().values()
        print('creds -> ', credentials_dict)

        if len(credentials_dict) == 0:
            return jsonify('required credentials missing')

        s = Student(*credentials_dict)

    except InvalidCredentials as e:
        return jsonify(e.message)

    try:
        s.login()
    except ConnectionError:
        print('Webkiosk is not working properly')
        return jsonify('Unable to reach webkiosk, probably host is not working properly')
    except InvalidCredentials as _:
        return jsonify('invalid credentials')

    if s.log_is_successful:
        enr_no = request.form.get('enrollment_number')

        push_get_student_object(enrollment_number=enr_no, student_obj=s)
        del s

        return jsonify('Login successful')

    else:
        return jsonify('Unable to login, unexpected error occurred')


@app.route('/get-all-subject-attendance')
def all_subj_attendance():
    enr_num = request.form.get('enrollment_number')

    if enr_num is None:
        return jsonify('enrollment number not sent along with other data')

    user_obj = push_get_student_object(enrollment_number=enr_num)

    if user_obj is None:
        return jsonify('You need to login before you can continue')

    return jsonify(user_obj.get_data())


@app.route('/get-subj-attendance')
def get_subj_attendance():
    data = None
    enr_num = request.form.get('enrollment_number')

    if enr_num is None:
        return jsonify('enrollment number not sent along with other data')

    user_obj: Student = push_get_student_object(enrollment_number=enr_num)

    if user_obj is None:
        return jsonify('You need to login before you can continue')

    subj_name = request.form.get('subj_name')
    class_type = request.form.get('class_type')

    if subj_name is None or class_type is None:
        return jsonify('subject name and class type not sent along with other data')

    print(subj_name, class_type)

    try:
        data = user_obj.get_subj_attendance(subj_name, class_type)

    except NoDataAvailable:
        user_obj.get_data()

        try:
            data = user_obj.get_subj_attendance(subj_name, class_type)

        except KeyboardInterrupt as _:
            exit(1)

        except:
            return jsonify('unknown error occurred')

    except InvalidSubjectOrClassType:
        return jsonify("attendance of required subject or classType for this subject doesn't exist")

    return data


if __name__ == '__main__':
    app.run()


