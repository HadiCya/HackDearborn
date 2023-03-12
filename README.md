# HackDearborn

## What it does
We were inspired by all the developers who can't afford to pay for user testing, and gives developers the opportunity to test their products on the fly without having to continuously test their products. Our app is demonstrated by our two flagship games that are inspired by common games and their mechanics. The AI will play the demo games and find the best strategies to beat it, even if they are exploits, which can in turn help developers find bugs in their code.

## How we built it
The Generative AI Tester is built off of the NeuroEvolution of Augmenting Topologies algorithm. This algorithm replicates the biological process of natural selection. It will produce multiple AI agents that represent the player of the game, and will give them random weights in their neural connections between inputs and possible outputs. In our example demo, "Flappy Ford," the three inputs we give it are the cars current position, the next top buildings position, and the next bottom buildings position. Each AI will randomly adjust weights until they find a strategy that gets them the highest fitness value. The fitness value is calculated, in our example, every frame they aren't dead. 

## Challenges we ran into
AI is extremely difficult to understand and implement. It was hard for our team to work on things simultaneously, so we prioritized creating demo games to go along with the AI.

## Accomplishments that we're proud of
Learned the skills of developing software that utilizes AI and make games to match it, while also having a really fun time!

## What's next for Generative AI Tester
Make a User friendly front-end for developers to implement into their own games and software!
