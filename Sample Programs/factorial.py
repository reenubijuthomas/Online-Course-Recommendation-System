#python program to find factorial of a number
n=int(input("Enter number"))
res=1
for i in range(1,n+1):
    res=res*i
print("Factorial of ",n,"is",res)