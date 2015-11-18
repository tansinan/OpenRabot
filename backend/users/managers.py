from users.models import UsersDao
import smtplib
from email.mime.text import MIMEText


class UsersManager():

    def __init__(self):
        self.dao = UsersDao()
        self.cur_user = None

    def __valid_passwd(self, passwd):
        if not 4 <= len(passwd) <= 24:
            return False

        for i in passwd:
            if not 32 < ord(i) < 127:
                return False

        return True

    def __send_authentication_email(self, uid, email):
        mail_host = 'smtp.sohu.com'
        mail_host_port = 25
        mail_from = 'Rabot Admin<project_rabot@sohu.com>'
        mail_from_uname = 'project_rabot'
        mail_from_passwd = 'orz_rabot'
        mail_to = email

        authentication_url = 'localhost:8000/authentication/' + str(uid)
        mail_content = """
            <h3> Welcome to Rabot -- Learn coding with a rabbit. </h3>
            <h5>Coding for fun? Is that a joke? No! </h5>
            <br>
            Thanks for your registration.<br>
            Please click this <a href="%s">link</a> to finish the registration. <br>
            <br>
            If the link above is not available, please copy the following url address: <br>
            %s<br>
        """ % (authentication_url, authentication_url)

        message = MIMEText(mail_content, _subtype='html', _charset='utf-8')
        message['Subject'] = 'Welcome to Rabot -- Learn coding with a rabbit'
        message['From'] = mail_from
        message['To'] = mail_to

        server = smtplib.SMTP(mail_host, mail_host_port)
        server.ehlo()

        server.login(mail_from_uname, mail_from_passwd)
        server.sendmail(mail_from, mail_to, message.as_string())
        server.close()

    def get_cur_user(self):
        return self.cur_user

    def clear(self):
        all_users = self.dao.get_all_users()
        for user in all_users:
            self.dao.delete_user(user)

    def registration(self, uname, passwd, email):
        if not self.__valid_passwd(passwd):
            return 'Password is invalid.'

        target = self.dao.get_user_by_uname(uname)
        if target:
            return 'Username is already used.'

        target = self.dao.get_user_by_email(email)
        if target:
            return 'Email is already used.'

        all_users = self.dao.get_all_users()
        if len(all_users) > 0:
            uid = all_users[-1].uid + 1
        else:
            uid = 1

        self.__send_authentication_email(uid, email)
        self.dao.create_user(uid, uname, passwd, email)
        self.cur_user = self.dao.get_user_by_uid(uid)

        return 'Succeeded.'

    def registration_authentication(self, uid):
        cur_user = self.dao.get_user_by_uid(uid)
        if cur_user:
            self.dao.authenticate(cur_user)
            return 'Succeeded.'
        else:
            return 'User does not exist.'

    def login(self, uname, passwd):
        cur_user = self.dao.get_user_by_uname(uname)

        if not cur_user:
            return 'User does not exist.'
        elif cur_user.passwd == passwd:
            if cur_user.authenticated:
                self.cur_user = cur_user
                return 'Succeeded.'
            else:
                return 'User has not authenticated yet, please check your email.'
        else:
            return 'Password is incorrect.'

    def logout(self, uid):
        if uid > 0:
            cur_user = self.dao.get_user_by_uid(uid)
            if not cur_user:
                return 'User does not exist or has not logged in.'
            else:
                self.cur_user = cur_user
                return 'Succeeded.'
        else:
            self.cur_user = None
            return 'User does not exist.'

    def update(self, uid, old_passwd, new_passwd, new_email):
        cur_user = self.dao.get_user_by_uid(uid)
        if not cur_user:
            return 'User does not exist.'

        if cur_user.passwd != old_passwd:
            return 'Old password is incorrect.'

        if len(new_passwd) > 0 and not self.__valid_passwd(new_passwd):
            return 'New password is invalid.'

        if len(new_email) > 0:
            target = self.dao.get_user_by_email(new_email)
            if target:
                return 'Email is already used.'

        if len(new_passwd) > 0: self.dao.update_passwd(cur_user, new_passwd)
        if len(new_email) > 0: self.dao.update_email(cur_user, new_email)
        self.cur_user = cur_user
        return 'Succeeded.'
