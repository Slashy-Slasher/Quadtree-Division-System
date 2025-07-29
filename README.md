<h2 align="center" style="font-size: 50px;"> The Barnes-Hut Simulation </h2>
<p3> The Barnes Hut simulation, is a classical approach originally developed in 1986 to the N-body problem utilizing a quadtree to circumvent the O(N^2) cost of a traditional "Bruteforce" N-body simulation. The Barnes-Hut method changes the upperbound in operation time to O(n log n) allowing for many more planets to be represented within the program, with a minor effect on overall accuracy</p3>
<br>https://en.wikipedia.org/wiki/Barnes%E2%80%93Hut_simulation</br>

<p align="center">
  <img src="Binary_Stars.gif" alt="Quadtree Demo" />
</p>


<h1 align="center" style="font-size: 50px;">Quadtree Generation Library</h1>
<p1>
The primary intention of this library is to create a launching off point for other projects of mine, its capable of creating the "Quadtree" data structure, effectively born of a tree which subdivides in order to create branches. With this in place, future projects such as my rendition of the Barnes-Hut simulation will be much more streamlined.</p1>
<br></br>
https://en.wikipedia.org/wiki/Quadtree
<br></br>

<p align="center">
  <img src="QuadTree Visual Implementation.gif" alt="Quadtree Demo" />
</p>
<br></br>

<p2>Above you can see the visual representation of utilizing this library, it takes a 2d coordinate plane and then subdivides from the base quadrants through a recursive structure. This visual representation has been slowed down significantly for visual understanding. The conditions on this are that whenever a subquadrant contains more than three points, it will self divide until there are less than three within the region.  </p2>

<s>All current updates to the Barnes-Hut simulation will take place on the master branch, a merge will occur when the results are stable</s>
This is no longer the case, all changes have been merged into the main Branch


# Limitations of Python and Future Plans
Through intensive debugging with the pyinstrument profiler, I've found that python's innate overhead was slowing down the simulation so much that even after using Numba's JIT-compling still became the bottleneck after creating 10000+ planets. 

To combat this I've decided that I'm going to re-write this program in C++ using the library Raylib, it should primarily be "Copy-Translate-Paste" as much of the simulation's logic doesn't change during the language switch. However this should yield far better performance and could allow me to implement CUDA parallelism directly in the compiler allowing for a magnitude more planets than could ever be possible with python. 

To keep this project neat however, I'm not going to add all of the project files from C++ as in previous projects they tend to clog up the repository. Only source and header files will be added under the folder Barnes-Hut C++. This should keep the old code easy to run in your IDE of choice while allowing you to see how the C++ implementation works, and with a little knowledge of C++ run them yourself too.
