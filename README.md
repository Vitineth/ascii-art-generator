# ascii-art-generator
A basic ASCII art generator feeding from images

## Code Breakdown

### Calculating Character Density

``` python
from PIL import Image, ImageFont, ImageDraw
from operator import itemgetter

test = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!\"£$%^&*()-_=+`¬#~'@;:/?.>,<\\| ")
cor = ImageFont.truetype(r"cour.ttf", 12)

def generateImg(char, font):
    im = Image.new("RGBA", font.getsize(char), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), char, (255, 255, 255), font=font)
    return im

def getDensity(image):
    t = 0
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x, y))
            t += round((p[0] + p[1] + p[2]) / 3)
    return t / (image.width * image.height)

output = []
for char in test:
    output += [(char, getDensity(generateImg(char, cor)))]
output = sorted(output, key=itemgetter(1))
```

#### Imports

``` python
from PIL import Image, ImageFont, ImageDraw
from operator import itemgetter
```

Within this, we need to calculate the lightness of each character when drawn to an image. Therefore, in order to achieve this we need to be able to create new images, open system fonts and draw to the images which cover the PIL imports. We use the itemgetter at the end of the process in order to sort a list of lists by a specific element in the sublists which we will cover shortly.

#### Initialisation

``` python
test = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!\"£$%^&*()-_=+`¬#~'@;:/?.>,<\\| ")
cor = ImageFont.truetype(r"cour.ttf", 12)
```

`test` outlines the characters that we will be using within the final input. In order to allow easy changes, this is intially entered as a string and is then converted to a list which will split every character into its own entry. Any character than can be handled by PIL and has a valid entry in the Courier New font can be entered into this string and it will be used in the final output. 
`cor` holds a reference to the Courier New font that should be installed as standard on Windows installations. If running on another platform, the `cour.ttf` should be replaced with a reference to an installed font. Due to the nature of ASCII art, this should be a monospace font, otherwise the output will look sub-par. We initialise the font with a size of 12 as we are only using this to determine the white density of the characters. This could be set to any value but 12 gives a reasonable output without using much memory and allows quick generation times.

#### Image Generation

``` python 
def generateImg(char, font):
    im = Image.new("RGBA", font.getsize(char), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), char, (255, 255, 255), font=font)
    return im
```

When we calculate the density, we first need to create the image to find the pixels in use. To do this, we create a RGBA image with the size of the character to be drawn as provided by PILs font metrics of the given font. This means that the character should fit perfectly inside of the image. Next we generate an ImageDraw instance which will allow us to actually edit and draw to our image. Using this we draw the given character in white which directly contrasts the black background of the image. This is important as white has a high RGB value `(255, 255, 255)` whereas black has a low `(0, 0, 0)`. This means that we can find out the level of white in the image and then sort it to find the characters with the highest and lowest densities. This could be adapted for other colours but for the sake of simplicity, white on black is the easiest combination. We must ensure that we draw the character with the font that we used to calculate the size of everything goes to hell. Finally just return the image instance.

#### Density Calculation

``` python

def getDensity(image):
    t = 0
    for x in range(image.width):
        for y in range(image.height):
            p = image.getpixel((x, y))
            t += round((p[0] + p[1] + p[2]) / 3)
    return t / (image.width * image.height)
```

In short, when we are calculating the density, we are just looking for how much white is included in the image. So to do this, we go through each pixel, sum the RGB value and divide it by 3. This is ultimately pointless as all pixels should be a shade of grey and therefore `R = G = B` but this was just included for completeness sake. This total is then divided by the number of pixels to give the average amount of white per pixel in the image. This effectivly averages the color of the entire image and returns the color value which we can then interpret as the density.

#### Execution and Ordering

``` python
output = []
for char in test:
    output += [(char, getDensity(generateImg(char, cor)))]
output = sorted(output, key=itemgetter(1))
```

Here we finally get to the actual calculation of the density for each character. For each character in the test string, we generate the image using the Courier New font, and calculate the density of it and insert it into the output array as a tuple storing the density value and the actual character which we eventually use in order to get the characters when drawing the image. Finally, we sort the entire array by the second value in the tuples which is the density value. Due to white being a high value and black being low as discussed before, this naturally sorts the list so that the most pixel dense characters are at the end and the least are at the front. For example, using the test string shown above, ' ' (space) is shown as the least dense and 'B' is the most.

### Image Generation

``` python
def toASCII(in_file, out_file="ascii.txt", rotation=0):
    im = PILImg.open(in_file).convert("RGB")
    im = im.rotate(rotation)
    with open(out_file, "w") as f:
        for h in range(0, im.height, 2):
            for w in range(im.width):
                f.write(getChar(toHSL(im.getpixel((w, h)))[2]))
            f.write("\n")
    
def toHSL(rgb):
    rgb_f = list(map(lambda x: x / 255, rgb))
    margb, mirgb = max(rgb_f), min(rgb_f)
    if margb - mirgb == 0:
        h = 0
    else:
        if rgb_f[0] == margb:
            h = (rgb_f[1] - rgb_f[2]) / (margb - mirgb)
        if rgb_f[1] == margb:
            h = 2.0 + ((rgb_f[2] - rgb_f[0])/(margb - mirgb))
        if rgb_f[2] == margb:
            h = 4.0 + ((rgb_f[0] - rgb_f[1]) / (margb - mirgb))
    h = round(h * 60)
    if h < 0:
        while h < 0:
            h += 360
    l = round(((mirgb + margb) / 2) * 100)
    if margb - mirgb == 0:
        s = 0
    else:
        if l < 50:
            s = (margb - mirgb) / (margb + mirgb)
        else:
            s = (margb-mirgb) / (2.0 - margb - mirgb)
    s = round(s * 100)
    return (h, s, l)

def getChar(l):
    index = round(l/(100/len(output)))
    if index >= len(output):
        index = len(output) - 1
    return output[index][0]
```

We are going to need to explore these in a slightly strange order in order to properly explain what each section is actually doing.

#### Converting to ASCII

``` python
def toASCII(in_file, out_file="ascii.txt", rotation=0):
    im = PILImg.open(in_file).convert("RGB")
    im = im.rotate(rotation)
    with open(out_file, "w") as f:
        for h in range(0, im.height, 2):
            for w in range(im.width):
                f.write(getChar(toHSL(im.getpixel((w, h)))[2]))
            f.write("\n")
```

Converting to ASCII is the main bulk of the program and actually produces the final output. This function loads the given image file and converts it to an RGB image (this should strip out alpha values and if possible convert the image type. This isn't a perfect method as there is a chance that it can't convert the format, at which the program will fall over). I added a section to rotate the image by a given angle as a helper function when handling photos taken off my old phone so I didn't have to rotate them myself because I'm lazy. 

Then the fun big begins, the output file is opened ready for writing and we iterate through every other row of pixels in the image. We do this due to the size differences between widths and heights. If you go through every pixel, the image becomes significantly longer than it should, and while it is preserving the actual content of the image, it looks wrong. Therefore, we use every other line which seems to maintain the apparent aspect ratio much better. Then for every pixel in that row, we convert it to HSL and get the character before writing it to the file. After each line we print a new line character so the art is actually produced, pretty self explanatory. 

I've kind of glossed over the actual content of what the function does in order to convert to ASCII but that is because we are exploring that next.

#### Converting RGB to HSL

``` python 
def toHSL(rgb):
    rgb_f = list(map(lambda x: x / 255, rgb))
    margb, mirgb = max(rgb_f), min(rgb_f)
    if margb - mirgb == 0:
        h = 0
    else:
        if rgb_f[0] == margb:
            h = (rgb_f[1] - rgb_f[2]) / (margb - mirgb)
        if rgb_f[1] == margb:
            h = 2.0 + ((rgb_f[2] - rgb_f[0])/(margb - mirgb))
        if rgb_f[2] == margb:
            h = 4.0 + ((rgb_f[0] - rgb_f[1]) / (margb - mirgb))
    h = round(h * 60)
    if h < 0:
        while h < 0:
            h += 360
    l = round(((mirgb + margb) / 2) * 100)
    if margb - mirgb == 0:
        s = 0
    else:
        if l < 50:
            s = (margb - mirgb) / (margb + mirgb)
        else:
            s = (margb-mirgb) / (2.0 - margb - mirgb)
    s = round(s * 100)
    return (h, s, l)
```

I'm not a complete expert on how this function works, this is adapted from a conversion guide I found online so I won't cover how it performs it, but I will explain why we do this. RGB is one of the default methods of representing colours and it is represented by 3 values ranging from either 0 to 1 or 0 to 255. In the case of PIL it uses 0 to 255. While this is a good method of representing it as it makes sense (we can individually see how much red, how much green and how much blue), it doesn't help too much when we are handling ASCII art. At the basic level, when generating ASCII art, we are converting a grayscale version of the image as the characters we are outputting can only be one color and the background can only be one color (sort of, we can do more complicated colors but at that point aren't we just painting the image again but with more steps and lower quality?). Therefore, we can use a much more helpful method of representing the colors called HSL. This also uses three values but instead they represent Hue (expressed as an angle between 0 and 360 degrees which represents the colors position on the color wheel), Saturation (which represents how much color there actually is. This is a percentage from 0 to 100 which represents how far out from the center of the color wheel the color actually is), and Lightness which represents how bright the color is unsuprisingly (expressed as another percentage from 0 to 100). Therefore, if we are wanting to work on a grayscale version of the image, we only need the lightness value. As a result, this function is overkill and could be reduced to the following:

``` python
def getLightness(rgb):
    rgb_f = list(map(lambda x: x / 255, rgb))
    margb, mirgb = max(rgb_f), min(rgb_f)
    return round(((mirgb + margb) / 2) * 100)
```

But this was also kind of a learning experience for me so I left it.

#### Converting Lightness to a Character

``` python
def getChar(l):
    index = round(l/(100/len(output)))
    if index >= len(output):
        index = len(output) - 1
    return output[index][0]
```

Now that we can figure out how light each pixel of the image is, we can actually figure out which character to represent it with. If we are using white text on a black background then we want to use the character with the highest density in order to represent whites and the lowest to represent blacks and visa versa for black on white. As my Notepad++ uses white on black, this is the theme that I went with my outputs.

Seeing as we have an array containing the possible characters, sorted by the density with the least (representing blacks) at the start and the highest (representing whites) at the end and we have a lightness value with a low value representing a black and a high value representing a white, we can simply just use this to gain an index in the array. To do this, we divide the lightness value by how much (in terms of percent) each character represents between 0 and 100. This is a strange thing to explain but effectively, if we have 10 characters, each one has a share of 10% of the total lightness value in order for each value to be used. Therefore we use this idea to find the index in the characters array. I will likely try and produce a better explanation for this at a later date but for now try and wrap your head around how it works.

Due to the nature of the round function, it may give an output out of range, therefore if it is larger or equal to the length of the array, we just select the last element. This could be mitigated by using `math.floor` but I wanted to avoid another import for some reason. Then we just return the character at that index in the characters array (remember we stored it as a tuple with the density and the character).

This isn't the best way to perform this, in hindsight. A better way would be to use the density value in order to map the lightness value as this would produce a much better output as the character chosen would be selected because it shares an equivalent value instead of just being in the right place. This would be much harder to program though and because I'm lazy and I compromised and used this function which does give passable outputs.

### Running

All that is left after this is to call the `toASCII` function with an input and output file and let it run. The rest of the program is just sugar in order to make it work nice such as a Tkinter window for entering the values. 
