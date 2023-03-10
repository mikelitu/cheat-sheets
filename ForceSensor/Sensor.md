# Force sensor

This file contains the commands to activate the serial port to read the 6-axial Force/Torque sensor.

## Initialize device

Connect the device via USB. Check that the sensor is detected by your PC running the command `lsub`. The sensor should appear on the list as *Bus 001 Device 003: ID 067b:2303 Prolific Technology, Inc. PL2303 Serial Port*. The serial port of the sensor should be named as follows */dev/ttyUSB\** for further processing.

Once we check that the device is connected, we need to give the device reading, writing and executing permissions. For this there are two different options, the first one requires you to run the command every time you restart your computer and the second will grant permission permanently to your user.

```
sudo cmod 777 /dev/ttyUSB*
```

or 

```
sudo adduser YourUserName dialout
```

In Windows, you just need to find the corresponding COM port number for the sensor. Save this number for the next steps.

## Activate device

To activate the serial connection with the sensor we will use the cutecom software for a more user friendly command sender. To install *cutecom* in Linux use the following commands.

```
$ sudo apt-get update
$ sudo apt-get install cutecom lrzsz
```

In Windows, you can install any alternative to CuteCom. For example, [YAT (Yet Another Terminal)](https://sourceforge.net/projects/y-a-terminal/) or [Tera Term](https://osdn.net/projects/ttssh2/)

Validate the installation running the `$ cutecom` command on the Linux terminal. Once the GUI is opened, find the serial port corresponding to the sensor that should look like the following */dev/ttyUSB_* where the underscore represents any number.

Click the Open button and in the input area make sure you set the the input mode to CR/LF in the sliding window (look at the image below) ![cutecome](imgs/cutecom.png). 

Now we need to start the sensor and setup the frequency at which we want to read the data stream. For this, Open the serial port and write the following commands on the *Input:* cell.

> AT+SMPF=200 
> 
> AT+GSTD

*AT+GSTD* restarts the data stream exchange with the serial port. *AT+SMPF* defines thesample frequency for the serial port.