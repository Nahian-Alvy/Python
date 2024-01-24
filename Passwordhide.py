message = 'It\s Getting Started'

#print(help(str)) #shows str function opertions
print(message)
username = input('Whats your Name?')
password = input('Enter Your PassWord\n')


length_of_Pass = len(password)
hidden_password = '*' * length_of_Pass 

print(f'{username} Greetings Your password is {length_of_Pass} digit and {hidden_password}')

                 