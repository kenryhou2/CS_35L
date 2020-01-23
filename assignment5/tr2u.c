#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
void checkReadStatus(size_t status)
{
	if (status < 0)
	{
		fprintf(stderr, "System call not successful.\n"); //C library calls to report errors is allowed.
		exit(1);
	}
	else
		return;
}
int main(int argc, char **argv)
{
	//printing out my args. Note, by default, argv[0] is the name of the file, so argv[0] = tr2b.c
	/*for (int i = 0; i < argc; ++i)
	{
	printf("argv[%d]: %s\n", i, argv[i]);
	}*/

	//printf("num args %d\n", argc); //print number of arguments

	//Error Checking
	//Num operands
	if (argc != 3)
	{
		fprintf(stderr, "Check number of operands. Must be two.\n"); //C library calls to report errors is allowed.
		exit(1);
	}

	//Initialize Operands
	char *from_operand = argv[1];
	char *to_operand = argv[2];

	//Operand length
	//check the byte string lengths of arg[1] and arg[2]
	//printf("arg1 len: %d, arg2 len: %d\n", strlen(from_operand), strlen(to_operand));
	
	if (strlen(from_operand) != strlen(to_operand))
	{
		fprintf(stderr, "Check operand length. Must be the same.\n");
		exit(1);
	}

	//Check if from_operand has duplicate bytes
	int asciiArr[256];
	for (int i = 0; i < 256; i++)
	{
		asciiArr[i] = 0;
	}

	for (int i = 0; i < strlen(from_operand); i++) //traverse through from_operand
	{
		//putchar((int)*(from_operand + i));
		if (asciiArr[*(from_operand + i)] == 1) //checks for repetition of the char by ascii character
		{
			fprintf(stderr, "Check for duplicate chars in first operand. No duplicates allowed!\n");
			exit(1);
		}
		asciiArr[*(from_operand + i)] = 1;
	}

	//TODO what if from operand contains a null character??
	//shouldn't be a problem because the arguments would not be equal in byte size, and \ and 0 will be treated separately.

	//After error checking, use get char and put char to transliterate the bytes from from_operand to to_operand.
	//byte by byte
	char inbuf[1]; //array of char pointers
	char outbuf[1];
	size_t status = 0;

	//performing sample read and write for one byte from Standard in
	/*size_t status = read(0, inbuf, 1);
	checkReadStatus(status);*/
	//write(1, inbuf, 1);

	while (read(0, inbuf, 1) != 0)
	{
		checkReadStatus(status); //this read status will not work...
		//status = write(1, inbuf, 1);

		char c = inbuf[0]; //seg fault here
		int match = 0;
		int str_index;
		for (str_index = 0; str_index < strlen(from_operand); str_index++) //traverse through from_operand
		{
			//putchar(*(from_operand + str_index));
			if ( c == *(from_operand + str_index))
			{
				match = 1;
				outbuf[0] = *(to_operand + str_index);
				status = write(1, outbuf, 1); //if there is a match with the correct char, replace it with the corresponding char from the to_operand.
				checkReadStatus(status);
			}
		}
		if (match == 0) //if no match, just output the char from standard input.
		{
			outbuf[0] = c;
			status = write(1, outbuf, 1);
			checkReadStatus(status);
		}
		//status = read(0, inbuf, 1);
		
	}
	return 0;
}