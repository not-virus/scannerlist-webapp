# scannerlist-webapp
A shopping utility application (intended for use with the Zebra MC92N0 mobile computer) hosted as a webapp.

Disclaimer: This is an unfinished prototype! I do not intend to continue development of this project. It was just for kicks and proof-of-concept

I found myself with a piece of expensive industrial-grade hardware and had the idea to use it to track my spending and completion of my shopping list as I went through the grocery store. The first try at this involved writing an Android app, but with the scanner module being a proprietary device, and the keyboard wedge pre-installed working so well, I decided a simple web app would provide me with a solid prototype.

This app actually worked quite well for a prototype/proof-of-concept. To use it, I had to run the Flask server with Termux on my Android phone and connect the scanner to my phone's hotspot.

# Note
This is only the core of the project. In order to make it actually work, the [android app](https://github.com/not-virus/ScannerList) must be installed and running on the scanner itself. This will require Android Studio. Unfortunately, I was not able to get Android 4.4 KitKat to give me a list of IP addresses on the network, so the IP of the server (in this case, my phone) has to be hardcoded into the app before it is compiled, packaged and installed.
