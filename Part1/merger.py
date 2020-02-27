########################################
####### GANGA CHALLENGE PART 1-2 #######
######### CUSTOM MERGER MODULE #########
########################################

# Imports
import os

#--------------------------------------#

def mergefiles(file_list,output_file):
    
    try:

        # Store count of "the" word
        totalCount = 0

        # File to write total count
        f_out = open(output_file,'w')

        # Iterate over all the subjob's "count.txt"
        for f in file_list:
            f_in = open(f)
            count = f_in.read()
            count = int(count)
            totalCount = totalCount + count
        
        print(f"PYTHON OUTPUT: Total Count of 'the' is {totalCount}")

        # Write the total count to the output file
        f_out.write(str(totalCount))

        # Close files
        f_in.close()
        f_out.flush()
        f_out.close()

        return True

    except:

        # Fail merge
        return False

########################################   

