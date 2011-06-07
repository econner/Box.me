README for Homework 1 of CS124


Name: Hari Arul
README for Homework 1 of CS124

To build:

./build

To execute:

./run <training data directory> <gold data file>

You can edit the files however you want however:

./build should be all we have to type to do do any configuration
./run <training data> <gold data file> should print email addresses and phone
numbers, 1 per line, to be compared with our list. Order and case does not
matter. The format of each line should be:

filename<TAB>p|e</TAB>address|phonenumber<NEWLINE>

where filename is without any directory, and p and e refer to a
phone number or an email address respectively.

Phone number should be canonicalzed as: 650-555-1234
Email addresses as: dlwh@stanford.edu

Now some information on what specific things this SpamBot can find:

E-mails: it can pull out the traditional e-mail format, such as h@a.edu
It can do this for a variety of email endings, provided as a string in the code (ex. edu, com, net, uk, etc…).  There are more that I haven't fully handled, but the top ones are provided.

It can also pull out emails when the "@" is changed to "at", "(at), or other various formats similar to that, whether they are separated by whitespace from the front of the e-mail address or not.  Ditto for "." and "dot".

SpamBot also has the capacity to pull out an e-mail when there is no recognition for "dot" but you just have an email like hari@cs stanford edu, and it will recognize that instead of those spaces, there needs to be periods.  This is a separate use case for which a method known as "emailCheckSpaces" has been written to test for this, and adjust the println accordingly.

Lastly, this SpamBot can pull out e-mails where each letter is separated by a "-".  There are more vigorous ways to improve upon this (Such as other forms of separation), but a lot of times it led to complications in the test scenario (e.g. using a ";" would bring up random false positives).

Phone Numbers:  Much simpler situationally to deal with 'edge cases' than with e-mails.  Two major ways of attacking the problem - the first is dealing with the traditional 10 number phone format, with parens optional.  Also to ensure that we are getting valid U.S. numbers, we check to see if the first number in the area code is between a 2-9, and the first number out of the first 3 digits is between a 2-9.

The second way is by looking at phone numbers in a generic way by assuming that the website owner will put a fixed string in between numbers in order to prevent spam.  Therefore, by searching for that particular string (doesn't have to be a 'dash'), we can get phone numbers.
