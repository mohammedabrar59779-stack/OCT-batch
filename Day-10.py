numbers=[100,20,30]
numbers.append(40)
print(numbers)



numbers=[100,20,30]
numbers.extend([30,40])
print(numbers)


list=[10,20,5,True,1+3j,"python"]
print(list)


list=[10, [20 , 30, 40],(50,60,70),{9,10,10},{1:'x',2:'y'}]
print(list)


list=[10, [20,30,40],(50,60,70),{9,10},{1:'x',2:'y'}]
print(list[1])[20,30,40]
print(list[1][1])
print(list[2]),(50,60,70)