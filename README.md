# The Yulia Pendant
Animated pendant using a LOLIN D1 Mini Pro ESP8266 and Adafruit CharliePlex FeatherWing 15x7 LED array

This is a fork of a Clone of Adafruit/FirePendant, modified for the Feather, then modified for ESP8266, I put my thang down, flip it and reverse it, Ti esrever dna ti pilf nwod gnaht ym tup i.  Oh yah, it loops a canned animation sequence on the display.  There's a conversion tool included for grey scale PNGs to a format that draws pixels.

This was originally made for my girlfriend as a courting gift but then it got popular, and well, I made a bunch of these for Burning Man 2019.  These will eventually be produced in mass including battery.  With a 560mah battery you can squeeze 5-7 hours out of it depending on brightness.  I have also included the 3d model for the cases used for Burning Man and the original 3d heart for my girlfirend.

Arduino sketch is comprised of 'Pendant.ino' and 'animation.h' -- latter contains animation frames packed into PROGMEM array holding bounding rectangle + column-major pixel data for each frame.  I have been able to pack over 600kb of frame data composed of over a 1000 frames.

The 'convert_big.py' is a python script that processes all the source PNG images into the required animation.h format. The PNG images were generated from Video to Image Converter by ChitPit.com using stock video found online.  I captured video, processed it using Gif Brewery 3 to an MP4 scaled down to a lower resolution in greyscale, then used Video to Image Converter to PNG files.  The convert_big.py converts those PNGs into the required format for Arduino.  This could probably be simplified and made free with imagemagick if someone wants to contribute.  I made most of this project with the help of French wine.

Parts list:
LOLIN D1 Mini Pro ESP8266
7x15 Adafruit Charliewing led board
Tiny momentary close buttons
This expensive button for sleep function (I'm open to other suggestions!)
Solid jumper wires
560mah lipo battery

Pinouts:
LOLIN D1 Mini Pro pin4 -> IO, SDA of Charliewing
LOLIN D1 Mini Pro pin5 -> IO, SCL of Charliewing
LOLIN D1 Mini Pro pin15 -> Normally Open pin of expensive button above
LOLIN D1 Mini Pro 3v -> Normally closed pin of expensive button above
LOLIN D1 Mini Pro Gnd -> Charliewing Gnd
Charliewing 3v -> Normally closed pin of expensive button above

Reason for the expensive button:
The Charliewing doesn't have a sleep function and will continue to consume power if there _was_ data at any time while powered.  If it's reset and doesn't detect data, it seems to go to sleep and doesn't consume any power.  This button interrupts power to the display (resetting it) while simultaneously brings pin15 HIGH on the ESP8266, putting it to sleep.  This is a hack.

Todo's:
[] Configure for multiple animations
[] Enable change animation button
[] Low battery auto sleep (this is a pain in the ass)
[] Enable wifi detection for synchronized animations
