import pickle
import redis
from student.main import Student
from datetime import timedelta
from .exceptions import BothFieldsNull

r = redis.Redis()


def push_to_redis(enrollment_no: int, pickle_student_obj: bytes):
    r.setex(enrollment_no, timedelta(minutes=4), pickle_student_obj)


def push_get_student_object(enrollment_number: int = None, student_obj: Student = None) -> Student:
    if enrollment_number is None and student_obj is None:
        raise BothFieldsNull

    if student_obj:
        pickle_obj = pickle.dumps(student_obj)
        push_to_redis(student_obj.get_enrollment_no, pickle_obj)
        return student_obj

    obj = r.get(enrollment_number)
    push_to_redis(enrollment_number, obj)
    return pickle.loads(obj)
