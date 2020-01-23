#! /bin/sh
#check number of operands

recursive_mode=0
path_operand="."
recursive_option="-r"
#detecting for recursive mode
if [[ $# -eq 0 ]] #setting D
then
    path_operand="."
elif [[ $# -ge 1 && $1 == $recursive_option ]] #case that one operand is -r
then
    recursive_mode=1
    #echo recursive mode
fi

if [[ $recursive_mode == 0 ]]
   then
       if [[ $# -eq 1 ]] #case that one operand is not -r
       then
	   path_operand="$1"
       elif [[ $# -ge 2 ]]
       then
	   echo "two or more operands given, Error!" >&2
	   exit 1
       fi
fi

if [[ $recursive_mode == 1 ]]
then
    if [[ $# -eq 1 ]] #wrt recursive mode, this is option for current directory
    then
	path_operand="."
    elif [[ $# -eq 2 ]]
    then
	path_operand="$2"
    elif [[ $# -ge 3 ]]
    then
	echo "More than two inputs put for recursive mode. Error!" >&2
	exit 1
    fi
fi

#checking validity of path_operand
if [ -d $path_operand ] #directory
then
    #echo "path is a directory"
    continue
elif [ -h $1 ] #symbolic link
then
    echo "path is a symbolic link" >&2 
    exit 1
#elif [ $1 == -* ]
#then
    #echo "single operand starts with a '-'" >&2
else #covers '-' case and case where our folder is bad.
    echo "path isn't anything we can use" >&2
    exit 1
fi

#path_operand is now a valid path
#iterate through every file name within path_operand.
#Note: Directories, symbolic links, and regular files are considered files with names we have to check.

#list=`find $path_operand -maxdepth 1 -type f -printf "%f\n"`

if [[ $recursive_mode == 0 ]]  
then
    list=`find $path_operand -maxdepth 1 -type f -printf "%f\n" -o -type d -printf "%f\n"` #lists files in curr directory
else
    list=`find $path_operand -type f -printf "%f\n" -o -type d -printf "%f\n"` #lists files recursively
fi

declare -a poornames_arr #output array for poorly named files
index=0
end_char="/"

#finalizing $path_operand
if [[ $recursive_mode == 0 ]]
   then
       last_char_path_operand=`echo -n $path_operand | tail -c 1`  #find the last char of the path_operand.
       output_path_operand=$path_operand                           
                 
       if [[ $last_char_path_operand != $end_char ]]               #if the last char of the path operand is not a /, add one.
       then
	   output_path_operand="$path_operand$end_char"            #our output operand is now the path_operand with a / appended.
       fi
fi


#find our duplicates (case insensitive)
dup=`find $path_operand -maxdepth 1 -type f -printf "%f\n" -o -type d -printf "%f\n" | sort -f | uniq -Di`

if [[ $recursive_mode == 1 ]]
then
    dup=`find $path_operand -type f -o -type d | sort -f | uniq -Di`
fi
#now dup holds our matched case insensitive functions.
for f in $dup
do
    inputvar=0
    if [[ $f == $1 ]]
    then
	inputvar=1
    fi
    
    output=$f
    if [[ -d $f ]]
    then
	output="$f$end_char"
    fi
    if [[ $inputvar == 0 ]]
       then
	   echo $output
    fi
done

#now we want to check our non duplicate list for syntax errors
#sorted_list=`find $path_operand -maxdepth 1 -type f -printf "%f\n" -o -type d -printf "%f\n" | sort -f | uniq -iu`
sorted_list=`find $path_operand -maxdepth 1 -type f -o -type d | sort -f | uniq -iu`
if [[ $recursive_mode == 1 ]]
then
    #sorted_list=`find $path_operand -type f -printf "%f\n" -o -type d -printf "%f\n" | sort -f | uniq -iu`
    sorted_list=`find $path_operand -type f -o -type d | sort -f | uniq -iu`
fi

for g in $sorted_list
do
    inputvar=0
    if [[ $g == $1 ]]
    then
	inputvar=1
    fi
    
    f=`basename $g`
    #echo $f
    if [[ $f == .* ]]
    then
	dot="."
	doubledot=".."
	output=$g
	if [[ $f != $dot && $f != $doubledot ]]
	then
	    if [[ -d $g ]]
	    then
		output="$g$end_char"
	    fi
	    if [[ $inputvar == 0 ]]
	    then
		echo $output
	    fi
	fi
    
    
    #search for '-' at the front of file name
    elif [[ $f == -* ]]
    then
	output=$g
	if [[ -d $g ]]
	    then
		output="$g$end_char"
	fi
	if [[ $inputvar == 0 ]]
	   then
	       echo $output
	fi

    #check for valid ascii letters '_' and '-' and '.'
    elif [[ $f == *[^a-zA-z\_\.\-]* ]]
    then
	output=$g
	if [[ -d $g ]]
	    then
		output="$g$end_char"
	fi
	if [[ $inputvar == 0 ]]
	   then
	       echo $output
	fi
	
    #A file name component must not contain more than 14 characters.
    line_len=`echo $f | awk '{print length}'`
    elif [[ $line_len -ge 15 ]]
    then
	output=$g
	if [[ -d $g ]]
	    then
		output="$g$end_char"
	fi
	if [[ $inputvar == 0 ]]
	then
	    echo $output
	fi
    fi
done

