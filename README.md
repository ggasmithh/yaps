# yaps (yet another pixel sorter)


## what?
It's just another pixel sorter, nothing super special functionality-wise. 

The only argument it takes is an image (.jpg, .png, 
.tif(f), .gif, or .bmp).

It's reasonably fast ~~(although I think using numpy would be faster)~~ and it can make some pretty pictures (and videos).

yaps now uses numpy!


## why?
Because I just came out of a project where nothing I wrote made sense even when
it worked and my comments were horrible if they were present at all. 
I wanted to write something kinda neat but very simple. Something that I could 
both understand at first glance and write good comments for.


## dependencies
Dependencies for yaps can now be found in requirements.txt

## open issues
I removed support for videos, but I'd like to bring them back in such a way that every frame does not have to be written to disk.
In order to do that, though, I need to get my method for sorting Images cemented, which brings me to my next point.

Pixel sorting is a weird problem. Sorting is more of a 1D concept, when most colorspaces are way farther up the ladder, dimensionally speaking (RGB and HSV are 3D, CYMK is 4D, etc). I feel like a good metric for the "sorted-ness" of an image is how close the color of one pixel is to its neighbors. Perhaps a pathfinding algorithm would be suitable?