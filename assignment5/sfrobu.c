/*
Henry Kou
UID: 204921239
Assignment 5, Hw 5

Task: write a program sfrob that reads frobnicated text lines from standard input,
and writes a sorted version to standard output in frobnicated form.
*/

#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<sys/stat.h>
#include<sys/types.h>
#include<string.h>
#include<ctype.h>

//Helper functions
//check Status of the system call. Returns 1 if error, returns 0 if successful.
int checkSysCallStatus(size_t status)
{
	if (status < 0)
	{
		fprintf(stderr, "System call not successful.\n"); //C library calls to report errors is allowed.
		return 1;
	}
	else
		return 0;
}
/*
Takes in a char and "defrobs" it by applying a bitwise XOR with 0x2A.
frob a second time on the same data returns it to its original state.
*/
int defrob(char byte)
{
	return (byte)^0x2A;
}

/*
Receives two "frobbed" text lines and compares them
Receives two pointers to char arrays.
Needs to output pos, neg, 0 int for the comparison between the two arrays

Mapping:
Condition --- Result
a<b		  --- neg
a=b		  --- 0
a>b		  --- pos

if a is an equivalent subarray of b, except shorter, a < b
if b is an equivalent subarray of a, except shorter, a > b
*/
int frobcmp(char const *a, char const *b)
{
	//char *a_iterator = *a; // char byte iterators which indexes their respective arrays and returns the values
	//char *b_iterator = *b;

	/*
	Iterate through each array and then unfrob and compare
	*/
	//for (;;a++,b++)
	
		while (1)
		{
			//smallest case: both spaces
			if (*a == ' ' && *b == ' ')
			{
				return 0;
			}

			//check if a ended before b OR defrob(a) < defrob(b)
			if ((*a == ' ' && *b != ' ') || (defrob(*a) < defrob(*b)))
			{
				return -1;
			}

			//check if b ended before a OR defrob(b) < defrob(a)
			if ((*b == ' ' && *a != ' ') || (defrob(*b) < defrob(*a)))
			{
				return 1;
			}

			//advance a and b
			a++;
			b++;
		}
	
} 

int frobcmp_upper(char const *a, char const *b)
{
	//char *a_iterator = *a; // char byte iterators which indexes their respective arrays and returns the values
	//char *b_iterator = *b;

	/*
	Iterate through each array and then unfrob and compare
	*/
	//for (;;a++,b++)

	while (1)
	{
		//smallest case: both spaces
		if (*a == ' ' && *b == ' ')
		{
			return 0;
		}

		//check if a ended before b OR defrob(a) < defrob(b)

		if ((*a == ' ' && *b != ' ') || toupper((defrob(*a)) < toupper(defrob(*b))))
		{
			return -1;
		}

		//check if b ended before a OR defrob(b) < defrob(a)
		if ((*b == ' ' && *a != ' ') || toupper((defrob(*b)) < toupper(defrob(*a))))
		{
			return 1;
		}

		//advance a and b
		a++;
		b++;
	}

}

//allows us to convert from our double char pointers from the total_lines_arr
//to the single char pointer format that frobcmp can take.
int cmp(const void* first, const void* second)
{
	//We cast to pointers to pointers since thats what our
	//words array holds
	const char* a = *(const char**)first; //convert the
	const char* b = *(const char**)second;
	return frobcmp(a, b);
}

int cmp_upper(const void* first, const void* second)
{
	//We cast to pointers to pointers since thats what our
	//words array holds
	const char* a = *(const char**)first; //convert the
	const char* b = *(const char**)second;
	return frobcmp_upper(a, b);
}

/*Checks for the error in our stream using ferror. Run everytime a char is read in from STDin and cues freeing of memory*/
int checkStdinErr()
{
	if (ferror(stdin)) //stdin is a stream which IO errors are being checked for
	{
		fprintf(stderr, "Cannot input from sdtin properly...I/O Error! Exiting...\n");
		return 1; //Use exit, not return when exiting with error
	}
	else
	{
		return 0;
	}
} 

int checkAllocErr(void *ptr)
{
	if (ptr == NULL)
	{
		fprintf(stderr, "Cannot allocate dynamic memory...Error! Exiting...\n");
		return 1;
	}
	else
	{
		return 0;
	}
}


int main(int argc, char **argv)
{
	//File Input
	struct stat fileS;
	char outbuf[1]; //for byte by byte writes
	int initFileSize = 0;
	if (fstat(0, &fileS) < 0)
	{
		fprintf(stderr, "Error, can't read file\n");
		exit(1);
	}
	initFileSize = fileS.st_size;
	int BYTE_BY_BYTE = 0;
	int F_FLAG = 0;

	if (S_ISFIFO(fileS.st_mode))
	{
		BYTE_BY_BYTE = 1;
	}

	if (!S_ISFIFO(fileS.st_mode) && !S_ISREG(fileS.st_mode))
	{
		fprintf(stderr, "Error: Input is not a file or piped input\n");
		exit(1);
	}
	//printf("Size of file is %d\n", fileS.st_size);

	//Figure out type of input file
	/*if (S_ISREG(fileS.st_mode))
	{
		printf("regular file \n");
	}
	else if (S_ISFIFO(fileS.st_mode))
	{

		printf("piped \n");
	}*/

	
	//Obtained File size
	int fSize = fileS.st_size;
	//printf("Size of file is %ld \n", fileS.st_size);
	char *fArray;
	
	//checking for input arguments

	//printing out my args. Note, by default, argv[0] is the name of the file, so argv[0] = tr2b.c
	/*for (int i = 0; i < argc; ++i)
	{
		printf("argv[%d]: %s\n", i, argv[i]);
	}*/
	//check number of args and if argv[1] is -f
	char comp[2] = { '-','f' };
	if (argc == 2)
	{
		if (strlen(argv[1]) != 2)
		{
			fprintf(stderr, "Operand is not allowed. Usage, -f\n");
			exit(1);
		}
		for (int i = 0; i < strlen(argv[1]); i++)
		{
			if (argv[1][i] != comp[i])
			{
				fprintf(stderr, "Operand is not allowed. Usage, -f\n");
				exit(1);
			}
		}
		F_FLAG = 1;
	}
	if (argc > 2)
	{
		fprintf(stderr, "Num Operand is not allowed. Usage, -f\n");
		exit(1);
	}


	if (S_ISREG(fileS.st_mode))
	{
		char **total_lines_arr = NULL;
		int total_lines_index = 0;
		
		//normal file procedure. 
		//How to go about this?
			//Iterate through fileS array and detect spaces... then output another array for qsort?
		fArray = (char*)malloc(fileS.st_size * sizeof(char)); //Allocate space for our file readin
		
		total_lines_arr = (char**)malloc(fileS.st_size * sizeof(char*));
		
		//char **total_lines_arr;
		char *curr_line;
		
		size_t status = read(0, fArray, fileS.st_size);
		if (checkSysCallStatus(status) == 1)
		{
			free(fArray);
		}

		//Goal of this iteration, figure out how many lines there are and record pointers to each word.
		int charCount = 1;
		if (fArray[fileS.st_size - 1] != ' ') //there seems to always be a \n at the end of the file...
		{
			//printf("end of file character: %d\n", fArray[fileS.st_size - 1]);
			fArray[fileS.st_size - 1] = ' ';
			//printf("space added\n");
		}
		//Used to figure out how many words there are. Aka how many spaces.
		for (int i = 0; i < fileS.st_size; i = i+charCount)
		{
			charCount = 1;
			for (int j = i; fArray[j] != ' '; j++)
			{
				charCount++;
			}
			//at this point we've come to the end of the word. put it in our total_line_arr
			char *segment = &fArray[i]; 
			
			//for debugging
			//for (int u = 0; u < charCount; u++)
			//{
			//	//printf("iteration: %d,  %c\n",u, *(segment+u)); //segment is holding the proper chars...
			//	printf("%c", *(segment + u));
			//}
			//printf("\n");

			
			*(total_lines_arr + total_lines_index) = segment;
			total_lines_index++;
		}

		//at this point, total_lines_arr holds all the unfrobbed line segments from the file.
		
		//this is where we check for -f
		if (F_FLAG)
		{
			//printf("using to upper to sort\n");
			qsort(total_lines_arr, total_lines_index, sizeof(char*), cmp_upper);
		}
		else
		{
			//Need to pass into the qsort.
			qsort(total_lines_arr, total_lines_index, sizeof(char*), cmp);
			//pass in our total_lines_arr with the size, size of each element in array and our function comparison pointer.
			//stores the sorted output in the same array as the input.
		}

		 

		size_t writeStatus = 0;
		for (size_t i = 0; i < total_lines_index; i++)
		{
			for (size_t j = 0; ; j++)
			{
				//EOF error checking
				/*if (putchar(total_lines_arr[i][j]) == EOF)
				{
				fprintf(stderr, "Error while writing character!");
				exit(1);
				}*/
				outbuf[0] = total_lines_arr[i][j]; //if total_lines_arr is 
				writeStatus = write(1, outbuf, 1);
				if (checkSysCallStatus(writeStatus) == 1)
				{
					fprintf(stderr, "Error while writing character!");
					exit(1);
				}
				if (total_lines_arr[i][j] == ' ')
				{
					break;
				}
			}
		}
		//after printing, de allocate all the dynamic memory.
		//for (int i = 0; i < total_lines_index; i++)
		//	free(total_lines_arr[i]);
		//free(total_lines_arr);
		//exit(0); //exit with success.

		fstat(0, &fileS);
		int postFileSize = fileS.st_size;
		if (initFileSize != postFileSize)
		{
			//printf("filesizes don't match\n");
			//go into byte by byte implementation, set flag.
			BYTE_BY_BYTE = 1; 

		}
	} 

	//We need to check here for growing file... note need to try with a file within tmp.
	
	//printf("filesize after file read: %d\n", fileS.st_size); 
	/*
	char buf[1];
	int rstat = read(0, buf, 1);
	if (buf[0] != )
	{
		printf("file hasn't ended")
	}
	*/
	
	
	if (BYTE_BY_BYTE) //byte by byte reading mode: for piped inputs or remainder of growing files.
	{
		//IO Variables
		char inbuf[1];
		char inbuf2[1];
		
		//Debugging variables

		char outstr[90];
		//puts(outstr);
		//char ex1 = '_';	
		//putchar(defrob(ex1));

		/* Pointer Example to a Char Array
		char ex[50] = "shit";
		const char *first = &ex[0];
		const char *c = first;
		putchar(*c); //Prints 's'
		putchar('\n');
		c++;
		putchar(*c); //prints 'h'
		putchar('\n');
		*/
		/* Testing frobcmp
		const char ex1[50] = "*{_CIA\030\031 ";
		const char ex2[50] = "*`_GZY\v ";
		int result = frobcmp(ex1, ex1); //note: add '0' to a digit to make it its char equivalent
		sprintf(outstr,"%d", result);
		puts(outstr);
		*/

		/*
		Procedure for sfrob:
		Take in one byte at a time from Stdin until you make a frobbed text line (ending in a space)
		Perform this for each line
		*/

		// initialist curr_line and total_lines_arr
		char *curr_line;		//pointer to store the current unfrobbed text line.
		char **total_lines_arr;		//pointer to start of char pointer array to store each unfrobbed text line.
		total_lines_arr = NULL;		//initialize total_lines_arr to hold nothing
		int curr_index = 0;
		int total_lines_index = 0;
		//Note: How to use malloc syntax: ptr = (cast - type*) malloc(byte - size)
		curr_line = (char*)malloc(sizeof(char)); //allocate the first byte and set curr_line to point to it.

		if (checkAllocErr(curr_line))
			exit(1);
		/*
		curr_line[curr_index] = getchar();
		if (checkStdinErr() == 1)
		{
			free(curr_line);
			exit(1);
		}
		*/

		size_t readStatus = 0;
		size_t nextReadStatus = 0;

		readStatus = read(0, inbuf, 1);

		if (checkSysCallStatus(readStatus) == 1)
		{
			free(curr_line);
			exit(1);
		}
		curr_line[curr_index] = inbuf[0];
		//get first char
		//while (curr_line[curr_index] != EOF) //prompts from stdin
		while (readStatus != 0)
		{
			/*
			char nextChar = getchar(); //look ahead with the nextChar for our spaces

			if (checkStdinErr() == 1) //error in our stdin, free our memory
			{
				free(curr_line);
				for (int i = 0; i < total_lines_index; i++)
					free(total_lines_arr[i]);
				free(total_lines_arr);
				exit(1);
			}
			*/

			nextReadStatus = read(0, inbuf2, 1);
			if (checkSysCallStatus(nextReadStatus) == 1) //error in our stdin, free our memory
			{
				free(curr_line);
				for (int i = 0; i < total_lines_index; i++)
					free(total_lines_arr[i]);
				free(total_lines_arr);
				exit(1);
			}
			char nextChar = inbuf2[0];

			//printf("%c", nextChar); Seems like we are reading in correctly, but we're getting hung forever somewhere

			//Take a look at our current char
			if (curr_line[curr_index] == ' ') //we've finished our word. Add to total_lines_arr
			{
				char **reserve = realloc(total_lines_arr, total_lines_index * sizeof(char*) + sizeof(char*));
				/*
				Notes on realloc:
				- reallocates previous total_lines array to be itself plus one more space for the next word
				- realloc deallocates the old object pointed to by ptr and returns a pointer to a new object that has the size specified by size.
				- The contents of the new object is identical to that of the old object prior to deallocation, up to the lesser of the new and old sizes.
				*/
				if (checkAllocErr(reserve)) //check state of our realloc. If bad, then free everything.
				{
					free(curr_line);
					for (int i = 0; i < total_lines_index; i++)
						free(total_lines_arr[i]);
					free(total_lines_arr);
					exit(1);
				}
				else if (!checkAllocErr(reserve))
				{
					//If reserve is a good pointer, set the start of our total_lines_arr to the start of reserve
					total_lines_arr = reserve;
					//add curr_line to our total_lines arr by pointing our lastmost element to currline.
					total_lines_arr[total_lines_index] = curr_line;
					total_lines_index++;
					//reset curr_line to read next line
					curr_line = (char*)malloc(sizeof(char)); //curr_line back to a space of one byte, ready to hold a new char.

					if (checkAllocErr(curr_line)) //check state of our new curr_line malloc. If bad, then free everything.
					{
						free(curr_line);
						for (int i = 0; i < total_lines_index; i++)
							free(total_lines_arr[i]);
						free(total_lines_arr);
						exit(1);
					}
					curr_index = -1;
				}

				//if (nextChar == EOF)
				if (nextReadStatus == 0)
				{
					break;
				}


				while (nextChar == ' ') //assumes consecutive spaces are treated as one space.
				{
					/*
					nextChar = getchar();
					if (checkStdinErr() == 1) //error in our stdin, free our memory
					{
						free(curr_line);
						for (int i = 0; i < total_lines_index; i++)
							free(total_lines_arr[i]);
						free(total_lines_arr);
						exit(1);
					}
					*/
					nextReadStatus = read(0, inbuf2, 1);
					if (checkSysCallStatus(nextReadStatus) == 1) //error in our stdin, free our memory
					{
						free(curr_line);
						for (int i = 0; i < total_lines_index; i++)
							free(total_lines_arr[i]);
						free(total_lines_arr);
						exit(1);
					}
					nextChar = inbuf2[0];
				}
			} //end if the current char in the current line is a space
			//else if (nextChar == EOF)
			else if (nextReadStatus == 0)
			{
				nextChar = ' ';
				//If standard input ends in a partial record that does not have a trailing space, 
				//your program should behave as if a space were appended to the input.
			}

			//now we are ready to append our nextChar to the curr_line.
			curr_index++;
			char *reserve_curr_line = realloc(curr_line, curr_index * sizeof(char*) + sizeof(char*));

			if (checkAllocErr(reserve_curr_line)) //check state of our realloc. If bad, then free everything.
			{
				free(curr_line);
				for (int i = 0; i < total_lines_index; i++)
					free(total_lines_arr[i]);
				free(total_lines_arr);
				exit(1);
			}
			else if (!checkAllocErr(reserve_curr_line))
			{
				curr_line = reserve_curr_line;
				curr_line[curr_index] = nextChar; //append nextChar to the curr_line
			}
		}
		//Finished prompting from Stdin: At this point total_line_array contains all of our frobbed text lines ready to be sorted.


		//this is where we check for -f
		if (F_FLAG)
		{
			//printf("using to upper to sort\n");
			qsort(total_lines_arr, total_lines_index, sizeof(char*), cmp_upper);
		}
		else
		{
			qsort(total_lines_arr, total_lines_index, sizeof(char*), cmp);
			//pass in our total_lines_arr with the size, size of each element in array and our function comparison pointer.
			//stores the sorted output in the same array as the input. 
		}
		size_t writeStatus = 0;
		for (size_t i = 0; i < total_lines_index; i++)
		{
			for (size_t j = 0; ; j++)
			{
				//EOF error checking
				/*if (putchar(total_lines_arr[i][j]) == EOF)
				{
					fprintf(stderr, "Error while writing character!");
				exit(1);
				}*/
				outbuf[0] = total_lines_arr[i][j]; //if total_lines_arr is 
				writeStatus = write(1, outbuf, 1);
				if (checkSysCallStatus(writeStatus) == 1)
				{
					fprintf(stderr, "Error while writing character!");
					exit(1);
				}
				if (total_lines_arr[i][j] == ' ')
				{
					break;
				}
			}
		}

		//after printing, de allocate all the dynamic memory.
		free(curr_line);
		for (int i = 0; i < total_lines_index; i++)
			free(total_lines_arr[i]);
		free(total_lines_arr);
		exit(0); //exit with success.
	}
}
