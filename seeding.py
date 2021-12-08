import json
import confparser
import requests



class Alert:
    def __init__(self):
        self.default = confparser.Default()

    def seed_msg(self, host, desc, ques):
        name = self.default.miner_name
        seed_message = "<font color='warning'>检测到异常，请相关同事注意.</font> \n" \
                       f">主     机 :  {host} \n" \
                       f">主 机 名 :  {desc} \n" \
                       f">所属集群 : {name} \n" \
                       f">问题描述 : {ques} \n"
        data = json.dumps({"msgtype": "markdown", "markdown": {"content": seed_message, "mentioned_list": ["@all"]}})
        r = requests.post(self.default.url, data, auth=('Content-Type', 'application/json'))
        return r.json()
