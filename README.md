# bouncing_balls
Bouncing balls with VTK visualization.

The purpose of this code was to present the modeling of bouncing balls with applied gravity force and physical interaction between pairs of balls.

One of the main goals was to demonstrate the ability to make boundaries transparent and inactive.

The project is divided into two parts: computation (with the creation of control datafiles) and visualization (with VTK and OggTheora) code.

// There is also a converter into .json format from plain text files (part of server interaction) //

Following running is suggested to be working on every system (no one really tried to run it somewhere else except our server and Jupyter Lab under W10):
1) python3 Computation_BB.py computation_configuration.json
2) python3 Visualization_BB.py -WD or place of the first code- visualization_configuration.json

// You may also find some comment lines in code which are supposed to check if it even works, so uncomment and change them a little bit to exclude some of the sys.argv //

Configuration files are supposed to be in .json format, but you can just write all of the parameters into .txt file and feed it to the converter.py.

I hope it will work.

//There is also YAML-markups for everything and some small videofile (We are not DeSiGnErS so it may seem disgusting for some pompous guys. //


Wanna joke? 
"What is the difference between goose? His left wing is more than right!"
 In Russian, this sounds much funnier (naah it doesn't)
