from decimal import Decimal

from common.db_handler_pg import PgDbHandler
from common.yaml_handler import read_yaml
from config import config



db = PgDbHandler(ssh_address_or_host=("mnet.datatub.com", 56000),
                 ssh_username="hequan",
                 ssh_password=r"Dstory@888",
                 remote_bind_address=(
                 read_yaml(config.yaml_path)["db"]["address"], read_yaml(config.yaml_path)["db"]["port"]),
                 database=read_yaml(config.yaml_path)["db"]["database"],
                 user=read_yaml(config.yaml_path)["db"]["user"],
                 password=read_yaml(config.yaml_path)["db"]["password"])
"""
-- 消费百分比
select  consume_low_percent AS 消费低百分比, 
 consume_mid_low_percent 消费次低百分比,
 consume_mid_percent 消费中百分比,
  consume_mid_high_percent 消费次高百分比, 
  consume_high_percent 消费高百分比
FROM  statis_grid_pop_profile 
WHERE grid_id 
IN('8137615388318433280' )  
AND city_id ='1003638925920000049'
AND pop_type = 2

//* 1  工作人口
        //* 2  常住人口
        //* 3  居住人口
        //* 4  流动人口

select cn_name, tgi_name, percent_name from dim_indicator_selector where parent_id = (
    select id from dim_indicator_selector where cn_name = '居住社区档次' and selector_type = 'GRID'
);
"""

# 消费能力-消费水平-百分比-低
consume_percent_low_sql = db.query(
    "select consume_low_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-消费水平-百分比-次低
consume_percent_mid_low_sql = db.query(
    "select consume_mid_low_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) "
    "and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-消费水平-百分比-中
consume_percent_mid_sql = db.query(
    "select consume_mid_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) "
    "and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-消费水平-百分比-次高
consume_percent_mid_high_sql = db.query(
    "select consume_mid_high_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) "
    "and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-消费水平-百分比-高
consume_percent_high_sql = db.query(
    "select consume_high_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) "
    "and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-餐馆消费价格-百分比-50元以内
restaurant_consume_price_percent_lessthan50 = db.query(
    "select canteen_lt50_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) "
    "and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-居住社区房价-百分比-2000-4999
live_community_price_percent_2000_4999 = db.query("select house_2000_4999_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-居住社区档次-百分比-低
live_community_level_percent_low = db.query("select price_low_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-通勤方式-百分比-公交
commuterway_percent_bus = db.query("select traffic_public_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-是否有车-百分比-是
if_have_car_percent_yes = db.query("select car_yes_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-手机价格-百分比-0-1000
mobile_price_percent_0_1000 = db.query("select phone_0_1000_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-手机品牌-百分比-苹果
mobile_brand_percent_apple = db.query("select phone_brand_apple_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
# 消费能力-差旅常客-百分比-是
travel_visitor_percent_yes = db.query("select trip_yes_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
#消费能力-出国游-百分比-是
travel_abroad_percent_yes = db.query("select overseas_yes_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
#消费能力-旅游距离-百分比-无出游
travel_distance_percent_no = db.query("select travel_no_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
#消费能力-居住酒店档次-百分比-低
live_hotel_level_percent_low = db.query("select hotel_level_low_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
#消费能力-居住酒店价格-百分比-150以内
live_hotle_price_percent_lessthan150 = db.query("select hotel_lt150_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")





#人群画像-性别-百分比-男
gender_percent_male = db.query("select gender_male_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
#人群画像-年龄-百分比-0-17
age_percent_0_17 = db.query("select age_0_17_percent from  statis_grid_pop_profile where  grid_id  in('8137615284748484608' ) and city_id ='1003638925920000049'and pop_type = 1")
#人群画像-人生阶段-百分比-中学生
#人群画像-学历-百分比-小学
#人群画像-婚姻状态-百分比-未婚
#人群画像-子女年龄-百分比-0到2岁
#人群画像-到访偏好-百分比-基础设施
#人群画像-app偏好-百分比-健康