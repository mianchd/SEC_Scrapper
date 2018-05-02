
# SEC Scrapper

1.	No need to install anything, just click and run.
2.	The program has been developed to be very flexible so that new type of filings to search or new keywords can be included by simply typing them.
3.	The program has been successfully tested on Windows 10 - 64Bit system
4.	Windows Firewall will ask whether to Allow the program, which must be allowed.
5.	Each time the program is run, it will create a folder (in the same directory from where it is run) with the report Date and Time as its name. 
6.	Inside the folder it will generate 2 files, a CSV Report and a Log file for debugging purposes.
7.	Since there is no standard API for SEC, the program takes about 2 Hours to completely search all the different types of filings for all the (currently about 2600) Companies.
8.	This report running time will be somewhat reduced in the future when the program is further optimised. But since it must send request to the server wait for reply and then scrap the response, the time cannot be significantly reduced.
9.	The program can be scheduled to run for regular intervals using "Windows Task Scheduler" which is method using which the program doesn't have to be running all the time.

# Future Features:
1.	Send the generated reports to pre-defined e-mail addresses
2.	Have a user-friendly GUI which allows for greater flexibility



 **Copyright - Mian A. Shah - Dec 2017**
