#!/usr/bin/python
# -*- coding: utf-8 -*
""" 收集用例，运行用例，生成测试报告的主程序"""
import os, unittest,HTMLTestRunner
from common.send_email import SendEmail
from datetime import datetime
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare

logger = MidWare.logger
# test目录的路径
case_path = os.path.join(config.root_path, "test")
# reports目录的路径
report_path = os.path.join(config.root_path, "reports")
loader = unittest.TestLoader()
logger.info("开始收集测试集")
# 收集test目录下所有test开头的模块作为测试集
suites = loader.discover(case_path)
# 测试报告文件名格式
ts = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
report_filename = 'report-{}.html'.format(ts)
# 测试报告文件路径
report_path = os.path.join(report_path, report_filename)

logger.info("开始运行测试用例")
with open(report_path, mode='wb') as f:
    runner = HTMLTestRunner.HTMLTestRunner(f, title='睿见接口测试报告', description='自定义描述')
    runner.run(suites)
logger.info("测试用例run完毕")
# 发送邮件
email_handler = SendEmail(smtpserver="smtp.qq.com",
                          user="485867062@qq.com",
                          password="edvwffwfpwyrcbdj",
                          sender="485867062@qq.com",
                          receiver=read_yaml(config.yaml_path)["email_receiver"],
                          report_path=report_path)
email_handler.send_email()

