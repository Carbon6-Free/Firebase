from firebase import firebase

firebase = firebase.FirebaseApplication("", None) #firebase data 링크

firebase.delete('/pythondbtest-d3f23/Customer/','-NvMqieTfL9CYOwSJF6b')
print("Record Deleted")
