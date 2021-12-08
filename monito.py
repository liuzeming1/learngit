import socket
import time
import threading
import re
import confparser
import paramiko
import logset
import seeding

logger = logset.load_my_logging_cfg()
seed_ = seeding.Alert()
key_path = "/home/fil/.ssh/id_rsa"

class SSH:
    """实现一个上下文协议，以确保ssh连接被正常关闭"""

    def __init__(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def __enter__(self):
        return self._ssh

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ssh.close()


class Interval:
    def __init__(self):
        self.ml = confparser.MonitorInterval()

    @staticmethod
    def connect(ssh, ip, user):
        ssh.connect(hostname=ip, username=user, timeout=5,
                    key_filename=key_path)
        return ssh


class AdminAlert(Interval):
    """功能机的监控类"""

    def __init__(self):
        self.admin = confparser.Admin()
        self.user = self.admin.user
        super(AdminAlert, self).__init__()

    def window_post(self):
        """通过读取post日志，使用正则匹配到windowpostErr就发送告警"""
        ip, desc = self.admin.window
        with SSH() as ssh:
            post_err = re.compile(r'windowpostErr diIndex:\d+ failed \d+')
            while True:
                time.sleep(10)
                ssh = self.connect(ssh, ip, self.user)
                stdin, stdout, stderr = ssh.exec_command('tail -n 10  /mnt/lotus/log/manager.log')
                data = stdout.read()

                if data.decode('utf-8').endswith('success'):
                    sec = int(self.ml.post) * 60
                    time.sleep(sec)
                if post_err.search(data.decode('utf-8')):
                    seed_.seed_msg(host=ip, desc="WindowPost", ques=post_err.groups)
                    logger.error(post_err.groups)

    def pgc(self):
        """检查进程是否在线，显卡是否正常"""
        while True:
            for ip, desc in self.admin:
                with SSH() as ssh:
                    ssh = self.connect(ssh, ip, self.user)
                    # 检查进程数量
                    stdin, stdout, stderr = ssh.exec_command("ps aux | grep lotus | grep -v grep | wc -l")
                    count_nums = len(desc) + 1
                    real_nums = int(stdout.read().decode("utf-8"))
                    if count_nums > real_nums:
                        logger.error("{} Process exit, current process number is {}，"
                                     "The actual number of processes is{}".format(ip, real_nums, count_nums))
                        seed_.seed_msg(ip, desc, "进程退出，当前进程数为{}，实际进程数量为{}".format(real_nums, count_nums))
                    # 检查显卡
                    stdin, stdout, stderr = ssh.exec_command("nvidia-smi | grep GeForce | wc -l")
                    gc = int(stdout.read().decode("utf-8"))
                    if "miner" in desc and "lotus" in desc:
                        if stderr.read() or gc < 1:
                            logger.error("{} Abnormalities in the graphics card!")
                            seed_.seed_msg(ip, desc, "显卡异常，请及时查看")
            sec = int(self.ml.process) * 60
            time.sleep(sec)

    def lotus(self):
        """检查lotus空间"""
        ip_list = []
        t = self.admin.lotus
        if t:
            ip_list.append(t[0])
        for ip, desc in self.admin:
            if "lotus" in desc:
                ip_list.append(ip)
        while True:
            for ip in ip_list:
                with SSH() as ssh:
                    ssh = self.connect(ssh, ip, self.user)
                    stdin, stdout, stderr = ssh.exec_command("du -h -s --block-size=G "
                                                             "/mnt/lotus/.lotus/datastore"
                                                             "| cut -f 1")
                    use = stdout.read().decode("utf-8")
                    use, _ = use.split("G")
                    alert_space = self.ml.use_space

                    if int(use) > int(alert_space):
                        logger.error("Not enough disk space, currently used {}".format(use))
                        seed_.seed_msg(ip, "lotus", "链空间已使用{}G，请检查是否充足！".format(use))
            sec = int(self.ml.lotus) * 60
            time.sleep(sec)


class StoreAlert(Interval):
    def __init__(self):
        self.store = confparser.Store()
        self.user = self.store.user
        super(StoreAlert, self).__init__()

    @staticmethod
    def connect(ssh, ip, user):
        """Add the exception handling of catching connection timeout"""
        try:
            ssh.connect(hostname=ip, username=user, timeout=5,
                        key_filename=key_path)
            return ssh
        except socket.timeout:
            logger.error("{} Unable to connect".format(ip))
            seed_.seed_msg(ip, "store", "无法连接远程服务器，请及时查看!")

    def process(self):
        """Check if the storage process is online"""
        while True:
            for ip in self.store.ip_list:
                with SSH() as ssh:
                    ssh = self.connect(ssh, ip, self.user)
                    stdin, stdout, stderr = ssh.exec_command("ps aux | grep lotus | grep -v grep | wc -l")
                    real_nums = int(stdout.read().decode("utf-8"))
                    if real_nums < 1:
                        logger.error("{} Process exit, please check soon".format(ip))
                        seed_.seed_msg(ip, "store", "存储进程退出!")
            sec = int(self.ml.storage) * 60
            time.sleep(sec)

    def md_start(self):
        """Iterate through all storage to check if the RAID status of /proc/mdstat is normal"""
        while True:
            for ip in self.store.ip_list:
                with SSH() as ssh:
                    ssh = self.connect(ssh, ip, self.user)
                    stdin, stdout, stderr = ssh.exec_command("cat /proc/mdstat  | grep md | cut -d ' ' -f3")
                    status_list = stdout.readlines()
                    for status in status_list:
                        if self.user == "root":
                            if status.strip("\n") != "healthy":
                                logger.error("{} Storage RAID Is abnormal!".format(ip))
                                seed_.seed_msg(ip, "store", "存储RAID异常！")
                        else:
                            if status.strip("\n") != "active":
                                logger.error("{} Storage RAID Is abnormal!".format(ip))
                                seed_.seed_msg(ip, "store", "存储RAID异常！")
            sec = int(self.ml.lotus)
            time.sleep(sec)


def multi_thread():
    threads = []
    func_list = [admin.window_post, admin.pgc, admin.lotus, store.process, store.md_start]
    for func in func_list:
        threads.append(
            threading.Thread(target=func)
        )
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    admin = AdminAlert()
    store = StoreAlert()
    multi_thread()
