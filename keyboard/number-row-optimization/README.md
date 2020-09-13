![Optimizing the number row folder image](folder.png)

**Estimated reading time:** 5 minutes

# Optimization potential

What's there to optimize? Ignoring some special cases, aren't all 10 digits used approximately equally?

It turns out no. A lot of real world data has a [Zipfian distribution](https://en.wikipedia.org/wiki/Zipf%27s_law), which means the frequency of any X is inversely proportional to its rank in the frequency table. For example, in texts, the most frequent word will occur approximately twice as often as the second most frequent word, three times as often as the third most frequent word, and so on. ("the" is the most common word with about 7%, while the second most common "of" has 3.5%)

And again, this comes up a lot in all kinds of data (Wikipedia quote):

> The same relationship occurs in many other rankings of human created systems, such as the ranks of mathematical expressions or ranks of notes in music, and **even in uncontrolled environments**, such as the population ranks of cities in various countries, corporation sizes, [...]

([The Zipf Mystery](https://www.youtube.com/watch?v=fCn8zs912OE) is a great video about this topic, but it's not necessary to watch for this post. There's also [Benford's law](https://en.wikipedia.org/wiki/Benford's_law), which states that "in many naturally occurring collections of numbers, the leading digit is likely to be small.")

One intuitive way I can think of for why it's true for numbers is this: A lot of text and code includes something that's akin to numbered lists. Some of these lists will end on 3, some on 701 and some on 41591878, but most of them will start with 0 or 1. Since that's the case but the higher numbers often aren't reached, it leads to 1 being more common than 2, 2 more common than 3, and so on.

To be sure, I [checked three gigantic collections of texts](corpus_count.py): A selection from project Gutenberg (public domain library of books, 6.4 GiB compressed, plain text only), Wikipedia (5.8 GiB, de, sanitized) and all C files of the Linux kernel. 

Here you can see the plot: 

![Plot that shows how the aforementioned data is mostly Zipfian](digit_frequencies.png). 

And indeed, the datasets mostly follow a Zipfian distribution. Of course, data is almost never free from noise and bias. For example, I think it's likely that the outliers of 8 and 9 in Wikipedia are largely caused by the fact that there's a lot of information about the 19th and 20th century (and less and less, the more you go into the past). It's also not surprising that 0 is a lot more common in code than in texts, given that indexes and counters usually start with 0.

So with that we have:

**Premise 1**: You type some number more often than others.

But we also need the following to get any optimization off the ground:

**Premise 2**: Some key positions are better in terms of comfort, ease, speed, or else

For example, if you agree that the key of 1 is the least comfortable, then the data shows us that the current layout (`12345 67890`) is not optimal: The digit 1 is the most common digit (or second most common, if you program a lot), yet it is in the worst position. I actually didn't realize this before working on this thing, but I actually use my ring finger to type 1's. That's how bad it is for me.

Obviously, changing the number row is of no use if it makes your life harder (after you got used to the new arrangement):

**Premise 3**: You don't have to switch, or it's easy for you to switch between a new and the traditional layout.

If any of these premises doesn't hold true for you, then changing the number row provides no benefits.

Now that we got that covered, let's look at finding your best digit arrangement. 
 

# Optimization
The [Python script](find_optimal_num_rows.py) I've written uses the previously mentioned digit distribution and several variables one can change to find the optimal arrangements. It does so by going through and rating every single one of the *10! = 3 628 800* permutations. On top of that it also rates the ones you've manually entered.

The most important variable defines how comfortable, easy and fast you find each key to type on (for the left side). It has a default of `[0.55, 0.7, 1, 0.98, 0.8]`

Your values will likely be a lot less extreme if you use a separate layer for numbers with more optimal placements. But even then you might want to put less common digits on your pinkies.


# Results
## Ratings of entered permutations

| arrangement | rating / side  | rating                              |
|-------------|----------------|-------------------------------------|
| 12345 67890 | (10.11, 7.67)  | 16.19 (current)                     |
| 42315 60897 | (11.31, 10.13) | 20.67 (+27.65% compared to current) |
| 54321 06789 | (11.23, 9.20)  | 19.12 (+18.05% compared to current) |
    
## Ratings of best possible permutations
   
| arrangement | rating / side  | rating                              |
|-------------|----------------|-------------------------------------|
| 95123 64078 | (11.14, 11.15) | 22.28 (+37.59% compared to current) |
| 95123 74068 | (11.14, 11.13) | 22.27 (+37.49% compared to current) |
| 98045 32167 | (11.18, 11.11) | 22.25 (+37.38% compared to current) |


**Best possible that keeps digits on their current side**

| arrangement | rating / side  | rating                              |
|-------------|----------------|-------------------------------------|
| 54123 76089 | (11.70, 10.35) | 21.17 (+30.71% compared to current) |


**Best possible with at most 2 swaps**

| arrangement | rating / side  | rating                              |
|-------------|----------------|-------------------------------------|
| 42315 67098 | (11.31, 10.30) | 20.96 (+29.41% compared to current) |

While I mostly made this for fun, I'm actually considering `54321 06789` or `42315 67098` for my next layout.

Thank you very much for reading! I hope you found it interesting =)


---

**TLDR**: Use `54123 76089` if you want numbers to stay on their side. Use `95123 64078` if you don't. Use `54321 06789` if you want an easy to remember change (reverse left side, move 0 right to 1). Use `42315 67098` if you only want to swap two digits (1 with 4 and 8 with 0) and still get about 3/4 of the maximum benefits.

Of course, the best number arrangement will depend on your preferences and what you do most on your computer. So, if you're going for the best possible result, you probably need to modify a few of the parameters and run the script yourself. (If you don't have Python, you can run the script here: https://repl.it/languages/python3)