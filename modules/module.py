import requests
import time
import re
import threading
#from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor


global ts_last_greeting
ts_last_greeting = 0


# class Uploader:
#     def __init(self, filename, file_host_url):
#         self.filename = filename
#         self.file_host_url = file_host_url
#
#     def _multipart_post(self, data):
#         encoder = MultipartEncoder(fields=data)
#         monitor = MultipartEncoderMonitor(encoder)
#         r = requests.post(self.file_host_url,
#                           data=monitor,
#                           headers={'Content-Type': monitor.content_type})
#         return r
#
# class FileioUploader(Uploader):
#     def __init__(self, filename):
#         self.filename = filename
#         self.file_host_url = "https://file.io"
#
#     def execute(self):
#         file = open('./cache/{}'.format(self.filename), 'rb')
#         try:
#             data = {'file': (file.name, file, self._mimetype())}
#             response = self._multipart_post(data)
#         finally:
#             file.close()
#
#         return response.json()['link']


# class CatboxUploader(Uploader):
#     def __init__(self, filename):
#         self.filename = filename
#         self.file_host_url = "https://catbox.moe/user/api.php"
#
#     def execute(self):
#         file = open('./cache/{}'.format(self.filename), 'rb')
#         try:
#             data = {
#                 'reqtype': 'fileupload',
#                 'userhash': 'd4536907ecfa84d32cb37d993',
#                 'fileToUpload': (file.name, file)
#             }
#             response = self._multipart_post(data)
#         finally:
#             file.close()
#
#         return response.text
#



# uploader_classes = {
#     "catbox": CatboxUploader,
#     "fileio": FileioUploader
# }




# def upload(host, name):
#     uploader_class = uploader_classes[host]
#     uploader_instance = uploader_class(name)
#     print(name)
#     result = uploader_instance.execute()
#     print("Your link : {}".format(result))
#     return result


class Commands:
    def __init__(self):
        self.session = requests.session()

        """
        Modulos de conexão com o servidor Drrr.com
        :load_cookie =  faz login no site utilizando o cookie salvo
        :leave_room = espesifica a função para o Bot sair da sala
        :kick_room = espesifica a função do Bot kikar alguém da sala
        :new_host = Essa função server para o Bot dar "Admin"/host para
        outra pessoa dentro da sala
        :post = função declada para poder mandar menssagem
        :share_music = função declada para poder mandar audio/musica
        """

    def load_cookie(self, file_name):
        f = open(file_name, 'r')
        self.session.cookies.update(eval(f.read()))
        f.close()

    def leave_room(self):
        leave_body = {
            'leave': 'leave'
        }
        lr = self.session.post('https://drrr.com/room/?ajax=1', leave_body)
        lr.close()

    def kick_room(self):
        kick_body = {
            'kick': 'kick'
        }
        kc = self.session.post('https://drrr.com/room/?ajax=1', kick_body)
        kc.close()

    def new_host(self, new_host_id):
        new_host_body = {
            'new_host': new_host_id
        }
        nh = self.session.post('https://drrr.com/room/?ajax=1', new_host_body)
        nh.close()

    def post(self, message, url='', to=''):
        post_body = {
            'message': message,
            'url': url,
            'to': to
        }
        p = self.session.post(
            url='https://drrr.com/room/?ajax=1', data=post_body)
        p.close()

    def room_enter(self, url_room):
        re = self.session.get(url_room)
        re.close()
        room = self.session.get('https://drrr.com/json.php?fast=1')
        return room.text

    """
    room_update: Atualiza a Sala a cada 1 segundo  procurando novas menssagens
    e assim sabendo de algum usuario digitou alguém comando,
    alem de ser nessa mesma função onde o bot captura 
    info_sender = Informação do autor (tripcode, id e outras coisas)
    name_sender = Autor da menssagem
    message = Menssagem enviada
    """

    def room_update(self, room_text):
        update = re.search('"update":\d+.\d+', room_text).group(0)[9:]
        url_room_update = 'https://drrr.com/json.php?update=' + update
        while 1:
            time.sleep(1)
            ru = self.session.get(url_room_update)
            update = re.search('"update":\d+.\d+', ru.text).group(0)[9:]
            url_room_update = 'https://drrr.com/json.php?update=' + update
            """
            Quando alguem entra ou sai da sala ele solta uma preve frase
            "type":"join" referece a qunado alguem entra na sala o mesmo se aplica a
                                   "type":"leave" 
                todos esses dados são pegos na propria api do site
                        https://drrr.com/room/?ajax=1
            """
            if '"type":"join"' in ru.text:
                self.post('/me Приветствует!')
            ru.close()
            if '"type":"leave"' in ru.text:
                self.post('/me Прощается!')
            ru.close()

            if 'talks' in ru.text:
                talks_update = re.findall(
                    '{"id".*?"message":".*?"}', re.search('"talks":.*', ru.text).group(0))
                # talk in "talks" block
                for tu in talks_update:
                    info_sender = re.findall('"from":{.*?}', tu)
                    info_sender = info_sender[0]
                    tripcode = re.findall(
                        '"tripcode":".*?"', info_sender)[0][12:-1]
                    name_sender = re.findall(
                        '"name":".*?"', info_sender)[0][8:-1]
                    message = re.search('"message":".*?"', tu).group(0)[11:-1].encode(encoding='utf-8').decode(
                        encoding='unicode-escape')
                    # log mostrado no shell quando se execulta o bot
                    # print('@%s: %s' % (name_sender,message))
                    if '/' in message or '@Void' in message:
                        info_sender = re.findall('"from":{.*?}', tu)
                        if info_sender:
                            info_sender = info_sender[0]
                            name_sender = re.findall(
                                '"name":".*?"', info_sender)[0][8:-1]
                            tripcode = re.findall(
                                '"tripcode":".*?"', info_sender)[0][12:-1]
                            # condição para o bot nao ficar auto se respondendo suas requisições
                            if name_sender == u'Void':
                                continue
                            id_sender = re.findall(
                                '"id":".*?"', info_sender)[0][6:-1]
                            # pesquisa "to" no bloco html
                            info_receiver = re.findall('"to":{.*?}', tu)
                            # condição no main para verificar se o bot esta fora da sala/banido de alguma sala
                            if info_receiver:
                                # was handle_private_message
                                is_leave = self.handle_message(message=message, id_sender=id_sender,
                                                                       name_sender=name_sender, tripcode=tripcode)
                                if is_leave:
                                    return True
                            else:
                                self.handle_message(message=message, name_sender=name_sender,
                                                    id_sender=id_sender, tripcode=tripcode)
            ru.close()

# Bot's commands
    def help(self):
        self.post(
            message="/help\n/admin\n/ban\n/unban\n/kick")

    def prekl(self):
       self.post(message='sukaaaaa')

    """
    ===============================
    Comandos Para administradores
    /kick == kika o usuario
    /ban == bane o usaurio
    /unban == desbane o usuario
    ===============================
    """

    def admin_host(self, name_sender, tripcode, id_sender):
        # print(tripcode)
        # print(id_sender)
        # print(message)
        if tripcode == "miIi1Ds8YY":
            new_host_body = {'new_host': id_sender}
            nh = self.session.post(
                'https://drrr.com/room/?ajax=1', new_host_body)
            nh.close()
            return True
        elif tripcode != "miIi1Ds8YY":
            self.post(message='Você Não tem permissão! @{}'.format(name_sender))
        elif tripcode is None:
            self.post(message='Você Não tem permissão! @{}'.format(name_sender))

    def admin_kick(self, message, name_sender, tripcode):
        if tripcode == "miIi1Ds8YY":
            if re.findall('/kick', message):
                message = message[7:]
                kick_body = {'kick': message}
                kc = self.session.post(
                    'https://drrr.com/room/?ajax=1', kick_body)
                kc.close()
                return True
        else:
            self.post(message=u'Недостаточно прав, @{}'.format(name_sender))

    def admin_ban(self, message, name_sender, tripcode):
        if tripcode == "miIi1Ds8YY":
            if re.findall('/ban', message):
                message = message[6:]
                ban_body = {'ban': message}
                kc = self.session.post(
                    'https://drrr.com/room/?ajax=1', ban_body)
                kc.close()
                return True
        else:
            self.post(message=u'Недостаточно прав, @{}'.format(name_sender))

    def admin_unban(self, message, name_sender, tripcode):
        if tripcode == "miIi1Ds8YY":
            if re.findall('/unban', message):
                message = message[8:]
                unban_body = {'unban': message}
                # print(kick_body)
                kc = self.session.post(
                    'https://drrr.com/room/?ajax=1', unban_body)
                kc.close()
                return True
        else:
            self.post(message='Você Não tem permissão! @{}'.format(name_sender))

    def handle_message(self, message, name_sender, tripcode, id_sender):
        if '/help' in message:
            t_help = threading.Thread(
                target=self.help)
            t_help.start()
        elif '/admin' in message:
            t_host = threading.Thread(target=self.admin_host, args=(
                name_sender, tripcode, id_sender))
            t_host.start()
        # elif '/kick' in message:
        #     t_kick = threading.Thread(target=self.admin_kick, args=(
        #        message, name_sender, tripcode))
        #     t_kick.start()
        # elif '/ban' in message:
        #     t_ban = threading.Thread(target=self.admin_ban, args=(
        #         message, name_sender, tripcode))
        #     t_ban.start()
        elif '/unban' in message:
            t_unban = threading.Thread(target=self.admin_unban, args=(
                name_sender, tripcode, id_sender))
            t_unban.start()
        elif '/disconnect' in message:
            t_leave = threading.Thread(target=self.leave_room)
            t_leave.start()
        # elif '/kick_room' in message:
        #     t_kick = threading.Thread(target=self.kick_room)
        #     t_kick.start()
        elif '/lol' in message:
            t_lol = threading.Thread(target=self.prekl)
            t_lol.start()


