#python program to check whether a number is pallindrome or not
n=int(input("Enter a number"))
temp=n
rev=0
while(n>0):
    digit=n%10
    rev=rev*10+digit
    n=n//10
if(temp==rev):
    print("Number is a pallindrome!")
else:
    print("Number is not a pallindrome!")