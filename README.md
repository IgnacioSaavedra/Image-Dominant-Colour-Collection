# Image-Dominant-Colour-Collection
A set of python scripts that take a number of images, get the dominant colours of every image and create some data visualizations based on their statistics

Suggested OS is Windows, it might work in other OS, but I cannot assure that.


Leave all images you wish to use in the folder named "Images", the folder should only contain .jpg and .png files.

Open main.py with any compatible IDE and run it, the data visualizations shouls appear in the folder shortly.
Though it should be noted the number of images can greatly impact the time it takes to run the script.



The statistics are dependant on the colour palette, using this the dominant colours of each image are assigned
to the closest colour in the palette, with closeness beign calculated with the differences between the rgb values
of the dominant colours and the rgb values of the colours defined in the palette.
The colour palette itself can be manually rearranged to add or remove colours, to do so simply add or remove rows
on the "colour_palette.csv" file. The columns "code","name" and "abreviation" should contain unique values. With code
just being an arbitrary number that serves as ID, and the other columns containing the rbg values of the colour
