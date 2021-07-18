import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
    return res


def leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def check_api(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char).text
    return leaks_count(response, tail)


def main(args):
    for password in args:
        count = check_api(str(password))
        if count:
            print(f'Your password {password} was found {count} times.You should change this.')
        else:
            print(f'{password} was not found.')


main(sys.argv[1:])
