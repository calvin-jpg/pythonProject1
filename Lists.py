#list,sample, dictionary and a set
list = [1,2,3,4,5]  #lists are mutable(can be changed or modified
tuple = (1,2,3,4,5) #this is a row in database(it cannot be changed or modified)immutable
set = {1,2,3,4,5} #set is mutable and must always be ordered
list.append(6)
print(list)
#list.remove(6)
print(list.pop())
print(type(tuple))
print(tuple)
for i in list:
    print(i)



