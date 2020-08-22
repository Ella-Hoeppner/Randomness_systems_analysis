# Randomness_systems_analysis
A framework for analyzing systems for producing random numbers. This code is a supplement to [this blog post](https://www.ellahoeppner.com/blog/post/making_randomness_fair). It defines two types of randomness systems called the "generalized deck" and "dynamic dice" systems, and analyzes their fairness and predictability. See the blog post for more details.

The run_tests.py file is the executable which invokes each of the other files. It will run tests using different versions of the generalized deck and dynamic dice systems to find the ideal form of each system, given a certain number of possible output values, a number of samples over which to measure the systems, and a minimum acceptable amount of unpredictability. There are constants defined near the top of run_tests.py that can be used to customize the search process.

The file randomness_systems.py defines the generalized deck and dynamic dice systems. Feel free to copy these implementations for use elsewhere.
