###Setting up Serial
MacOS: `ser = /dev/SERIALPORT`
Windows: `seri = COMx`

### Running the Auto Tracking Script
When running the auto tracking script you can choose between the **tiny** and **tiny-v4** hand tracking models. To start the tracking script make sure you have the Arduino plugged in and run:
<br>
<br>
`python auto_track.py -n tiny` or `python auto_track.py -n v4-tiny`

### Running the Manually Controllable GUI

To run the GUI that allows you to manually control the stepper motors make sure the Arduino is plugged in and run:

`python app.py`

### Acknowledgments and Important Info
This code is not maintained and is very unoptimized. It can be significantly improved to be much quicker and responsive.
Credit to Cansik for the YOLO hand model, check his repo out here: https://github.com/cansik/yolo-hand-detection


