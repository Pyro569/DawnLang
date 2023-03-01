import DawnLang

while True:
    command = input('DawnLang > ')
    result, error = DawnLang.run('<stdin>', command)
    
    if error: print(error.turnString())
    else: print(result)