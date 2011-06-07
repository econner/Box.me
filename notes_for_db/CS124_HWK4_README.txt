CS124 Homework 4 README

To build:

./build

To execute:

./run <train file> <test file>

Name: Hari Arul
CS 124 Hwk 4

So I'll start out with what ended up being in the final implementation - my F1 score ended up at 0.8026, which is right around the highest I was able to get it.  
The reason I stopped here (and it will be brought up later) is because when I would try to add other things, my precision would go up, but my recall would decrease
to the point where my F1 score would actually go down.
.....................

Anyway, other than the 3 given features, this is what I added in:

A case feature, where case=Title if the first word was capitalized, and case=Normal for ALL other cases.  This includes a word with all lowercase, as well as
a word that is ALLCAPS or CamelCase.  I figured that ALLCAPS and CamelCase words are just as likely to be names as words which are all lowercase, which is why
I bundled those together.

A length feature, where I had a bucket for "short" words (<=3 letters), "medium words" (3<x<=6 letters), and "long" words (>6).  The numbers were fairly arbitrary,
and I think I got better results using different numbers, but it seemed right to have 3 and 6 be the cutoff, for some odd reason!

I also added in the length along with the previous label, as it might be plausible that if the previous label was a person and then we had a long word, that was more
likely to be a person's last name than anything else (or another person), particularly if they are in title case.

Then I added in a Name list which I was able to locate nicely on the Piazza List, where I was able to use starter code in homework 3 to make a hashmap of the common 
names.  If the word was in that, I would add a feature saying so.  This didn't seem to help my F1 too much, though, I think because precision was already fairly high,
particularly for those common names.
(I believe this is using the idea of a 'gazeteer') -- the file is called 'names.txt'

There were a mix and match of features throughout the rest of FeatureFactory, but the two main additions which I kept in were looking at previous and following words.
For previous words, I basically added a feature which had the case of the previous word, along with the case of the current word and the previous label.  This was similarly
done for the case of the next word, but since the next Label isn't given to us, that was not included in the feature.  A feature that matched the next word (i.e. the actual word)
along with the current case was also added in, and seemed to help the F1 score.

The last feature set which I added in dealt with the "position" of the word (I use 'position' fairly crudely here).  If the previous 'word' and following 'word' were
not PERIODS (i.e. did not indicate the start / end of something), I added in a features aying the position = middle (and added the case along with that).  A end position 
was similarly added (I originally had a beginning position, but that ended up obfuscating results I think because all first words in a sentence are capitalized, so it does not
help to figure out which ones are names).  This position feature seemed to help slightly.

.....................

Now onto what I tried that ended up not working as successfully as I hoped, either because the iterations / testing went too slow, or because it detracted from the F1 
score I was previously getting:

A feature for the previous label along with the current case -- didn't help! probably because that information was too sparse and already encoded within other features.

A feature for previous word + current word + previous label -- because there were so many combinations of this, it took too long for the iterations to run.

Length of word + case of word (together) -- did not help F1 score, but that's ok because they were both encoded individually, so I kept it as such.

Looking at the WORDS at position+2 and position-2.  I was thinking maybe this could help if combined with the case of those words (or if JUST the case was added), but 
not only did it greatly slow down the iterations when those features were added, it didn't seem to help F1 much.  Perhaps I was adding it into FeatureFactory incorrectly, because it seems like
First Middle Last name could be common.

Geographical information -- since states, cities, capitals could be confused for names, I thought it would be nice to add a database of those in to check.  However, since
my precision was already fairly high, and my issue was recall, that did not actually help results, and only drove recall down slightly.  My list probably wasn't too extensive either.

The last thing which I tried, which I admit was a little od, but thought it could have some merit, was that I wanted to check if the currentWord was REPEATED at 
any point in time within the last 20 words (i.e. 10 before, 10 after).  I left the code in and commented out, but my thoughts were that if a name were introduced in a paragraph
or a story, it would be repeated in succession, both in Titlecase.  That would be MUCH less likely for a place, or a title (such as 'Mayor') because it would only be 
used once, but a name is an identifier that would be used multiple times in titlecase.  However, the way I had it implemented made the program run way too slow, so I
wasn't able to see if it was actually effective.  Seeing how the other tests went, it probably wouldn't have helped much, but I thought it would be interesting to try.

That's what I tried for the most part! (I think) Thanks for reading.
Hari
