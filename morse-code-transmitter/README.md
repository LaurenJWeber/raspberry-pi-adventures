# Morse Code Transmitter

Convert a string into morse code, and display it using LEDs driven by Raspberry Pi.

## Initial Setup and Assumptions

* Your Pi is assembled and powered up.
* Raspberry Pi OS Full (32-bit) is installed.
* The GPIOs you wish to control have been connected to LEDs with series resistors (Canakit guide recommends 220-ohm).  
  A breadboard is handy here.
* This repo has been cloned to your Pi, or to your workstation and files copied to your Pi.
  
## Usage Instructions

1. Edit the `config.json` file.  
   
   * Set `gpo_dot` to the GPO used to signal a dot.
   * Set `gpo_dash` to the GPO used to signal a dash.
   Note: these can be the same, or different, since two symbols are never sent simultaneously.
   * Adjust the timing values if desired.
   * Set `string_to_send` to the string which will be encoded and transmitted

   Save the file.
   
2. Ensure the required Python modules are installed on the Pi.  To check:
 
   `python3 -m pip list`
   
   To install any missing module, e.g. `jsons`
   
   `python3 -m pip install jsons`
   
3. Run the program and supply the following as arguments: 

* Configuration file
* Number of times to repeat the string
    * If omitted, the default is `1`
    * To repeat continually, supply `0`

Examples:

    python3 morse-code-transmitter.py config.json
    
    python3 morse-code-transmitter.py config.json 2
    
    python3 morse-code-transmitter.py config.json 0

        
The string will be flashed on the LEDs in morse code.
See video  [here](https://rumble.com/vjpqxt-raspberry-pi-morse-code-transmitter.html).

If operating in continual repeat mode, press `Enter` to break out of the loop and quit.
 
## References

[International Morse Code Alphabet](https://en.wikipedia.org/wiki/Morse_code#/media/File:International_Morse_Code.svg)

## TODO
