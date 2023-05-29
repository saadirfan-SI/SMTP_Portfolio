from socket import *
import ssl
import base64

# Some global variables
SMTP_MAIL_SERVER = 'smtp-mail.outlook.com'
SMTP_TLS_PORT = 587
END_MESSAGE = '\r\n.\r\n'

client_socket = None
ssl_context = None


def send_line(line):
    global client_socket
    print('CLIENT: ' + line.strip())
    client_socket.send(line.encode())
    response = client_socket.recv(1024).decode()
    return response


def get_code(response):
    return int(response[:3])


def connect():
    global client_socket
    global ssl_context
    print('CLIENT: Connecting to ' + SMTP_MAIL_SERVER)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SMTP_MAIL_SERVER, SMTP_TLS_PORT))
    response = client_socket.recv(1024).decode()
    return response


def send_ehlo():
    helo = 'ehlo smtp-mail.outlook.com\r\n'
    return send_line(helo)


def send_helo():
    helo = 'helo smtp-mail.outlook.com\r\n'
    return send_line(helo)


def start_tls():
    global client_socket
    global ssl_context
    response = send_line('STARTTLS \r\n')
    ssl_context = ssl._create_stdlib_context()
    client_socket = ssl_context.wrap_socket(client_socket, server_hostname=SMTP_MAIL_SERVER)
    return response


def send_auth_request():
    return send_line('auth login \r\n')


def send_username(username):
    as_bytes = username.encode('ascii')
    as_b64 = base64.b64encode(as_bytes)
    as_utf8 = as_b64.decode('utf-8')
    return send_line(as_utf8 + '\r\n')


def send_password(password):
    as_bytes = password.encode('ascii')
    as_b64 = base64.b64encode(as_bytes)
    as_utf8 = as_b64.decode('utf-8')
    return send_line(as_utf8 + '\r\n')


'''--------------------------------------------------------------------------------
TODO - Implement the functions below this point in order to send a test
       email successfully using SMTP commands  
--------------------------------------------------------------------------------'''


def send_mail_from(sender):
    # TODO write code to send the MAIL FROM command
    sender = 'Mail From: ' + sender + '\r\n'
    return send_line(sender)

def send_rcpt_to(recipient):
    # TODO write code to send the RCPT TO command
    recipient = 'RCPT To: ' + recipient + '\r\n'
    return send_line(recipient)

def send_begin_data():
    # TODO write code to send the DATA command
    DATA = 'DATA\r\n'
    return send_line(DATA)

def send_message(subject, message):
    # TODO write code to send the message (optionally - include a subject line)
    subjectOfEmail = 'subject: ' + subject + '\r\n\r\n'
    messageToRCPT = message + '\r\n'
    return send_line(subjectOfEmail + messageToRCPT + END_MESSAGE)

def send_quit():
    # TODO write code to send the QUIT command
    endEmail = 'QUIT\r\n'
    return send_line(endEmail)



'''--------------------------------------------------------------------------------
TODO - Implement the functions above this point in order to send a test
       email successfully using SMTP commands  
--------------------------------------------------------------------------------'''


def send_one_email():
    # Open a TCP connection - the reply should start '220'
    reply = connect()
    print('SERVER: ' + reply)
    # Send a EHLO command - the reply should be a list of supported
    # 'enhanced' SMTP functions each starting '250'
    reply = send_ehlo()
    print('SERVER: ' + reply)
    # Ask the server to switch to TLS - reply should start '220'
    reply = start_tls()
    print('SERVER: ' + reply)
    # Send a HELO command encrypted - reply should start '220'
    reply = send_helo()
    print('SERVER: ' + reply)
    # Send an AUTH LOGIN command
    reply = send_auth_request()
    print('SERVER: ' + reply)
    # Send your (base64 encoded username) -
    reply = send_username(username)
    print('SERVER: ' + reply)
    # Send your (base64 encoded username) -
    reply = send_password(password)
    print('SERVER: ' + reply)
    # Send MAILFROM command - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply = send_mail_from('saad___irfan@outlook.com')
    print('SERVER: ' + reply)
    # Send RCPT TO command - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply=send_rcpt_to(reciptent)
    print('SERVER: ' + reply)
    # Send DATA command - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply = send_begin_data()
    print('SERVER: ' + reply)
    # Send the message (including subject) - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply = send_message(subject, message)
    print('SERVER: ' + reply)
    # Quit the SMTP session - TODO - YOU IMPLEMENT THE FUNCTION BELOW
    reply = send_quit()
    print('SERVER: ' + reply)


if __name__ == '__main__':
    send_new_mail = 'Yes'
    print(' Welcome\n Please Enter Your Username and Password\n')
    username = input('Username: ')
    password = input('Password: ')
    while send_new_mail == 'Yes':
        print('Welcome back ' + username + '\n')
        sender = username
        print('Mail from ' + sender)
        reciptent = input('Send To: ')
        subject = input('Subject: ')
        message = input('Message: ')
        send_one_email()
        send_new_mail= input('Do you want to send another email? Yes or No \n')


