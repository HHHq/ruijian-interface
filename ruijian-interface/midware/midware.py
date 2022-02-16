import requests, json, random
from common.log_output import log_output
from common.yaml_handler import read_yaml
from config import config
from common.requests_handler import visit


class MidWare():
    logger = log_output(filename=config.log_path)

    # 获取cookie
    def get_cookies(self):
        response = requests.post(url=read_yaml(config.yaml_path)["env_ruijian"]["url"]+"/account/login",
                                 data={"emailOrPhone": read_yaml(config.yaml_path)["env_ruijian"]["login_account"],
                                       "password": read_yaml(config.yaml_path)["env_ruijian"]["password"]},
                                 headers={"content-type": "application/x-www-form-urlencoded"}
                                 )
        cookie = response.cookies.get_dict()

        return cookie

    # 调用添加关注接口，获取返回的signid。以便取消关注/评估接口的入参调用
    def user_sign_areasave(self):
        # url = "https://channel.matrix.datastory.com.cn/serv/v2/openApi/m2Af/userSignAreaSave"
        try:
            response = visit(method="post",
                             url=read_yaml(config.yaml_path)["env_ruijian"]["url"]+"/serv/v2/openApi/m2Af/userSignAreaSave",
                             json={"relationType": "POI", "areaType": "网点", "shapeType": "圆形", "isPoi": 1,
                                   "poiInfo": {"id": "8148776635522359310", "cityId": "1003638925920000049",
                                               "centerLoc": {"type": "Point", "coordinates": [113.379094, 23.119897]},
                                               "categoryId": "1003638925970000020", "name": "麦德龙(天河商场店)",
                                               "address": "广东省广州市天河区黄埔大道中351号近科韵路地铁站", "signId": None, "signStatus": 0,
                                               "aoiId": None, "boundary": None, "gridId": "8137615312581885952",
                                               "rootCategoryName": "购物服务", "poiDetailExtraList": None},
                                   "relationId": "8148776635522359310", "cityId": "1003638925920000049",
                                   "centerLoc": {"longitude": 113.379094, "latitude": 23.119897},
                                   "name": "麦德龙(天河商场店)-{}".format(random.randint(1, 100000000))},
                             cookies=self.get_cookies())
            signid = response["data"]["signId"]
            return signid
        except Exception:
            MidWare.logger.error("获取signid失败")

    # 返回queryid，以便后续的poiinfo接口入参调用
    def get_queryid(self):
        res = visit(method='post',
                    url=read_yaml(config.yaml_path)['env_ruijian']['url'] + "/serv/v2/openApi/m2Af/poiQuerySave",
                    json={"cityId": "1003638925920000049",
                          "filter": [{"name": "7天优品酒店", "categoryId": "1003638925950001274", "attribute": []}]},
                    cookies=self.get_cookies()
                    )
        query_id = res["data"]["queryId"]
        return query_id

    # 四舍五入保留两位小数
    def data_rounded(self, number):

        if str(number).split(".")[1][2] >= "5":
            data = str(number).split(".")[0] + "." + str(int(str(number).split(".")[1][:2]) + 1)
        else:
            data = str(number).split(".")[0] + "." + str(number).split(".")[1][:2]
        return data


if __name__ == '__main__':

    print(MidWare().get_cookies())
    # url = read_yaml(config.yaml_path)["env_ruijian"]["url"]
    # data = {"emailOrPhone": read_yaml(config.yaml_path)["env_ruijian"]["login_account"],
    #         "password": read_yaml(config.yaml_path)["env_ruijian"]["password"]}


