class solution(object):
	def findlongestsubstring(self,s):
		result = 0
		l = 0
		r = 0
		lib = {}
		list1 = []
		st = ''
		for r, c in enumerate(s):
			if c in lib:
				list1.append(s[l:r])	
				l = max(l, lib[c] + 1)
			lib[c] = r
			length = r - l + 1
			result = max(result, length)

		print 'given word:',s
		print list1
		long_sub = max(list1,key=len)
		return result,long_sub	


test1 = solution()
length, substring = test1.findlongestsubstring('abcdcabeafcbb')
print 'Length of the longest substring: ',length
print '\n Longest substring:  ',substring
