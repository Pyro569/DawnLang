import DawnLang

while True:
    command = input('DawnLang > ')
    result, error = DawnLang.run('<stdin>', command)

    if error:
        print(error.as_string())
    elif result:
        print(repr(result))
