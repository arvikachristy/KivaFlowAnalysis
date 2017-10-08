""" This is the schema module.

This is where you would transform Kiva data into data that means something to you. I.e. into models that your application understands.

I'm doing this serialisation manually for now because it's easy but you might use a library like marshmallow if you want a bit more flexibility/power.

https://marshmallow.readthedocs.io/en/latest/

"""

def model(data):
    return {
        'lenderId': data['id'],
        'lenderName': data['name'],
        'isImportantLender': True if data['loan_amount'] > 2000 else False,
    }

def transform(data):
    return map(model, data)

