import random
import string
import time
from threading import Thread

import pyuser_agent
import requests

ua = pyuser_agent.UA()

proxy_location = [
    "br",
    "br2",
    "ch",
    "ca",
    "cavan",
    "mx",
    "us-atl",
    "us-la",
    "us-fl",
    "us-dal",
    "us-nj",
    "us-ny",
    "us-chi",
    "us-lv",
    "us-sf",
    "us-sa",
    "us-slc",
    "aus",
    "bg",
    "cz",
    "dn",
    "fn",
    "fr",
    "ger",
    "gre",
    "hg",
    "ice",
    "ire",
    "it",
    "lux",
    "md",
    "nl2",
    "no",
    "pl",
    "pg",
    "ro",
    "ru",
    "slk",
    "sp",
    "swe",
    "swiss",
    "ukr",
    "uk",
    "hk",
    "id",
    "jp",
    "sk",
    "nz",
    "sg",
    "tw",
    "th",
    "in",
    "isr-loc1",
    "isr-loc2",
    "sa",
    "uae",
]
email_domaine = [
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "aol.com",
    "hotmail.co.uk",
    "hotmail.fr",
    "msn.com",
    "yahoo.fr",
    "wanadoo.fr",
    "orange.fr",
    "comcast.net",
    "yahoo.co.uk",
    "yahoo.com.br",
    "yahoo.co.in",
    "live.com",
    "rediffmail.com",
    "free.fr",
    "gmx.de",
    "web.de",
    "yandex.ru",
    "ymail.com",
    "libero.it",
    "outlook.com",
    "uol.com.br",
    "bol.com.br",
    "mail.ru",
    "cox.net",
    "hotmail.it",
    "sbcglobal.net",
    "sfr.fr",
    "live.fr",
    "verizon.net",
    "live.co.uk",
    "googlemail.com",
    "yahoo.es",
    "ig.com.br",
    "live.nl",
    "bigpond.com",
    "terra.com.br",
    "yahoo.it",
    "neuf.fr",
    "yahoo.de",
    "alice.it",
    "rocketmail.com",
    "att.net",
    "laposte.net",
    "facebook.com",
    "bellsouth.net",
    "yahoo.in",
    "aliceadsl.fr",
    "voila.fr",
    "club-internet.fr",
    "centurytel.net",
]
picture = [
    "https://profilepicturehyak.s3.eu-west-3.amazonaws.com/pp/IxZYdqjUPCpDsnAT955387.8069481131.jpeg",
    "https://profilepicturehyak.s3.eu-west-3.amazonaws.com/pp/IxZYdqjUPCpDsnAT656724.3567202457.png",
    "https://profilepicturehyak.s3.eu-west-3.amazonaws.com/pp/IxZYdqjUPCpDsnAT175174.57142934788.png",
]

key = "AIzaSyCmk-8N4oP5mQxdCIK5Seacmve0vu_RKqY"

THREAD_NUMBER = 1

PROXY_USER = ""
PROXY_PASSWORD = ""
PROXY_PORT = "1343"


def random_char(char_num):
    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))


class ACCOUNT:
    def __init__(self):
        self.email = (
            f"{random_char(random.randint(10, 20))}@{random.choice(email_domaine)}"
        )
        self.password = random_char(random.randint(10, 20))
        self.username = random_char(random.randint(10, 20))
        self.avatar = f"{random.choice(picture)}?{random_char(random.randint(10, 20))}"
        self.proxy_location = random.choice(proxy_location)
        self.session = requests.session()
        self.session.proxies.update(
            {
                "http": f"http://{PROXY_USER}:{PROXY_PASSWORD}@{self.proxy_location}.torguard.com:{PROXY_PORT}",
                "https": f"https://{PROXY_USER}:{PROXY_PASSWORD}@{self.proxy_location}.torguard.com:{PROXY_PORT}",
            }
        )

        self.header = {"User-Agent": ua.random, "referer": "https://www.hyakanime.fr/"}

    def test_proxy(self):
        print(f'GOOD PROXY: {self.session.get("https://api.my-ip.io/ip").text}')

    def t0(self):
        data = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True,
        }
        response = self.session.post(
            f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={key}",
            data=data,
            headers=self.header,
            timeout=5,
        ).json()
        return response

    def t1(self, response):
        data2 = {"idToken": response["idToken"]}
        self.session.post(
            f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={key}",
            data=data2,
            timeout=5,
        )

    def t2(self, response):
        data3 = {"userID": f"{response['localId']}", "username": self.username}

        self.session.post(
            "https://backend.hyakanime.fr/user/create-user/",
            data=data3,
            headers=self.header,
            timeout=5,
        )
        self.session.post(
            "https://backend.hyakanime.fr/user/create-useview/",
            data=data3,
            headers=self.header,
            timeout=5,
        )

    def t3(self, response):
        data4 = {
            "idToken": response["idToken"],
            "displayName": self.username,
            "photoUrl": f"{random.choice(picture)}?{random_char(random.randint(10, 20))}",
            "returnSecureToken": True,
        }
        self.session.post(
            f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/setAccountInfo?key={key}",
            data=data4,
            timeout=5,
        )

    def t4(self, response):
        data5 = {"photoURL": self.avatar, "username": self.username}
        self.session.post(
            f'https://backend.hyakanime.fr/user/activate-profile/{response["idToken"]}',
            data=data5,
            timeout=5,
        )


def create_account():
    try:
        account = ACCOUNT()
        t0 = account.t0()
        account.t1(t0)
        account.t2(t0)
        account.t3(t0)
        account.t4(t0)
        print(f"{account.email}:{account.password} | {account.proxy_location}")
        del account
    except:
        pass


def wait():
    print("Short break to rest the google API...")
    time.sleep(7)
    launch()


def launch():
    thds = []
    for _ in range(THREAD_NUMBER):
        if len(thds) > 0 and len(thds) % 10 == 0:
            for thdj in thds:
                thdj.join()

            thds = []

        thd = Thread(target=create_account)
        thd.start()
        thds.append(thd)

    wait()


if __name__ == "__main__":
    launch()
