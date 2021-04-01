import json
import codecs
import os.path
from instagram_private_api import Client, ClientError, ClientLoginError, ClientCookieExpiredError, ClientLoginRequiredError

settings_file_path = ".instauth"

def to_json(python_object):
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': codecs.encode(python_object, 'base64').decode()}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def from_json(json_object):
    if '__class__' in json_object and json_object['__class__'] == 'bytes':
        return codecs.decode(json_object['__value__'].encode(), 'base64')
    return json_object


def onlogin_callback(api, new_settings_file):
    cache_settings = api.settings
    with open(new_settings_file, 'w') as outfile:
        json.dump(cache_settings, outfile, default=to_json)
        print('SAVED: {0!s}'.format(new_settings_file))


def get_settings():
    with open(settings_file_path) as file_data:
        cached_settings = json.load(file_data, object_hook=from_json)
        return cached_settings

def get_client(username, password) -> Client:
    if os.path.isfile(settings_file_path):
        print(f'Reusing settings: {settings_file_path}')
        device_id = get_settings().get('device_id')

        return Client(username, password, settings=get_settings())

    return Client(
        username,
        password,
        on_login=lambda x: onlogin_callback(x, settings_file_path)
    )


def login(username, password):

    device_id = None
    try:
        return get_client(username, password)

    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))

        # Login expired
        # Do relogin but use default ua, keys and such
        return Client(
            username, password,
            device_id=device_id,
            on_login=lambda x: onlogin_callback(x, settings_file_path)
        )

    except ClientLoginError as e:
        print('ClientLoginError {0!s}'.format(e))
        exit(1)
    except ClientError as e:
        print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
        exit(1)
    except Exception as e:
        print('Unexpected Exception: {0!s}'.format(e))
        exit(1)