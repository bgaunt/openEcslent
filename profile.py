import pstats
p = pstats.Stats('profileData')
p.sort_stats('time').print_stats(25)
