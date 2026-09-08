print("Hello , This is a password checker.")
password = str(input("Enter a password of at least 8 characters. : "))
a = 0 
Common_Passwords = ['12345678', 'password', 'password1', 'PASSWORD']
if len(password)<8 :
    print("Invalid password , your password should be of min. 8 characters. ")
elif password in Common_Passwords:
    print("Your password is not strong try to create new one.")
    
else:    
    if any(ch.isupper() for ch in password):
        a= a +1
    if any(ch.isdigit() for ch in password):
        a= a +1 
    if any(ch.islower() for ch in password):
        a= a +1
    if any(not ch.isalnum() for ch in password):
        a= a +1
   
    if ( a == 4 ):
        print( "Your password is strong." )
    elif (a == 3 ):
        print("Your password is good.")  
    elif (a == 2 ):
        print("Your password is weak.")
    else:
        print("Your password is very weak.")
        
