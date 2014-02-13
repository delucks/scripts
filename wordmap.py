def f(word):
	m = {}
	a = ord('a')
	p = ''
	for l in word:
		if not l in m:
			m[l] = chr(a)
			a+=1
		p+=m[l]
	return p

print f('alphabet')=='abcdaefg'
print f('poop')=='abba'
print f('appropriate')=='abbcdbceafg'
