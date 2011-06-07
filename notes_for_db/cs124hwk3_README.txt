CS124 Homework 3 README

Name: Hari Arul
Class: CS124

1.
(With stop words left in)
imdb1 accuracies (cross-fold validation):
	Average accuracy: 0.817
		Accuracies per fold:
		0 - 0.765
		1 - 0.845
		2 - 0.835
		3 - 0.825
		4 - 0.82
		5 - 0.82
		6 - 0.835
		7 - 0.825
		8 - 0.8755
		9 - 0.845
imdb2 accuracies: 
	Accuracy: 0.728

The model would perform worse on imdb2 than with imdb1 because as stated in the assignment, the data for imdb2 was created several years later than the data from imdb1. 
Therefore, there could easily be different word choices in general amongst the film rating community, meaning any cross-validation test amongst data from THE SAME YEAR
is most likely going to be better than when doing tests across ratings from different years. And that is what we see.

(With stop words taken out)
imdb1 accuracies (cross-fold validation):
	Average accuracy: 0.8155
		Accuracies per fold:
		0 - 0.755
		1 - 0.83
		2 - 0.835
		3 - 0.83
		4 - 0.8
		5 - 0.83
		6 - 0.825
		7 - 0.845
		8 - 0.785
		9 - 0.82

imdb2 accuracies:
	Accuracy: 0.7867

The reason removing stop words improves the accuracy in imdb2 is because when we remove a set of common words that are sure to be found across ALL different reviews,
regardless of whether they are positive or negative, we basically get rid of words that really show no differentiation amongst classes.  Not only do they not show differentiation,
they STILL would play a heavy impact in how a rating would be rated since they show up so many times.  These two factors lead to greater false classifications. 
Therefore, when these "stop words" are removed in imdb2, we get a greater accuracy with imdb2 (and roughly the same for imdb1).  This is a pattern that exists not only
with stop words, but other words that are common to film reviews - we will see this when the top 20 words for each class are shown in the next question.  One can figure
that accuracy would be increased if words like "film" and "movie" were removed, since those clearly will be in both positive and negative movie reviews quite a bit.

2. 

When class = pos: (in descending order of weighted-ness)
film
movie
story
good
time
character
life
characters
films
make
people
great
scene
man
love
scenes
world
movies
plot
back

When class = neg:
film
movie
good
time
bad
story
character
plot
characters
make
scene
people
films
scenes
action
director
man
made
movies
end

Interesting difference 1:
The first interesting diffeence I noticed was that while the word 'good' showed up as highly weighted in BOTH positive and negative reviews, but the word 'bad' 
only made the top 20 in the negative reviews.  It obviously makes sense to have the word 'good' be associated with positive reviews and the word 'bad' to be
associated with negative reviews, but it was particularly interesting to see the word good be SO highly weighted for the negative reviews.  In fact, it is the 
third highest weighting for negative review indicator, but only fourth for positive reviews (the word 'story' seems to be used more often with positive reviews than
with negative, which is also an interesting subliminal difference even though they are both used a lot between all the reviews).

My initial guess as to why negative reviews use the word 'good' so much is that the bad movies are MEANT to be put in contrast to something good, like the films it
was trying to emulate, or an actor in the film who was great in a previous one (but subpar here).  With good film reviews, however, my guess would be the reviewer
would like to emphasize how good the movie is in and of itself, rather than comparing it to something that is worse in quality (since that doesn't add any humor or 
value, in the way negatively comparing a bad film to something good might).

After grep'ing to see how the word 'good' is used in negative reviews, we do see multiple instances of what I initially surmised.  For example, we have
" james woods can be a good actor , but he has nothing to do here but to say a couple of " pseudo " -clever lines of dialogue . " in a negative review, 
clearly showing how the actor had potential / was good before, but did not play up to his/her role.  There's also the more philosophical 
"good actors should sign to good scripts , and if hollywood insists on making flicks to rake in cash , they least they could do is assume that we'd like to spend our money on a story worth more than ten cents ."
  This is suggesting that good actors should be doing something, but clearly are not doing so.  These types of examples pervade the use of "good" in negative reviews.
  
I had an interesting conversation with my roommate when I brought the use of "good" in negative reviews up.  He said 'well, I think it could be because 'not good'
 will be used to describe movies when the reviewer prefers that over 'bad', either because 'bad' was used before or because the reviewer was trying to be nice.'
 I tested this theory by grep'ing 'not good', and found out it only showed up in three cases of negative reviews, so clearly was not as big of an impact as the factor 
 listed above.  It was a theory that seeemed logical though, and it was fun to test out.

Interesting difference 2:
Another interesting difference is that the word 'life' shows up in the top 10 highly weighted words for positive reviews, but does not even show up in the top 20
 for negative reviews.  The main reason for this, I believe, is that 'life' connotes a very positive feeling, that is likely to be associated with very positive 
 reviews.  However, the first thing I noticed when grep'ing is that 'life' actually shows a lot in the negative reviews as well, so I'm surprised it doesn't make the top 20.
 Therefore, I decided to try searching for the top 30 highest weighted words to see if 'life' showed up in the negative list.  Lo and behold, "life" is the twenty-second
  most popular word on the negative reviews.  
  
However, my initial theory on why 'life' showed up a lot with good reviews still holds.  When doing a grep search under the positive reviews, I did see a couple of 
instances of this type of positive use of life.  Here are a couple of examples: "perhaps " suggested by " the novel is the appropriate way to go after all , since " simon birch " only focuses on one chapter , one year , of simon's extraordinary life ."
This is a use of the life of the character being portrayed, and how it was 'extraordinary'.  Another example of life associated with a positive term is 
'mr . cameron brings the ship to life in an almost literal sense . '  Though when I really was examining the large list of the word 'life' in positive reviews, there was
not a consistent pattern as to why it was used more so than they would be used in negative reviews (i.e. I could see them being used in the same context for negative 
reviews.)  this could be part of the reason why 'life' does show up in the top 30 weighted words in negative reviews, meaning it is just a common term amongst movie 
reviewers.  That being said, certainly part of the reason 'life' is used more in positive reviews may just be a natural association of the word as a positive term, and 
therefore subliminally more likely to be used by the reviewer when writing a review.  Just a theory though!

Interesting difference 3:
The last interesting difference which I am going to briefly discuss is how the word 'director' showed up in the top 20 for negative reviews, but not for positive reviews. 
The one obvious reason I can think of this is that movie reviewers enjoy putting blame on bad directing, whereas with good directing, they are more likely to attribute
 success to actors and/or the script.  The reason I thought of that is because of someone like M. Night Shyamalan, who has been a consistent source of ridicule amongst 
 the movie reviewers, and therefore the word 'director' would be brought up a lot when his films were reviewed.  Except when we deal with great directors like James Cameron, 
 Scorcese, Tarantino, or Guillermo del Toro, a lot of times the director goes unnoticed (in my theory).
 
 When this was put to the test, I noticed a couple of things.  The first is that 'director' still shows up a lot with positive reviews, so it's not as if the director 
 goes completely unnoticed!  Rather ,there is just more focus on other parts of the film when a review is good.  Perhaps this is because since the director has such an
 overall encompassing part in the movie, it is not as important to talk about the positive qualities of the director, since a positive review of the movie would be a 
 1-to-1 relation to this.  
 
 Anyway, when looking at how 'director' was used in negative reviews, I did see uses of it like I described i.e. the director was reviewed poorly.  For example, we have
  "the director , barry levinson , who directed the better crichton adaptation disclosure ( 1994 ) messes up with the drama and the action ."  And here's a pretty brutal 
  review: the directing is awful : it seems director matt williams had an index card with six angles written on it and used every one of them , over and over and over again"
  
I also noticed that even when the director was considered good, if (s)he did a bad movie, that would be a point that is noticed!  This is similar to what we say for main actors as well.  Here's an 
  example of this happening within the negative reviews: "the cast is great , the director is talented , and the budget is lavish , but this ill-advised remake of the classic rogers and hammerstein movie is unable to utilize any of those things to form a compelling whole . "
  
Thanks for reading my thoughts on the differences I noticed!
Hari