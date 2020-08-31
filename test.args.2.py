
import argparse 
  
# function to convert the input and  
# check the range 
def checker(a): 
    num = int(a) 
      
    if num < 5 or num > 15: 
        raise argparse.ArgumentTypeError('invalid value!!!') 
    return num 
  
  
parser = argparse.ArgumentParser( 
    description='Processing integers in range 5 to 15') 
  
# passing the function for 'type' parameter 
parser.add_argument('n', type=checker) 
  
res = parser.parse_args() 
print("square is :", res.n*res.n) 
