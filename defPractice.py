def json_get():
   import json
   f = open(r"C:\Users\mengs\Desktop\1000T.json")
   json_data = json.load(f)
   return (json_data)

def add(num1,num2):
   ans = num1 + num2 
   return (ans)

def message(greeting,name):
    ansMessage = greeting + name 
    return(greeting,name,ansMessage)

#def for json_get 
temp = json_get()
print(temp)

#def for add
temp1 = add(2,5)
print(temp1)

#def for message
temp3 = message("Hello"," Takeshi")
print(temp3[0])
print(temp3[1])
print(temp3[2])