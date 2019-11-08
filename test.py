from urllib.parse import quote, unquote

text = "cqwbi82!@#$?/[]%"
print(text)
text = quote(quote(text, safe = ''))
print(text)
text = unquote(unquote(text))
print(text)