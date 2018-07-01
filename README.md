# YAPS (yet another pixel sorter)

## what?
Its just another pixel sorter, nothing super special functionality-wise. It won't
even tell you how to use it if you pass it something like -h/--help. The only
argument it takes is an image (.jpg, .png, .tif(f), .gif, or .bmp), and it always
outputs to output.png. It's reasonably fast (although I think using numpy would
be faster) and it can make some pretty pictures.

## why?
Because I just came out of a project where nothing I wrote made sense even when
it worked and my comments were horrible if they were present at all. 
I wanted to write something kinda neat but very simple. Something that I could 
both understand at first glance and write good comments for.

### dependencies
Pillow 5.2.0 (earlier versions should work too)