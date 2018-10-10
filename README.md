# yaps (yet another pixel sorter)


## what?
~~It's just another pixel sorter, nothing super special functionality-wise.~~

yaps now does some pretty cool stuff!

Pixels in the image are sorted by luma value, but only within regions defined by a Sobel edge-detection algorithm.
This has some pretty neat results.


## why?
Because I just came out of a project where nothing I wrote made sense even when
it worked and my comments were horrible if they were present at all. 
I wanted to write something kinda neat but very simple. Something that I could 
both understand at first glance and write good comments for.


## open issues
yaps is now EXTREMELY slow and memory-hungry because I decided to take everything OO, and to make every pixel its own object (mistake).

This will be fixed in the next commit, however. The ease of readability and extensibility that comes with each pixel being an object isn't worth the performance hit (yes, it's that bad). I think a solution to this may be to spread out the pixels' attributes into several numpy ndarrays. This will let me use numpy's optimized matrix math, rather than my own.

I'm also working on replacing for loops with the much faster standard library functions (which are implemented in C) where I can, and flattening them where I cannot.


## usage
```
yaps.py foo.{'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp'}
```