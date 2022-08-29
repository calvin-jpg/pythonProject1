__author__ = 'dev'
#Finding the amount of seconds in a month

print(30*24*3600)
#Finding the factorial of a number
print((4-0)*(4-1)*(4-2)*(4-3))
#Float Operations
print(1+2+3+4.0+5)
#Exponentiations on python
print(((3**4)**(1/2))**(1/2))
#Floor Division
print(10//4)
#Reminder of a number
print(20 % 6)
print(1.25 % 0.5)
print(7%(5//2))
print(1+4*3)
#Strings by single and double quotations
print("hello, hello")
print('my name is, Butcher')
#Newlines and Multiline text
print('and Brian is my mother\'s son, he\'s not an angel. He\'s a very naughty boy!')
print('and i\'m learning how to live with him \nalthough he really gives me a tough time')
print("""this
is a
multiline
text""")
#Concatenation : Adding of strings
print("Spam" + " emails")
print('are bad for ' + 'business')
print("i love you \n" * 10 + 'so much')
print(4 * '<3')
#alternative one of the problem given
x = 3
y = 4
sum = x+y
if(sum> 8):
    print("the sum of x and y is greater than eight")
elif(sum< 8):
    print("the sum of x and y is less than eight")
else:
    print("the sum of x and y is essentially the same as eight")
#Alternative two of the problem given
def sumofAandB(a,b):
    sum = a+b
    if(sum> 5):
        print("the number is greater than five")
    elif(sum< 5):
        print("the number is less than five")
    else:
        print("the number is essentially the same as five")
sumofAandB(4,0)
#printing the name and age of a person
def printnameandage(name, age):
    print("your name is:", name,"\nand your age is:", age, "years old")
printnameandage("Calvin Makawia", 24)
#determining data types of different variables
g = 91
h = True
print('g is {}'.format(g))
print(type(g))
print('h is {}'.format(h))
print(type(h))




