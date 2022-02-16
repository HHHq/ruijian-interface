"""
@Author:hq
"""
import json, ddt, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler

excel_data = ExcelHandler(config.excel_path).read_sheet("睿见V2_取消关注")
request_url = read_yaml(config.yaml_path)["env_ruijian"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestV2UserSignAreaDelete(unittest.TestCase):
    def setUp(self):
        try:
            self.cookie = MidWare().get_cookies()
            logger.info("成功获取cookie")
            self.signId = MidWare().user_sign_areasave()
        except Exception:
            logger.error("setup前置条件运行失败")

    @ddt.data(*excel_data)
    def test_v2_userSignAreaDelete(self, info):
        try:
            if "#id#" in info["data"]:
                info["data"] = info["data"].replace("#id#", self.signId)
        except Exception:
            logger.error("替换signid失败")
        logger.info("开始请求取消关注接口-用例id_{}".format(info["case_id"]))
        logger.info("请求头:{},请求参数:{}".format(info["header"], info["data"]))
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"]),
                    cookies=self.cookie)
        logger.info("返回信息:{}".format(rsp))
        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["message"] == rsp["message"])
            self.assertTrue(json.loads(info["expected"])["success"] == rsp["success"])
            logger.info("取消关注接口测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("取消关注接口测试用例id_{}不通过".format(info["case_id"]))
            raise e
