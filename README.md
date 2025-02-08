### Getting Started

1. Clone the repo via `git clone https://github.com/NarrowJS/camera-tracker.git`.
2. Flash the code inside of the **Arduino** folder to the Arduino.
3. Create a folder named **videos** in the cloned repo's root directory.
4. Make sure you have `Python` and `pip` installed and install the required libraries by running:
   <br>
   `pip install opencv-python pyserial pyqt5`
   <br>

### Setting up Serial
Depending on your OS the serial ports will have different names. Edit the `auto_track.py` and `app.py` script and change the `ser` variable at the top.
<br>
<<<<<<< HEAD
MacOS: `ser = 'serial.Serial('/dev/SERIALPORT', 9600)`
<br>
Windows: `ser = 'serial.Serial('COMx', 9600)'`
=======
MacOS: `ser = '/dev/SERIALPORT'`
<br>
Windows: `ser = 'COMx'`
>>>>>>> 6410370ea25f9d4a86cf17b8eed211e1ab2f313d

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
This project would also not be possible without the YOLO hand model made by Cansik: https://github.com/cansik/yolo-hand-detection
<<<<<<< HEAD
=======

>>>>>>> 6410370ea25f9d4a86cf17b8eed211e1ab2f313d

