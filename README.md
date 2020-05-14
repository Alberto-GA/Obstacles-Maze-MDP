# Obstacles-Maze-MDP
This repository contains a repertoire of python files which provides a generative model as well as some solver algorithms for my Obstacles-Maze problem.

In this problem the autonomous agent must travel through a grid map from a initial state (that can be known or not) to the goal.
Nonetheless, the agent must be careful because it is quite likely that it will find some obstacles in the journey. These obstacles 
have been modeled as dead-ends. Mausan and kolobov describe dead-ends as states such that it is impossible to reach the goal from them.
I have said that if the agent falls in a dead-end, it will not be able to leave regardless the action it takes.

To sum up, the problem has been formulated under the frame of Markov Decision Processes (MDPs). Namely, I have described a discounted reward-infinite horizon MDP. The generative model is provided by a particular file and there are other files focused on applying particular solver algorithms such as: VI, RTDP, LRTDP, UCT...

I will try to write something that gets more into detail as soon as possible...however the codes are fully explained...


