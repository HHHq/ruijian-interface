"""
@Author:hq
@Date 2022/1/18 15:02
"""

import json, ddt, unittest
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common import query_sql_data

excel_data = ExcelHandler(config.excel_path).read_sheet("睿见V2_栅格消费能力")
request_url = read_yaml(config.yaml_path)["env_ruijian"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestV2GridDetailPopProfile(unittest.TestCase):
    def setUp(self):
        self.cookie = MidWare().get_cookies()

    @ddt.data(*excel_data)
    def test_v2_gridDetailPopProfile(self, info):

        if info["interface"] == "栅格-消费能力":
            logger.info("开始请求--->栅格消费能力接口-用例id_{}".format(info["case_id"]))
            rsp = visit(method=info["method"],
                        url=request_url + info["url"],
                        json=json.loads(info["data"]),
                        headers=json.loads(info["header"]),
                        cookies=self.cookie)
            logger.info("返回信息:{}".format(rsp))
            try:
                self.assertTrue(json.loads(info["expected"])["message"] == rsp["message"])
                self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
                self.assertTrue(json.loads(info["expected"])["success"] == rsp["success"])
                # 消费能力-消费水平-百分比-低
                self.assertTrue(
                    float(query_sql_data.consume_percent_low_sql[0]) == rsp["data"][0]["value"]["percent"][0]["value"])
                # 消费能力-消费水平-百分比-次低
                self.assertTrue(
                    float(query_sql_data.consume_percent_mid_low_sql[0]) == rsp["data"][0]["value"]["percent"][1][
                        "value"])
                # 消费能力-消费水平-百分比-中
                self.assertTrue(
                    float(query_sql_data.consume_percent_mid_sql[0]) == rsp["data"][0]["value"]["percent"][2]["value"])
                # 消费能力-消费水平-百分比-次高
                self.assertTrue(
                    float(query_sql_data.consume_percent_mid_high_sql[0]) == rsp["data"][0]["value"]["percent"][3][
                        "value"])
                # 消费能力-消费水平-百分比-高
                self.assertTrue(
                    float(query_sql_data.consume_percent_high_sql[0]) == rsp["data"][0]["value"]["percent"][4]["value"])
                # 消费能力-餐馆消费价格-百分比-50元以内
                self.assertTrue(float(query_sql_data.restaurant_consume_price_percent_lessthan50[0]) ==
                                rsp["data"][1]["value"]["percent"][0]["value"])
                # 消费能力-居住社区房价-百分比-2000-4999
                self.assertTrue(float(query_sql_data.live_community_price_percent_2000_4999[0]) ==
                                rsp["data"][2]["value"]["percent"][0]["value"])
                # 消费能力-居住社区档次-百分比-低
                self.assertTrue(float(query_sql_data.live_community_level_percent_low[0]) ==
                                rsp["data"][3]["value"]["percent"][0]["value"])
                # 消费能力-通勤方式-百分比-公交
                self.assertTrue(float(query_sql_data.commuterway_percent_bus[0]) ==
                                rsp["data"][4]["value"]["percent"][0]["value"])
                # 消费能力-是否有车-百分比-是
                self.assertTrue(float(query_sql_data.if_have_car_percent_yes[0]) ==
                                rsp["data"][5]["value"]["percent"][0]["value"])
                # 消费能力-手机价格-百分比-0-1000
                self.assertTrue(float(query_sql_data.mobile_price_percent_0_1000[0]) ==
                                rsp["data"][6]["value"]["percent"][0]["value"])
                # 消费能力-手机品牌-百分比-苹果
                self.assertTrue(float(query_sql_data.mobile_brand_percent_apple[0]) ==
                                rsp["data"][7]["value"]["percent"][0]["value"])
                # 消费能力-差旅常客-百分比-是
                self.assertTrue(float(query_sql_data.travel_visitor_percent_yes[0]) ==
                                rsp["data"][8]["value"]["percent"][0]["value"])
                # 消费能力-出国游-百分比-是
                self.assertTrue(float(query_sql_data.travel_abroad_percent_yes[0]) ==
                                rsp["data"][9]["value"]["percent"][0]["value"])
                # 消费能力-旅游距离-百分比-无出游
                self.assertTrue(float(query_sql_data.travel_distance_percent_no[0]) ==
                                rsp["data"][10]["value"]["percent"][0]["value"])
                # 消费能力-居住酒店档次-百分比-低
                self.assertTrue(float(query_sql_data.live_hotel_level_percent_low[0]) ==
                                rsp["data"][11]["value"]["percent"][0]["value"])
                # 消费能力-居住酒店价格-百分比-150以内
                self.assertTrue(float(query_sql_data.live_hotle_price_percent_lessthan150[0]) ==
                                rsp["data"][12]["value"]["percent"][0]["value"])
                logger.info("栅格消费能力接口_测试用例id_{}通过".format(info["case_id"]))
            except Exception as e:
                logger.error("栅格消费能力接口_测试用例id_{}不通过".format(info["case_id"]))
                raise e

        if info["interface"] == "栅格-人群画像" :
            logger.info("开始请求--->栅格人群画像接口-用例id_{}".format(info["case_id"]))
            rsp = visit(method=info["method"],
                        url=request_url + info["url"],
                        json=json.loads(info["data"]),
                        headers=json.loads(info["header"]),
                        cookies=self.cookie)
            try:
                self.assertTrue(json.loads(info["expected"])["message"] == rsp["message"])
                self.assertTrue(json.loads(info["expected"])["code"] == rsp["code"])
                self.assertTrue(json.loads(info["expected"])["success"] == rsp["success"])
                # 人群画像-性别-百分比-男
                self.assertTrue(float(query_sql_data.gender_percent_male[0]) ==
                            rsp["data"][0]["value"]["percent"][0]["value"])
                # 人群画像-年龄-百分比-0-17
                self.assertTrue(float(query_sql_data.age_percent_0_17[0]) ==
                            rsp["data"][1]["value"]["percent"][0]["value"])
                logger.info("栅格人群画像接口_测试用例id_{}通过".format(info["case_id"]))
            except Exception as e:
                logger.error("栅格人群画像接口_测试用例id_{}不通过".format(info["case_id"]))
                raise e
