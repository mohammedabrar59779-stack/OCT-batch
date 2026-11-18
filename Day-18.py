a={"x":1,"y":2}
b={"y":20,"z":30}
a.update(b)




d={"a":1,"b:":2,"c":3,"d":4}
x=d.pop("b")
del d['c']
print(x)
print(d)


d={"a":1,"b":2}
print("a" in d)
print(2 in d)
print(2 in d.values())


d={"a":1,"b":2,"c":3}
for k, v in d.items():
   print(k,v)