
#function call
def editDistance(str1, str2, m, n):
	if(m==0):
		return n
	if(n==0):
		return m
	if(str1[m-1]==str2[n-1]):
		return editDistance(str1,str2,m-1,n-1) #Do nothing same chars
	else:				#Insert							#Remove								#Replace
		return 1+min(editDistance(str1,str2,m,n-1),editDistance(str1,str2,m-1,n-1),editDistance(str1,str2,m-1,n))	

print("Enter first string:")
str1 = str(raw_input())
print("Enter second string:")
str2 = str(raw_input())
print("Calculated Edit Distance:")
print(editDistance(str1,str2,len(str1),len(str2)))