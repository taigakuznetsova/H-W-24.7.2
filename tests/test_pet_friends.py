from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Ted', animal_type='goldfish', age='1', pet_photo='images/goldfish.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet_info():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Tail", "iguana", "3", "images/iguana.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Izzy', animal_type='lizard', age=4):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pet")


def test_successful_add_new_pet_simple_with_valid_data(name='Iggy', animal_type='iguana', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_pet_with_valid_data(pet_photo='images/iguana.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__),pet_photo)
    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        assert status == 200

    else:
        raise Exception("Oh no")


def test_unsuccessful_add_new_pet(name=' ', animal_type='giraffe', age='1', pet_photo='images/giraffe.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert type(result['name']) == str
    # Bug 001


def test_unsuccessful_add_new_pet_simple(name='Dorothy', animal_type='sheep', age='-1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name
    #Bug 002


def test_unsuccessful_add_new_pet_simple_with_invalid_data(name='Poppy', animal_type='guinea pig', age='two'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name
#Bug 003


def test_unsuccessful_update_self_pet_info(name='Poppy', animal_type='1', age=2):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 400
        assert result['name'] == name
    else:
        raise Exception("There is no my pet")
#Bug 004


def test_unsuccessful_add_photo_of_pet(pet_photo='images/flashcards.pdf'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 400

    else:
        raise Exception("Oh no")
#Bug 005


def test_unsuccessful_add_new_pet_simple_with_invalid_name(name='15', animal_type='cat', age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] == name
 #Bug 006


def test_unsuccessful_get_api_key_for_invalid_user(email='ozzy@mail.ru', password='15380GhO'):
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_unsuccessful_add_new_pet_with_invalid_photo(name='Fluffy', animal_type='cat', age='3', pet_photo='images/cat'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    try:
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        assert status == 200

    except FileNotFoundError:
        assert True
    else:
        assert False
