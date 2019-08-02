class FallsPosition:

	def __init__(self):
		pass
		
	def z_p(self,h,w,r,data_position_p):
		
		if r == 1:
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1	
		if r == 2 and w < 8:
			data_position_p[h][w] = 1
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w+2] = 1	
		if r == 3:
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1	
		if r == 0 and w < 8:
			data_position_p[h][w] = 1
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w+2] = 1
		elif w > 7:
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1	

		return data_position_p

	def r_z_p(self,h,w,r,data_position_p):
		
		if r == 1:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w+1] = 1
		if r == 2 and w < 8:
			data_position_p[h][w+1] = 1
			data_position_p[h][w+2] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1	
		if r == 3:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w+1] = 1	
		if r == 0 and w < 8:
			data_position_p[h][w+1] = 1
			data_position_p[h][w+2] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1
		elif w > 7:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w+1] = 1	
			
		return data_position_p

	def stick_p(self,h,w,r,data_position_p):
		
		if r == 0:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h+3][w] = 1
		if r == 1 and w < 9 and w > 1:
			data_position_p[h+2][w-2] = 1
			data_position_p[h+2][w-1] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h+2][w+1] = 1	
		if r == 2:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h+3][w] = 1	
		if r == 3 and w < 9 and w > 1:
			data_position_p[h+1][w-2] = 1
			data_position_p[h+1][w-1] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1	
		elif w > 8 or w < 2:	
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h+3][w] = 1

		return data_position_p

	def l_p(self,h,w,r,data_position_p):
		
		if r == 0:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h+2][w+1] = 1
		if r == 1 and w < 8:
			data_position_p[h][w+2] = 1
			data_position_p[h+1][w+2] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1	
		elif r == 1 and w > 7:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h+2][w+1] = 1	
		if r == 2:
			data_position_p[h][w] = 1
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w+1] = 1	
		if r == 3 and w < 8:
			data_position_p[h+2][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w+2] = 1	
		elif r == 3 and w > 7:
			data_position_p[h][w] = 1
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w+1] = 1	
		
		return data_position_p

	def r_l_p(self,h,w,r,data_position_p):
		
		if r == 0:
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w+1] = 1
			data_position_p[h+2][w] = 1
		if r == 1 and w < 8:
			data_position_p[h][w] = 1
			data_position_p[h][w+1] = 1
			data_position_p[h][w+2] = 1
			data_position_p[h+1][w] = 1	
		elif r == 1 and w > 7:
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w+1] = 1
			data_position_p[h+2][w] = 1	
		if r == 2:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h][w+1] = 1	
		if r == 3 and w < 8:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w+2] = 1	
		elif r == 3 and w > 7:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h][w+1] = 1	

		return data_position_p

	def rec_p(self,h,w,r,data_position_p):
		
		if r == 0 or r == 1 or r == 2 or r == 3:
			data_position_p[h][w] = 1
			data_position_p[h][w+1] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1

		return data_position_p

	def r_t_p(self,h,w,r,data_position_p):
		
		if r == 0 and w < 9 and w > 0:
			data_position_p[h][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w-1] = 1
		elif r == 0 and w > 8:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w-1] = 1
			data_position_p[h+2][w] = 1	
		elif r == 0 and w < 1:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w] = 1
		if r == 1 and w > 0:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w-1] = 1
			data_position_p[h+2][w] = 1	
		elif r == 1 and w < 1:	
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w] = 1
		if r == 2 and w < 9 and w > 0:
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w-1] = 1
			data_position_p[h+2][w] = 1
			data_position_p[h+1][w+1] = 1	
		elif r == 2 and w > 8:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w-1] = 1
			data_position_p[h+2][w] = 1
		elif r == 2 and w < 1:	
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w] = 1
		if r == 3 and w < 9:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w+1] = 1
			data_position_p[h+2][w] = 1
		elif r == 3 and w > 8:
			data_position_p[h][w] = 1
			data_position_p[h+1][w] = 1
			data_position_p[h+1][w-1] = 1
			data_position_p[h+2][w] = 1		

		return data_position_p
