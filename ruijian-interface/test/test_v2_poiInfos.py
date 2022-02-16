"""
@Author:hq
@Date 2021/12/1 14:28
"""


import json, ddt, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler

excel_data = ExcelHandler(config.excel_path).read_sheet("睿见V2_poi搜索")
request_url = read_yaml(config.yaml_path)["env_ruijian"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestV2PoiInfos(unittest.TestCase):
    def setUp(self):
        self.cookie = MidWare().get_cookies()
        self.query_id = MidWare().get_queryid()

    @ddt.data(*excel_data)
    def test_v2_poiInfos(self, info):
        if "#poi_id#" in info["data"]:
            info['data'] = info['data'].replace("#poi_id#",self.query_id)
        logger.info("开始请求poi搜索接口-用例id_{}".format(info["case_id"]))
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
            logger.info("poi搜索接口测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("poi搜索接口测试用例id_{}不通过".format(info["case_id"]))
            raise e
