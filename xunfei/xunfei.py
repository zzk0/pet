import requests
import datetime
import hashlib
import base64
import hmac
import json


class XunfeiApi(object):

    def __init__(self):
        self.APPID = "b322250b"
        self.Secret = "ZGE5MWYxY2UxNzJlZWUwZmVkOTY2Njdi"
        self.APIKey= "583eaf9d70669263f2e35f999ba2a7f8"
        
        self.host = 'ntrans.xfyun.cn'
        self.request_uri = "/v2/ots"
        self.url="https://" + self.host + self.request_uri
        self.http_method = "POST"
        self.algorithm = "hmac-sha256"
        self.http_proto = "HTTP/1.1"

        cur_time_utc = datetime.datetime.utcnow()
        self.date = self.__httpdate(cur_time_utc)

    def __call__(self, text: str, from_lang: str, to_lang: str) -> str:
        return self.translate(text, from_lang, to_lang)

    def translate(self, text: str, from_lang: str, to_lang: str):
        business_args = {
            "from": from_lang,
            "to": to_lang
        }
        return self.__call_url(self.__get_body(text, business_args))

    def __hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def __httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.
        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def __generate_signature(self, digest):
        signatureStr = "host: " + self.host + "\n"
        signatureStr += "date: " + self.date + "\n"
        signatureStr += self.http_method + " " + self.request_uri \
                        + " " + self.http_proto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def __init_header(self, data):
        digest = self.__hashlib_256(data)
        sign = self.__generate_signature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.algorithm, sign)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.host,
            "Date": self.date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def __get_body(self, text: str, business_args: dict):
        content = str(base64.b64encode(text.encode('utf-8')), 'utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": business_args,
            "data": {
                "text": content,
            }
        }
        body = json.dumps(postdata)
        return body

    def __call_url(self, body):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            print('appid, apikey, apisecret is empty')
        else:
            code = 0
            headers = self.__init_header(body)
            response = requests.post(self.url, data=body, headers=headers, timeout=8)
            status_code = response.status_code
            if status_code != 200:
                print("http status code", status_code, ", error information: ", response.text)
                print("please check the documentation: https://www.xfyun.cn/doc/nlp/niutrans/API.html")
                raise RuntimeError
            else:
                respData = json.loads(response.text)
                code = str(respData["code"])
                if code != '0':
                    print("error code: ", code, "please go to https://www.xfyun.cn/document/error-code?code=", code, "for more help")
                return respData['data']['result']['trans_result']['dst']
        return ""

if __name__ == '__main__':
    # back-translation
    trans = XunfeiApi()

    origin_lang = 'zh'
    temp_lang = 'ja'
    text = "若打开IP白名单，则服务端会检查调用方IP是否在讯飞开放平台配置的IP白名单中，对于没有配置到白名单中的IP发来的请求，服务端会拒绝服务。"
    res = trans(text, from_lang=origin_lang, to_lang=temp_lang)
    print(res)
    res = trans(res, from_lang=temp_lang, to_lang=origin_lang)
    print(res)
