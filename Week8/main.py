def simple_interest(p,r,t):
  return (p*r*t)/100

p=int(input("What's the principle amount="))
t=int(input("What's the time="))
r=int(input("What's the rate="))
ans=simple_interest(p,r,t)
print("Simple Interest is ",ans) 
#simple interest