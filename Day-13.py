import time
list=[1,2,23,55]
start=time.time()
print(23 in list)
end=time.time()
print(end-start)

import time
tuple=(1,2,23,55)
start=time.time()
print(23 in tuple)
end=time.time()
print(end-start)

import sys
lst=[1,2,23,55]
p=sys.getsizeof(lst)
print(p)


import sys
tup=[1,2,23,55]
x=sys.getsizeof(tup)
print(p)