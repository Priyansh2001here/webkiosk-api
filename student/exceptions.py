from requests.exceptions import ConnectionError


class InvalidCredentials(Exception):

    def __init__(self, message=None):

        if message:
            self.message = message

        else:
            self.message = "Credentials Provided were invalid please enter correct password and dob should be in " \
                           "format 'dd-mm-yy' "

        super().__init__(self.message)


class InvalidSubjectOrClassType(KeyError):

    def __init__(self):
        self.message = "Subject name or Class type is invalid"

        super().__init__(self.message)


class NoDataAvailable(Exception):

    def __init__(self):
        self.message = 'Please run get_data method associated with student object before accessing data from other methods'

        super().__init__(self.message)