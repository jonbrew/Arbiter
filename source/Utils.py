def pct_inc(p1, p2) :
	if p1 > p2 :
		temp = p1
		p1 = p2
		p2 = temp
	return ((p2-p1)/p1)*100
