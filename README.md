

# yaps (yet another pixel sorter)
![yaps, because we needed another pixel sorter.](https://github.com/ggasmithh/yaps/blob/master/example/Hopetoun_falls_output.png)

## what?
yaps sorts the pixels of the image by luma value, but only within regions defined by a Sobel edge-detection algorithm.
This has some pretty neat results.


## why?
Because I just came out of a project where nothing I wrote made sense even when
it worked and my comments were horrible if they were present at all. 
I wanted to write something kinda neat but very simple. Something that I could 
both understand at first glance and write good comments for.


## open issues
~~yaps is now EXTREMELY slow and memory-hungry because I decided to take everything OO, and to make every pixel its own object (mistake).~~

This has been fixed! The latest commit now stores pixel attributes in several numpy ndarrays, and has far less for loops (there are still some to flatten, though).

Check out the results!

### low resolution image sort
#### old
![old version](https://github.com/ggasmithh/yaps/blob/master/img/old/old_time0.png)

#### new
![new version](https://github.com/ggasmithh/yaps/blob/master/img/new/new_time0.png)


### medium resolution image sort
#### old
![old version](https://github.com/ggasmithh/yaps/blob/master/img/old/old_time1.png)

#### new
![new version](https://github.com/ggasmithh/yaps/blob/master/img/new/new_time1.png)

### high resolution image sort
#### old
![old version](https://github.com/ggasmithh/yaps/blob/master/img/old/old_time2.png)

#### new
![new version](https://github.com/ggasmithh/yaps/blob/master/img/new/new_time2.png)



## usage
```
yaps.py foo.{'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp'}
```