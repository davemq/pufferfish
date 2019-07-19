import sys
from Bio.Seq import Seq

#An utility that takes a GFA generated by TwoPaCo as input and glues it back into
#original genome(s)

def rev_comp(seq):
	rc = Seq(seq).reverse_complement()
	return str(rc)

if len(sys.argv) != 2:
	print "Usage: glue.py <GFA file>"
	exit()

segment = dict()

def spell_segment(sid):
	return segment[sid] if sid > 0 else rev_comp(segment[-sid])

def spell_path(path, k):
	chr_body = [spell_segment(path[0])]
	spell = [spell_segment(path[0])]
	for i in xrange(1, len(path)):
		sid = path[i]
		s = spell_segment(sid)
		ps = spell[-1]
		if ps[-k:] != s[:k]:
			print path[i], path[i - 1], path
			print spell, s
			sys.exit("Improper segment overlap!")
		spell.append(s)
		chr_body.append(s[k:])
	print ''.join(chr_body)	

def refine_int(pos):
	return int(''.join(ch for ch in pos if str.isdigit(ch)))
		
def get_segment_substr(segment_id, begin, end):
	begin, end = refine_int(begin), refine_int(end)
	segment_uid = refine_int(segment_id)
	if segment_id[-1] == '+':
		return segment[segment_uid][begin:end]
	return Seq(segment[segment_uid][begin:end]).reverse_complement()
	
handle = open(sys.argv[1])
for line in handle:
	line = line.split()
	if len(line) > 0:
		if line[0] == 'S':
			sid, body = line[1], line[3]
			if sid not in segment:
				if body != '*':
					segment[int(sid)] = body
			else:
				sys.exit("Segment duplicate!")
		if line[0] == 'E':
			k = int(line[-1][:-1])	
			substr1 = get_segment_substr(line[1], line[3], line[4])
			substr2 = get_segment_substr(line[2], line[5], line[6])
			if substr1 != substr2:
				sys.exit("Invalid edge overlap")
		if line[0] == 'O':
			path = [int(x) for x in line[2:]]		
			spell_path(path, k)
handle.close()