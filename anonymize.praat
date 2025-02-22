##############
# This script is for anonymization of .wav files within the ELIC project 
#
# Peggy Renwick, November 2024 mrenwick@uga.edu 
#

form Directory
	# Set directory where input files are located
	comment input files directory:
	sentence directory /Users/mrenwic2/sync/research/Istria/anonymization/
	# Set directory to which output files should be written 
	comment output files directory:	
	sentence output /Users/mrenwic2/sync/research/Istria/anonymization/test/
	# Set directory to where the anonymization script lives
	comment anonymization scripts directory:	
	sentence anon /Users/mrenwic2/sync/research/Istria/
endform

# Tell it to apply to all (.wav) files in the selected directory
Create Strings as file list... fileList 'directory$'*.TextGrid
select Strings fileList
Sort

# Define the variable numberOfFiles
numberOfFiles = Get number of strings
option = 1

# Read files into the Object Window
for a from 1 to numberOfFiles
	select Strings fileList
        current_file$ = Get string... 'a'
        Read from file... 'directory$''current_file$'
        object_name$ = selected$("TextGrid")
	
	# get the associated sound file 
	Read from file... 'directory$''object_name$'.wav

	# Select the TextGrid and get number of intervals on Tier 1
	select TextGrid 'object_name$'
	numberOfIntervals = Get number of intervals... 1
		for b from 1 to numberOfIntervals
			select TextGrid 'object_name$'
		
			# find intervals that contain POS labels 
			pos1$ = Get label of interval... 1 'b'
			if pos1$ = "NAME"

				# get start and end times 
				select TextGrid 'object_name$'
				pos1_start = Get start point... 1 'b'
				pos1_end = Get end point... 1 'b'
		
				# take the audio file and silence it from start time to end time
				# repeat for all intervals 
				select Sound 'object_name$'
				Set part to zero: pos1_start, pos1_end, "at nearest zero crossing"

			endif
		endfor
	
	# Select the TextGrid and get number of intervals on Tier 2
	select TextGrid 'object_name$'
	numberOfIntervals = Get number of intervals... 2
		for c from 1 to numberOfIntervals
			select TextGrid 'object_name$'
		
			# find intervals that contain POS labels 
			pos2$ = Get label of interval... 2 'c'
			if pos2$ = "NAME"

				# get start and end times 
				pos2_start = Get start point... 2 'c'
				pos2_end = Get end point... 2 'c'
		
				# take the audio file and silence it from start time to end time
				# repeat for all intervals 
				select Sound 'object_name$'
				Set part to zero: pos2_start, pos2_end, "at nearest zero crossing"

			endif
		endfor

	# save .wav file with "_anon" appended to filename 
	select Sound 'object_name$'
	Write to WAV file... 'output$''object_name$'_anon.wav

	# Remove all temporary objects
	select all
	minus Strings fileList
	Remove


# Repeat with next file until done with list 
select Strings fileList
endfor
clearinfo
print That's it!
