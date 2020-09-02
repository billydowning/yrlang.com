from twilio.rest import Client



class SendSMSWithTwillo:

    def __init__(self):
        self.account_sid = 'AC18121903c6616bb00069fc3e82d62a30'
        self.auth_token = '9c78cda84f59cf97ba0dc699ed898966'
        self.from_mo = '+12078060423'
        self.twillo_client = Client(self.account_sid, self.auth_token)


    def send_messsge_to_user(self, to, body):

        self.twillo_client.messages.create(
            body = body,
            to = to,
            from_ = self.from_mo)
