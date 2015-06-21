from firebase import firebase
firebase = firebase.FirebaseApplication('https://wapi.firebaseio.com', None)
new_user = 'Ozgur Vatansever'

result = firebase.post('/users', new_user, name=None, connection=None, params={'print': 'pretty'}, headers={'X_FANCY_HEADER': 'VERY FANCY'})
print result
