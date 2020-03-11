########################################
####### GANGA CHALLENGE PART 1-2 #######
######### CUSTOM MERGER MODULE #########
########################################

# Imports
import os

#--------------------------------------#

def mergefiles(file_list,output_file):
    """ Custom merger helper module for merging the outputs of subjobs into one file """
    
    try:

        # Store count of "the" word
        totalCount = 0

        f_out = open(output_file,'w')

        # Iterate over all the subjob's "count.txt"
        for f in file_list:
            f_in = open(f)
            count = f_in.read()
            count = int(count)
            totalCount = totalCount + count
        
        print("PYTHON OUTPUT: Total Count of 'the' is {}".format(totalCount))

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

