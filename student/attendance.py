from bs4 import BeautifulSoup as bs
from .exceptions import InvalidSubjectOrClassType, NoDataAvailable


class StudentAttendance:

    def __init__(self, request_session):
        self.__all_subj_attendance_data_with_links = None

        self.__attendance_page_url = 'https://webkiosk.jiit.ac.in/StudentFiles/Academic/StudentAttendanceList.jsp'

        self.__session = request_session

    def get_data(self):

        attendance_data = self.__session.get(self.__attendance_page_url)
        attendance_page = bs(attendance_data.content, 'html.parser')
        attendance_table = attendance_page.find(id='table-1')
        attendance_table_body = attendance_table.find('tbody', class_=False, id=False)
        table_contents = attendance_table_body.find_all('tr', class_=False, id=False)
        return self.__attendance_subjects(table_contents)

    def __attendance_subjects(self, table_contents):
        all_subject_attendance = {}
        all_subject_attendance_with_links = {}

        for sub in table_contents:
            all_sub_table_data = sub.find_all('td', class_=False, id=False)

            sub_name = all_sub_table_data[1].text

            all_subject_attendance[sub_name], all_subject_attendance_with_links[
                sub_name] = self.__attendance_dict_creator(all_sub_table_data)

        self.__all_subj_attendance_data_with_links = all_subject_attendance_with_links

        return all_subject_attendance

    @staticmethod
    def __attendance_dict_creator(sub_table_data):
        subject_dict = {}
        subject_dict_with_links = {}

        for i in range(len(sub_table_data)):

            attendance = sub_table_data[i].find('a', class_=False, id=False)
            if attendance:
                sub_attendance_link = attendance.attrs['href']

                if i == 2:
                    '''lec+tut'''

                    subject_dict_with_links['lecture+tutorial'] = {
                        'link': sub_attendance_link,
                        'attendance': attendance.text
                    }
                    subject_dict['lecture+tutorial'] = {
                        'attendance': attendance.text
                    }

                if i == 3:
                    '''lec'''
                    subject_dict_with_links['lecture'] = {
                        'link': sub_attendance_link,
                        'attendance': attendance.text
                    }
                    subject_dict['lecture'] = {
                        'attendance': attendance.text
                    }

                if i == 4:
                    '''tut'''
                    subject_dict_with_links['tutorial'] = {
                        'link': sub_attendance_link,
                        'attendance': attendance.text
                    }
                    subject_dict['tutorial'] = {
                        'attendance': attendance.text
                    }

                if i == 5:
                    '''lab'''
                    subject_dict_with_links['lab'] = {
                        'link': sub_attendance_link,
                        'attendance': attendance.text
                    }
                    subject_dict['lab'] = {
                        'attendance': attendance.text
                    }

        return subject_dict, subject_dict_with_links

    def get_subj_attendance(self, subj_name: str, class_type: str):

        if self.__all_subj_attendance_data_with_links is None:
            raise NoDataAvailable()

        print('called')
        print(self.__all_subj_attendance_data_with_links)
        print(subj_name, class_type)

        try:
            sub_link = self.__all_subj_attendance_data_with_links[subj_name][class_type]['link']
        except KeyError:
            raise InvalidSubjectOrClassType

        link = "https://webkiosk.jiit.ac.in/StudentFiles/Academic/" + sub_link

        subj_attendance = self.__session.get(link)

        soup_obj = bs(subj_attendance.content, 'html.parser')
        tbody = soup_obj.find('tbody', class_=False, id=False)
        tr_set = tbody.find_all('tr', class_=False, id=False)
        thead = soup_obj.find('thead', class_=False, id=False)
        tr_set_head = thead.find_all('tr', class_=False, id=False)
        all_head_td = thead.find_all('td', class_=False, id=False)

        my_dict = {}

        for index, i in enumerate(tr_set):
            all_td = i.find_all('td', class_=False, id=False)
            temp_dict = {}

            for j in range(len(all_td)):
                temp_dict[str(all_head_td[j].text.strip())] = str(all_td[j].text)

            my_dict[index] = temp_dict.copy()

        return my_dict


"""

decorators

 
        def is_authenticated(fun):
            @functools.wraps(fun)
            def inner(this):
                if this.__creds_are_valid:
                    return fun(this)
    
                def not_authenticated():
                    print('User nit authenticated')
    
                return not_authenticated()
    
            return inner()


        def data_is_available(function):
                
                @functools.wraps(function)
                def inner(this, *args, **kwargs):
        
                    if this.__all_subj_attendance_data_with_links:
        
                        return function(this, *args, **kwargs)
        
                    def no_data():
                        raise NoDataAvailable()
        
                    return no_data()
        
                return inner

"""
