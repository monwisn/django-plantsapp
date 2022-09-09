#
#     # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     #
#     # if x_forwarded_for:
#     #     ip = x_forwarded_for.split(',')[0]
#     # else:
#     #     ip = request.META.get('REMOTE_ADDR')
#
#     # print(geolocation)
#
#     # return render(request, 'hobby/location.html', {'ip': ip, 'geo': geo})
#
#     # url = "https://ip-location5.p.rapidapi.com/get_geo_info"
#     # payload = "ip=172.19.128.1"
#     #
#     # headers = {"content-type": "application/x-www-form-urlencoded",
#     #            "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
#     #            "X-RapidAPI-Host": "ip-location5.p.rapidapi.com"
#     #            }
#     #
#     # response = requests.request("POST", url, data=payload, headers=headers)
#     # print(response.text)
#     #
#     # return response
#
#
# # import requests
# #
# # url = "https://ip-geo-location.p.rapidapi.com/ip/check"
# #
# # querystring = {"format": "json"}
# #
# # headers = {
# # 	"X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
# # 	"X-RapidAPI-Host": "ip-geo-location.p.rapidapi.com"
# # }
# #
# # response = requests.request("GET", url, headers=headers, params=querystring)
# #
# # print(response.text)
#
#
# # url = "https://ronreiter-meme-generator.p.rapidapi.com/meme"
# #
# # querystring = {"meme": "Condescending-Wonka", "bottom": "Bottom Text", "top": "Top Text", "font": "Impact",
# #                "font_size": "50"}
# #
# # headers = {
# #     "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
# #     "X-RapidAPI-Host": "ronreiter-meme-generator.p.rapidapi.com"
# # }
# #
# # response = requests.request("GET", url, headers=headers, params=querystring)
# #
# # print(response.text)
#
# import requests
#
#
#
# def house_plants(request):
#
#         url = requests.get("https://house-plants.p.rapidapi.com/common/coralberry").json()
#
#         headers = {
#             "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
#             "X-RapidAPI-Host": "house-plants.p.rapidapi.com"
# }
#
# response = requests.request("GET", url, headers=headers)
#
# print(response.text)
