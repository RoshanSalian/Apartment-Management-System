# from urllib.parse import quote, unquote

# text = "cqwbi82!@#$?/[]%"
# print(text)
# text = quote(quote(text, safe = ''))
# print(text)
# text = unquote(unquote(text))
# print(text)

from datetime import datetime
today = datetime.today()

# year = today.year
# month = today.month

year = 1970
month = 1

monthNum = (year - 1970) * 12 + month

print(monthNum)

y = monthNum // 12 + 1970
m = monthNum % 12
if m == 0:
	m = 12
	y -= 1

print(y, m)