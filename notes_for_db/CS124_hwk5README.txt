CS124 Homework 5 README

Readme for part 2 of assignment 6
Name: Hari Arul
(note: I mentioned this in my source code, but I did work with Andy Altman when we thought about ways to do the solution - honor code statement)

Given the submission for examining how the husband-wives pairs matched up in Jeopardy format, I think that based on the 20 input strings in wives.txt, all of them actually
gave us acceptable answers in wives.txt; however, when I ran the actual java file, it ended up showing 16 right and 4 wrong, but I can explain why.  Mainly this is because
what was given in gold.txt is actually slightly diferent from what was pulled out, but the name is actually the same (i.e. in Jeopardy, if we were to give the answer which I 
had presented, it would have been considered correct).

To be specific, when I ran the java file, the four errors (there were 16 correct, 4 errors) were for the wives.txt names:
Alma Vivian Johnson
Francine Faure
Naina Yeltsina
Lisa Marie Kurbikoff

In each of these cases, this is the respective results of what my file outputted as the husband and what the correct answer was:
MY ANSWER | CORRECT ANSWER
General Colin L. Powell | Colin Powell
Camus | Albert Camus
Boris Nikolayevich Yeltsin | Boris Yeltsin
Ivan Simon Cary Elwes | Cary Elwes

In all of these cases, if we gave my answer in a 'jeopardy' setting, they would be considered correct since we are actually getting the right name.  The main reason why they
don't match up perfectly with gold.txt's answers is because for some cases, we are pulling out the 'name' in the Infobox whereas the answer gives the value of the <title> 
node within page (this is the case for Colin Powell, for example).  In other cases, however, it just seems that we are either pulling just a part of the name, or we are pulling too
much of the name, as is the case with Camus and Yeltsin/Elwes, respectively.  However, in total, we can say that all our results actually work great from the test data.

From here, though, we can analyze what was tried / what worked (for both structured / unstructured cases).  Basically, for the structured data case, it worked as follows:
have an ArrayList of each text for each given wiki page in the file, and for each of those, look for a {{Infobox ... parser string, which was inevitably found wherever
there was an Infobox.  When this was found, we can use group quantifiers to pull out what the 'name' was and what the first 'spouse' was.  We assumed that the spouse would
be the wife and the name would be the husband, since this worked in all the test cases, but I can definitely see why this may not cover all cases where we have a wife which
is actually the name of the entry ,and we are trying to find the husband.  It is a simple iteration to change that, but since the test data works for this purpose, I left it as is.
RE the relative accuracy / coverage of the structured data (i.e. with Infobox), we have 100% accuracy in our test data ASSUMING that our errors would actually be considered
correct by a Jeopardy machine because Boris Nikolyevich Yeltsin, for example, is the same as Boris Yeltsin even though it doesn't match perfectly with gold.txt.  The coverage
misses two of the cases where this is no infobox relationship, but we see it interspersed in the text.  We will see in this next case how analyzing unstructured data takes
care of that problem.  Since the accuracy is so high with the structured data (i.e. it is fairly streamlined), we search for this first BEFORE trying to find any unstructured relationships
which can lead to false positives.

Moving on to the unstructured data, the main methodology was basically trying to find capitalized words that were found close to the word 'married' or 'wed'.  Obviously, 
there are many counterexamples / cases where this would NOT work, and the use of pronouns such as He/She complicates things, but for the most part, and particularly for the two cases
where unstructured finds spousal relationships that Infobox doesn't, it works fairly well.  The one interesting case is that we can make optional brackets in order to get
the proper groups for the names, and then figure out which one is supposed to be the wife and which is the husband based on what we are searching for in wives.txt.  Coverage 
remains an interesting issue, because if there was NO structured data (i.e. no infobox), the program still does a pretty good job of capturing relationships based on searching for names
between married / wed, but its not ideal or in the right order.  However, our coverage ends up being a lot higher, with WAY more false cases leading to a significantly
lower accuracy than with the structured data.  In the example used here, the two cases where the unstructured data gives us better information than the structured data is with "Elizabeth Dunnell" and "Francine Faure" where there is no direct spousal relationship within an infobox, but it works because of the unstructured relationship and the way 'marriage' is used.

All in all, this was an awesome way to be able to anayze things from a wikipedia document and analyze relationships by parsing XML and going back to using regex.  Structured data
takes the cake for accuracy, but unstructued data helps fill in the pieces.

Hari