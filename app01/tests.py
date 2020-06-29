from django.test import TestCase

# Create your tests here.


# Kvps = {'1':1,'2':2}
# theCopy = Kvps
# Kvps['1'] = 5
# sum = Kvps['1'] + theCopy['1']
# print(sum)
#
# a = 3>2>1
# print(3>2>1)
#
# ch='A'
# print(ch>'B')
#
# x=43
# ch='A'
# y = 1
# print(x>=y and ch<'b' and y)
#
# min = x if x < y else y
# print(min)

a=['a','b','v','dd']
a_enum = enumerate(a)
for index,a in a_enum:
    a[index]+='a'
print(a)