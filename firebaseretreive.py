from firebase import firebase

firebase=firebase.FirebaseApplication("",None) #firebase data 링크
result=firebase.get('/pythondbtest-e851c/Customer','')
print(result)
