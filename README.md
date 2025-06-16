<h1 align="center" style="font-size: 50px;">Quadtree Generation Library</h1>
<p1>
The primary intention of this library is to create a launching off point for other projects of mine, its capable of creating the "Quadtree" data structure, effectively born of a tree which subdivides in order to create branches. With this in place, future projects such as my rendition of the Barnes-Hut simulation will be much more streamlined.

  ‎ 
</p1>

<p align="center">
  <img src="QuadTree Visual Implementation.gif" alt="Quadtree Demo" />
</p>
<p2>
  
  ‎ 
  
Above you can see the visual representation of utilizing this library, it takes a 2d coordinate plane and then subdivides from the base quadrants through a recursive structure. This visual representation has been slowed down significantly for visual understanding. The conditions on this are that whenever a subquadrant contains more than three points, it will self divide until there are less than three within the region.  
</p2>
