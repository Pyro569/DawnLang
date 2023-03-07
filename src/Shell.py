import DawnLang
import readline

while True:
    command = input('DawnLang > ')
    result, error = DawnLang.run('<stdin>', command)

    if error:
        print(error.as_string())
    elif result:
        print(result)
