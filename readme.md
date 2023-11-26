# Adele in Vegas: A Pepper's Ghost Project

## Project Overview

Welcome to the "Adele in Vegas" project, an immersive and interactive experience created to bring a slice of Adele's Las Vegas concert into your home. This project is based on the Pepper's Ghost principle, an illusion technique used in theater and magic tricks to create ghostly images. It's perfect for fans of Adele or anyone who loves a bit of showmanship and technology melded together.

My source if insparation came from this article at Element14 [Element14 Holo Pyramid Project](https://community.element14.com/challenges-projects/design-challenges/picasso/b/blog/posts/hologram-pi-ramid---project-complete)

For this particular setup, we've focused on creating a captivating display that combines video projections with synchronized LED lighting effects. It's designed to celebrate a special occasion — in this case, a birthday — with a unique and memorable Adele-themed experience.


### Features

- **Pepper's Ghost Illusion:** A clever use of lighting and reflective surfaces to create a lifelike image of Adele performing.
- **LED Light Show:** Synchronized Addressble LED animations that complement the music and visuals.
- **Customizable Video Playback:** Tailor the experience with your favorite performances.
- **Interactive Elements:** Includes functionality for user interaction, enhancing the immersive experience.
- **Raspberry Pi Powered:** The entire setup is controlled by a Raspberry Pi, making it compact and easy to replicate.

## Hardware Requirements

- Raspberry Pi (any model with sufficient processing power)
- NeoPixel LED Strips
- Transparent reflective surface (e.g., Plexiglas)
- Monitor, projector or in my case 7" Raspberry PI touch display
- Basic wiring tools and connectors
- USB sound card and small audio amp

## Software Dependencies

- Python 3
- VLC for Python (for video playback and graphics)
- RPi.GPIO (for Raspberry Pi GPIO control)
- Adafruit_NeoPixel library (for controlling NeoPixel LEDs)

## Issues with NeoPixel Library and Sound Playback

When integrating the NeoPixel LED library with sound playback in a Raspberry Pi project, there are specific challenges and considerations to be aware of:

### Running LEDs and Sound Under Different Users

#### NeoPixel LEDs Requirement for Root Access
- The NeoPixel library typically requires root access to control the GPIO pins on the Raspberry Pi effectively.
- Running LED control scripts with root privileges is necessary for proper functioning.

#### Sound Playback as a Non-Root User
- In contrast, sound playback tools like VLC generally run under a standard user account.
- Running these applications as root is not recommended for security reasons.

### Audio Interference with GPIO Pins

#### Interference When Using GPIO for Audio
- Utilizing certain GPIO pins for LED control can interfere with the onboard audio output of the Raspberry Pi.
- This interference is especially noticeable when the NeoPixel library is used, as it requires precise timing control over the GPIO pins.

#### Solution: Using USB Audio
- To circumvent the audio interference issues, we use a USB audio output instead of the onboard audio jack.
- The USB audio solution isolates the sound playback from the GPIO pins, thus eliminating the interference.
- This approach allows both the LEDs and sound to function optimally without impacting each other's performance.

### Conclusion

In summary, while integrating NeoPixel LEDs with sound playback, it's essential to run the LED controls with root access and handle sound playback as a non-root user. To avoid audio interference with the GPIO pins used by the NeoPixel library, employing a USB audio output is a recommended solution. This setup ensures both visual and audio elements of the project can operate effectively and without conflict.

Note: To create the 3 sided video footage I used a Pro license for Canva (canva.com) but I assume any video editing tool would work fine.

## Installation

1. **Clone the Repository:**

    `git clone https://github.com/jimbydude/pyramid-hologram.git`

2. **Create python envronment**

    `python3 -m venv foobar`
    
    See this doc for more details: https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi?view=all

3. **Install Required Libraries:**

    `pip install python-vlc`
    `sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel`
    `sudo python3 -m pip install --force-reinstall adafruit-blinka`

    Neopixel setup: https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage

4. **Hardware Setup:**
- Assemble the Pepper's Ghost reflective setup using Plexiglas and strategic lighting.
- Connect the NeoPixel LEDs to the Raspberry Pi GPIO pins.

## Usage
1. **Setup the Project:**
Navigate to the cloned repository's directory and run the main script:

    ```bash
    cd pyramid-hologram
    python3 control.py
    ```

2. **Choose a Performance:**
Place your video file(s) in the designated folder and select it within the script's interface.

3. **Enjoy the Show:**
The script will handle the projection and LED synchronization. Sit back and experience "Adele in Vegas" right at home!

## Customization
Feel free to modify the scripts to include different songs, adjust the LED animations, or change the video content to suit your preferences or special occasions.

I did not include video files I used but you can easily add your own as per instructions.

## Contributing
Contributions, ideas, and feedback are warmly welcomed. Whether it's adding new features, improving documentation, or reporting issues, your input is valuable.

## License
[none]

## Acknowledgments
A special thanks to all contributors and to the open-source community for making projects like this possible.

## Helpful Resources

During the development of this project, several online resources were instrumental in providing guidance and technical information. Below is a list of these key resources:

1. **Python Virtual Environment on Raspberry Pi - Adafruit**  
   A comprehensive guide on setting up and using Python virtual environments on Raspberry Pi.  
   [Adafruit Guide](https://learn.adafruit.com/python-virtual-environment-usage-on-raspberry-pi?view=all)

2. **Python VLC MediaPlayer - Setting Position - GeeksforGeeks**  
   An article explaining how to control media playback positions using the Python VLC MediaPlayer.  
   [GeeksforGeeks Article](https://www.geeksforgeeks.org/python-vlc-mediaplayer-setting-position/?ref=ml_lbp)

3. **NeoPixels on Raspberry Pi Using Python - Adafruit**  
   A detailed guide on how to use NeoPixels (WS2812 LEDs) with a Raspberry Pi, including Python code examples.  
   [Adafruit NeoPixel Guide](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage)

4. **WS2812 Addressable LEDs Raspberry Pi Quickstart Guide - Core Electronics**  
   A quickstart guide for setting up WS2812 addressable LEDs with a Raspberry Pi.  
   [Core Electronics Guide](https://core-electronics.com.au/guides/ws2812-addressable-leds-raspberry-pi-quickstart-guide/)

5. **Installing CircuitPython on Raspberry Pi - Adafruit**  
   Instructions for installing CircuitPython on Raspberry Pi, useful for various hardware projects.  
   [Adafruit CircuitPython Guide](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)

These resources provided valuable information and instructions that greatly assisted in the successful completion of this project.
 
