import filecmp

def compare_pngs(png1, png2):
	return filecmp.cmp(png1, png2, shallow=False)
