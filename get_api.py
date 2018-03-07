# ! /usr/bin/ python
# coding:utf-8
# author:wisdom_tree
# get most website api

import requests
import json
import sys
import time


# Censys API
def get_info(country,app,page,ip_list):
	Cen_Api_Url="https://www.censys.io/api/v1/search/ipv4"   #身份认证 UID和SECRET每次登陆都会改变
	UID="9e16f3d4-e0e4-4001-a45d-f11cc8896498"
	SECRET="XXXXXXXXXXX"

	if country=="null":   #提交查询数据
		data={"query":app,"page":page,"fields":["ip","protocols","location.country"]}
	else:
		data={"query":app+" location.country_code: "+country,"page":page,"fields":["ip","protocols","location.country"]}
	Cen_req=requests.post(Cen_Api_Url,data=json.dumps(data),auth=(UID,SECRET))	
	if Cen_req.status_code!=200:   #判断扫描是否结束
		print("End!!!!")
		sys.exit(1)

	result=Cen_req.json()
	for i in result["results"]:  #提取数据
		print(i["ip"],i["protocols"],i["location.country"])
		ip_list.write(i["ip"]+"\n")   #写入文件


if __name__ == '__main__':
	country=input("输入国际域名缩写(取消国家限制输入null):")
	app=input("请输入关键字：")
	top=int(input("输入扫描页数："))
	#search_type=input("输入ipv4或者websites:")
	ip_list=open("ip.txt","w+")
	page=1
	for page in range(1,100):
	# while page:
		try:
			get_info(country,app,page,ip_list)
			# page=page+1
		except Exception:
			#break
			# sys.exit("超过速率限制，请稍等")
			time.sleep(10)  #突破速率限制
			continue
	ip_list.close()

	ip_list=open("ip.txt","r")   #统计ip数量
	flag=0
	for i in ip_list:
		#print(i)
		flag=flag+1
	print(flag)
	ip_list.close()
