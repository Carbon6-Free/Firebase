from firebase import firebase

firebase = firebase.FirebaseApplication("", None) #firebase data 링크

firebase.put('/pythondbtest-d3f23/Customer/-NvMqieTfL9CYOwSJF6b','Name', 'Bob')
print("Record Updated")
