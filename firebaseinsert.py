from firebase import firebase

firebase=firebase.FirebaseApplication("",None) #firebase data 링크
data={
    'Name':'John Doe',
    'Email':'John@gmail.com',
    'Phone':4407904449
}

result=firebase.post('/pythondbtest-e851c/Customer', data)
print(result)
