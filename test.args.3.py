import argparse 
  
parser = argparse.ArgumentParser() 
  
# a variable to hold odd numbers 
ref_arg1 = parser.add_argument('odd', type=int) 
  
# a variable to hold even number 
ref_arg2 = parser.add_argument('even', type=int) 
  
args = parser.parse_args() 
  
# raising error in cas of 
if args.odd % 2 == 0: 
    raise argparse.ArgumentError(ref_arg1, "Argument 1 Can't be even number!!") 
  
if args.even % 2 != 0: 
    raise argparse.ArgumentError(ref_arg1, "Argument 2 Can't be odd number!!") 
