class BothFieldsNull(Exception):

    def __init__(self):
        self.message = "Both arguments i.e(enrollment_number and student_obj) for function push_get_student_object " \
                       "can't be null "

        super().__init__(self.message)