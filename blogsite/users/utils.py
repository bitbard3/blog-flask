import os
import secrets
from PIL import Image
from flask import url_for,current_app
from flask_mail import Message
from blogsite import mail


def saveimgage(imgform):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(imgform.filename)
    img_name = random_hex + ext
    file_location = os.path.join(
        current_app.root_path, 'static/profile_pics', img_name)
    output_size = (300, 300)
    i = Image.open(imgform)
    i.thumbnail(output_size)
    i.save(file_location)

    return img_name


def send_email(user):
    token = user.create_token()
    msg = Message("FlaskFolio-Password Reset Link",
                  sender='ansh.arora2k04@gmail.com', recipients=[user.email])
    msg.body = f'''To reset you password kindly visit the following link
{url_for('users.reset_password',token=token, _external =True)}

If you didn't initiate the password reset kindly ignore the mail
    
    '''
    mail.send(msg)
