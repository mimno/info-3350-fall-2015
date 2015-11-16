

"""
Randomization

Goal: We often want to make arguments that two variables are related.
But with finite samples, things could appear related just by random chance.
How do we tell whether two variables are actually related, or if
there is only chance similarity?

The key question is: what would I observe if there were no connection
between the two variables? Randomization answers this question by 
deliberately breaking any connection between variables.

We'll start by replicating the "Tea Tasting" experiment from R.A. Fisher's
book "The Design of Experiments" (1935). Here the two variables are
(1) whether milk was added to a cup before or after the tea and (2)
whether a taster says the milk was added before or after.

1. Run the function "guess_constant_number()" with n=8, 10 times. Record
your results here:

2. Run the function "guess_randomly()", also with n=8, 10 times. Record 
your results. How are these results different from #2?

3. Write a "for" loop that runs the first of these experiments 1000 times.
Use a variable called "num_eights" to keep track of how many times you
got 8/8 correct. Run this experiment 10 times, and record your
results here:

4. Change the number of trials from 8 to 10. Rerun your experiments from #3.
How many times do you get >= 8 correct?

5. If someone tells you they can tell the difference between Gimme's 
Espresso Blend and Holiday Blend, how many cups would you ask them to taste?
 

"""

import random

correct = [1, 1, 0, 0, 1, 0, 1, 0]

def guess_constant_number(n):
    ## Simulate a random guess with an equal number of positives/negatives
    guess = [0, 1] * (n/2)
    random.shuffle(guess)
    
    print correct
    print guess    
    
    correct_guesses = 0
    for i, j in zip(correct, guess):
        if i == j:
            correct_guesses += 1
            
    return correct_guesses

def guess_randomly(n):
    ## Simulate purely random guessing
    guess = []
    for i in range(n):
        guess.append(random.randint(0,1))
    
    print correct
    print guess    
    
    correct_guesses = 0
    for i, j in zip(correct, guess):
        if i == j:
            correct_guesses += 1
            
    return correct_guesses

### Write your "do N experiments" for loop here: