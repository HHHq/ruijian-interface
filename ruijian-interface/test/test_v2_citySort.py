"""
# @Time    : 2021/12/27 17:26
# @Author  : lcf
"""
import json, ddt, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler

excel_data = ExcelHandler(config.excel_path).read_sheet("睿见V2_城市甄选_按城市指标排序")
request_url = read_yaml(config.yaml_path)["env_ruijian"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestV2CitySort(unittest.TestCase):
    def setUp(self):
        self.cookie = MidWare().get_cookies()

    @ddt.data(*excel_data)
    def test_v2_citysort(self, info):
        logger.info("开始请求--->按城市指标排序接口-用例id_{}".format(info["case_id"]))
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    #params=json.loads(info["data"]),
                    # headers=json.loads(info["header"]),
                    cookies=self.cookie)
        logger.info("返回信息:{}".format(rsp))
        try:
            self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
            self.assertTrue(json.loads(info["expected"])["message"] == rsp["message"])
            self.assertTrue(json.loads(info["expected"])["success"] == rsp["success"])
            logger.info("城市筛选_按城市指标排序接口_测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("城市筛选_按城市指标排序接口_测试用例id_{}不通过".format(info["case_id"]))
            raise e
