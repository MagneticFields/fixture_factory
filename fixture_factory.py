import sys
import random
import os
import datetime
import json


def load_files():
    """
    Loading files from the same directory of the script. There are 3 txt files and their names are self explanatory.
    It also closes the files after loading so you can edit the files.
    """
    directory = os.getcwd()
    # Load the names
    with open(directory + '/names.txt') as names:
        name_list = names.read().splitlines()
        names.close()
    # Load the last names
    with open(directory + '/last_names.txt') as last_names:
        last_name_list = last_names.read().splitlines()
        last_names.close()
    # Load the email providers
    with open(directory + ('/email.txt')) as mails:
        mail_list = mails.read().splitlines()
        mails.close()
    return name_list, last_name_list, mail_list

model_name = input('Enter the name of the model: ')
num_of_items = int(input('How many items do you want?: '))
pk = int(input('Enter the starting primary key: '))

# if len(sys.argv) > 1:
#     print('there are extra arguments in command line')

#     if '-n' in sys.argv:
#         item_index = sys.argv.index('-n') + 1
#         num_of_items = sys.argv[item_index]
#         print(f'You want {num_of_items} items.')
#     elif '--number' in sys.argv:
#         item_index = sys.argv.index('--number') + 1
#         num_of_items = sys.argv[item_index]
#     else:
#         num_of_items = int(input('How many items do you want?: '))
#     if '--pk' in sys.argv:
#         pk_index = sys.argv.index('--pk') + 1
#         pk = sys.argv[pk_index]
#     else:
#         pk = int(input('Enter the starting primary key: '))
name_list, last_name_list, mail_list = load_files()

def create_item(pk):
    """
    This creates a single python dict with random name, last name, ıusername and email.
    Username creating scheme is first name + first letter of the last name.
    Note that passwords are all same 'testing1234' django hashes passwords with pbkdf2 sha250 with random salt and 180000 iterations.
    input: int
    return: dict
    """

    name = random.choice(name_list)
    last_name = random.choice(last_name_list)
    username = name + last_name[0]
    username = username.lower()
    email = username + '@' + random.choice(mail_list)
    item = {}
    item['model'] = 'users.' + model_name
    item['pk'] = pk
    item['fields'] = {}
    item['fields']['password'] = 'pbkdf2_sha256$180000$UHsXnV8XFT8M$5n9TYOYZfiHk2NPAU4hZR6P5pyiDz4Cku7q4xo9njNk='
    item['fields']['last_login'] = None
    item['fields']['is_superuser'] = False
    item['fields']['username'] = username # usernames should be lower
    item['fields']['first_name'] = name
    item['fields']['last_name'] = last_name
    item['fields']['email'] = email
    item['fields']['is_staff'] = False
    item['fields']['is_Active'] = True
    item['fields']['date_joined'] = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%SZ')
    item['fields']['groups'] = []
    item['fields']['user_premissions'] = []



    return item

def generate_pk(pk):
    pk = [pk for pk in range(int(num_of_items))]
    yield pk

items = []
for i in range(int(num_of_items)):
    items.append(create_item(pk))
    pk += 1

with open("data_fixtures.json", 'w') as write_file:
    json.dump(items, write_file)


