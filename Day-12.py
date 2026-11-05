sum=0
for x in [10,20,30]:
    sum=sum+x
print(sum)


mul=1
for x in [10,20,30]:
    mul=mul*x
print(mul)


count=0 
for x in [10,20,30]:
    count=count+1
print(count)

nums=[2,5,9,1,9]
n=len(nums)
for x in range(n):
  for j in range(n-1):
      if nums[j]>nums[j+1]:
        nums[j] ,nums[j+1]=nums[j+1],nums[j]
print(nums)