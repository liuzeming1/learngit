import os
import configparser
import logging
import logset


def _load_conf():
    conf_dir = os.path.dirname(os.path.abspath(__file__))
    conf_file = 'config.cfg'
    conf_path = os.path.join(conf_dir, conf_file)
    cf = configparser.ConfigParser(allow_no_value=True)
    cf.read(conf_path, encoding='utf-8')
    return cf


# def logout():
#     bar = logging.getLogger('bar')
#     return bar
logger = logset.load_my_logging_cfg()

class ReadConfig:
    """
    Reading configuration Files
    Get configuration items by instantiating the specified section and calling get_conf
    """
    _cf = _load_conf()
    _logger = logger

    def __init__(self, section):
        self._section = section

    def _user(self):
        """
        Convert the format of admin_ip and store_ip.
        admin_ip
            :return: -> ['user', {'ipaddress': ['Description'],}]
        store_ip
            :return: -> ['user', 'ipaddress',]
        """
        user = ReadConfig._cf.get(self._section, "user")
        conf_list = [user]
        ip_desc = {}
        for i in ReadConfig._cf[self._section].items():
            element, _ = i
            element = element.split()
            if element[0] != 'user' and len(element) == 1:
                conf_list.append(element[0])
                ReadConfig._logger.info("Monitoring of {} will start soon, Storage Object".format(element[0]))
            else:
                if len(element) != 1:
                    ip = element[0]
                    fc = element[1:]
                    ip_desc.update({ip: fc})
                    ReadConfig._logger.info("Monitoring of {} will start soon, Function Description: {}".format(ip, fc))
        if len(ip_desc) != 0:
            conf_list.append(ip_desc)
        return conf_list

    def get_items_conf(self, get_opt, log_desc=None):
        """
        get_opt: Get configuration items
        log_desc: Log description document
        :param get_opt: Str -> : Name of the option to get.
        :param log_desc: Str -> : The description character of the obtained configuration item.
        :return: For the options of the default configuration items
        """
        conf = ReadConfig._cf.get(self._section, get_opt)
        if log_desc:
            ReadConfig._logger.info("{}: [{!r}]".format(log_desc, conf))
        return str(conf)

    def get_monitor_interval(self, get_opt):
        """
        Get the monitoring interval time in the configuration.
        :param get_opt:
        :return:
        """
        conf = ReadConfig._cf.get(self._section, get_opt)
        return int(conf)

    def get_conf(self):
        return self._user()


class Default:
    def __init__(self):
        self._defaults = ReadConfig("defaults")

    @property
    def url(self):
        return self._defaults.get_items_conf(get_opt="wx_url", log_desc="Acquired alarm address")

    @property
    def miner_id(self):
        return self._defaults.get_items_conf(get_opt="miner_id", log_desc="Acquired Miner ID")

    @property
    def miner_name(self):
        return self._defaults.get_items_conf(get_opt="miner_name", log_desc="Acquired Miner Name")

    @property
    def forks(self):
        return self._defaults.get_items_conf(get_opt="forks")


class Admin:
    def __init__(self):
        self._admin = ReadConfig("admin").get_conf()
        self._ad = [self.miner, self.window, self.winning, self.lotus]

    def _reduction(self):
        dict_ = {"miner": None, "window": None, "winning": None, "lotus": None}
        for ip, desc in self._admin[1].items():
            desc = desc[0].split(",")
            main_func = desc[0]

            dict_.update({main_func: (ip, desc[1:])})
        return dict_

    @property
    def user(self):
        return self._admin[0]

    @property
    def miner(self):
        dict_ = self._reduction()
        return dict_["miner"]

    @property
    def lotus(self):
        dict_ = self._reduction()
        return dict_["lotus"]

    @property
    def window(self):
        dict_ = self._reduction()
        return dict_["window"]

    @property
    def winning(self):
        dict_ = self._reduction()
        return dict_["winning"]

    def __iter__(self):
        for i in self._ad:
            if i is not None:
                yield i


class Store:
    def __init__(self):
        self._store = ReadConfig("store").get_conf()

    @property
    def user(self):
        return self._store[0]

    @property
    def ip_list(self):
        return self._store[1:]


class MonitorInterval:
    def __init__(self):
        self.monitor_interval = ReadConfig("monitor_interval")

    @property
    def post(self):
        return self.monitor_interval.get_items_conf(get_opt="val_post")

    @property
    def storage(self):
        return self.monitor_interval.get_items_conf(get_opt="val_storage")

    @property
    def lotus(self):
        return self.monitor_interval.get_items_conf(get_opt="val_lotus")

    @property
    def process(self):
        return self.monitor_interval.get_items_conf(get_opt="val_process")

    @property
    def use_space(self):
        return self.monitor_interval.get_items_conf(get_opt="alert_space")


def test():
    default = Default()
    admin = Admin()
    store = Store()
    monito = MonitorInterval()
    print(admin.user)
    print(admin.lotus)
    print(admin.window)
    print(admin.winning)


if __name__ == "__main__":
    print("开始测试参数是否被正常解析！")
    test()