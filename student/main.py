import requests
from bs4 import BeautifulSoup as bs
from . import attendance
from . import exceptions


class Student(attendance.StudentAttendance):

    def __init__(self, enrollment_number, dob, user_password):
        self.__credentials = {
            "txtInst": "Institute",
            "InstCode": "JIIT",
            "UserType101117": "S",
            "MemberCode": enrollment_number,
            "DATE1": dob,
            "Password101117": user_password,
            "txtcap": 'captcha'
        }

        self.__session = requests.Session()

        self.__creds_are_valid = False

        self.__webkiosk_url = 'https://webkiosk.jiit.ac.in/'
        self.__use_valid_url = 'https://webkiosk.jiit.ac.in/CommonFiles/UseValid.jsp'
        self.__student_info_url = 'https://webkiosk.jiit.ac.in/StudentFiles/PersonalFiles/StudPersonalInfo.jsp'

    def __check_validity(self):
        stu_info_data = self.__session.get(self.__student_info_url)

        stu_info_page = bs(stu_info_data.text, 'html.parser')
        stu_info_page_body_text = stu_info_page.find('body', class_=False, id=False).contents[0].strip()

        not_found_string = 'Unable to find profile...'

        self.__creds_are_valid = False if stu_info_page_body_text == not_found_string else True

    def login(self):
        main_page = self.__session.get(self.__webkiosk_url)

        bs4_page = bs(main_page.content, 'html.parser')

        captcha = bs4_page.find('s', class_=False, id=False)
        self.__credentials['txtcap'] = captcha.text

        self.__session.post(self.__use_valid_url, data=self.__credentials)

        self.__check_validity()

        if self.__creds_are_valid:
            print('login successful')
            super().__init__(self.__session)

        else:
            print('Unsuccessful Login')
            raise exceptions.InvalidCredentials()

    @property
    def log_is_successful(self):
        return self.__creds_are_valid

    @property
    def get_enrollment_no(self):
        return self.__credentials.get('MemberCode')
