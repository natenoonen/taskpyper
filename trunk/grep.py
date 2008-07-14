import re;


class grep():
	def __init__(self,*args):
		#print 'Foo'
		str = None
		target = None;
		matches = [];
		
		#if(len(args) == 0):
			#print 'empty foo'
		if(len(args) >= 1):
			str = args[0];
		if(len(args) >= 2):
			target = args[1];
		
		if (str is not None) and  (target is not None):
			reg = re.compile(re.escape(str),re.I)
			#print 'reg'
			#print reg
			for item in target:
				#print 'item'
				#print item
				if reg and (reg.search( item) is not None) :
					matches.append( item );
					#print item;
		
		if (matches is not None):
			print matches
		
def main():
	print 'main'
	
	#g = grep()


if __name__ == '__main__':
	main();
