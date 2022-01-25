# scannerlist-webapp
A shopping utility application (intended for use with the Zebra MC92N0 mobile computer) hosted as a webapp.

Disclaimer: This is an unfinished prototype! I do not intend to continue development of this project. It was just for kicks and proof-of-concept

I found myself with a piece of expensive industrial-grade hardware and had the idea to use it to track my spending and completion of my shopping list as I went through the grocery store. The obvious solution here would be to simply write an app for your phone or even the scanner itself. However, seeing as how I had this purpose-built hardware at my disposal (and being almost completely new to Android development), I decided a simple web app would provide me with a solid prototype.

This app actually worked quite well for a prototype/proof-of-concept. To use it, I had to run the Flask server with Termux on my Android phone and connect the scanner to my phone's hotspot.

# Note
This is only the core of the project. In order to make it actually work, I developed a simple android app that functioned as a kiosk-style web browser and points to only one address: the address of this server. I no longer have the code for that readily available, but you should be able to view this web app in a standard browser. If you choose to implement the android app, it should be a piece of cake for anyone with Android development experience (not me). Note that the app is to be installed and running on the scanner itself, while this webapp should be running on a server (phone, Raspberry Pi, etc)
