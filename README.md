###Setting up Serial
MacOS: `ser = /dev/SERIALPORT`
Windows: `seri = COMx`

### Running Auto Tracking
To run the auto tracking script you can choose between tiny and tiny-v4 which might work better depending on the situation.

To run the auto tracking script run
`python auto_track.py -n tiny` or `python auto_track.py -n v4-tiny`

### Running the manual GUI

To run the GUI that allows you to manually control the stepper motors run

`python app.py`

This code is not maintained and is very unoptimized. It can be significantly improved to be much quicker and responsive.
Credit to Cansik for the YOLO hand model, check his repo out here: https://github.com/cansik/yolo-hand-detection


