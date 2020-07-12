

# yaps (yet another pixel sorter)
![yaps, because we needed another pixel sorter.](https://github.com/ggasmithh/yaps/blob/master/example/Hopetoun_falls_output.png)

## what?
yaps sorts the pixels of the image by luma value, but only within regions defined by a Sobel edge-detection algorithm.
This has some pretty neat results.

## new!
yaps has been updated to be much faster for larger images. What took 2 or 3 minutes to sort now only takes roughly 100 seconds. This performance gain was made possible by removing unnecessary object strucutres and by making use of the concurrency library.

## usage
```
yaps.py foo.{'.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp'}
```