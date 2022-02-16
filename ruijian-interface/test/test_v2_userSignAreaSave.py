"""
@Author:hq
@Date 2021/11/16 17:38
"""
import json, ddt, unittest,random
from config import config
from common.yaml_handler import read_yaml
from midware.midware import MidWare
from common.requests_handler import visit
from common.excel import ExcelHandler
from common.db_handler_pg import PgDbHandler


excel_data = ExcelHandler(config.excel_path).read_sheet("睿见V2_添加关注")
request_url = read_yaml(config.yaml_path)["env_ruijian"]["url"]
logger = MidWare.logger


@ddt.ddt
class TestV2UserSignAreaSave(unittest.TestCase):
    def setUp(self):
        self.cookie = MidWare().get_cookies()

    """
    请求成功后，需要update表map_user_sign_area和map_user_sign_area_relation的字段is_del=1取消关注。因为请求数据是写死的，
    点位是已关注的状态，后续再用同样的数据请求，会断言失败
    """
    def tearDown(self):
        db = PgDbHandler(ssh_address_or_host=("mnet.datatub.com", 56000),
                         ssh_username="hequan",
                         ssh_password=r"Dstory@888",
                         remote_bind_address=(read_yaml(config.yaml_path)["db"]["address"],read_yaml(config.yaml_path)["db"]["port"]),
                         database=read_yaml(config.yaml_path)["db"]["database"],
                         user=read_yaml(config.yaml_path)["db"]["user"],
                         password=read_yaml(config.yaml_path)["db"]["password"])
        db_sql1 = "update map_user_sign_area set is_del=1 where name='{}'".format(
            json.loads(excel_data[0]["data"])["name"])
        db_sql2 = "update map_user_sign_area_relation set is_del=1 where sign_id in(select id from map_user_sign_area where name='{}')" \
            .format(json.loads(excel_data[0]["data"])["name"])
        db.update(db_sql1,db_sql2)

    # @unittest.skip("1")
    @ddt.data(*excel_data)
    def test_v2userSignAreaSave(self, info):

        if "#id#" in info["data"]:
            info["data"] = info["data"].replace("#id#",str(random.randint(1,1000000000)))
        logger.info("开始请求添加关注接口-用例id_{}".format(info["case_id"]))
        logger.info("请求头:{},请求参数:{}".format(info["header"], info["data"]))
        rsp = visit(method=info["method"],
                    url=request_url + info["url"],
                    json=json.loads(info["data"]),
                    headers=json.loads(info["header"]),
                    cookies=self.cookie)
        logger.info("返回信息:{}".format(rsp))
        try:
            self.assertTrue(json.loads(info["expected"])["code"]== rsp["code"])
            self.assertTrue(json.loads(info["expected"])["message"] == rsp["message"])
            logger.info("添加关注接口测试用例id_{}通过".format(info["case_id"]))
        except Exception as e:
            logger.error("添加关注接口测试用例id_{}不通过".format(info["case_id"]))
            raise e
