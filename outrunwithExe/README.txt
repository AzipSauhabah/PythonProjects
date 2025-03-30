Compatibility:
 - Windows:
    It only works on modern versions of Windows (7, 10) with 64-bit architectures.
 - MacOS and Linux:
    The compatibility of the video game has been verified using WineHQ 5.0. Download page: https://www.winehq.org/

Instructions:
  1- Unzip all the content to a new folder.

  2- Run Outrun.exe

Controls:
  In the menu select with ENTER and move with the ARROWS.

In-game controls are those set in control options.
  By default the controls are:
    Accelerate: Ctrl Left
    Brake: Alt Left
    Rotate: Arrows
    Pause: Esc

Options: (ENTER to confirm)
  Difficulty: (ARROWS)
    - Peaceful: No enemy vehicles and time to spare.
    - Easy: With 5 simultaneous enemy vehicles and with enough time.
    - Normal: With 10 simultaneous enemy vehicles and with a set time.
    - Hard: With 15 simultaneous enemy vehicles and with a very tight time.
  Enemies AI: (ARROWS)
    Activate or deactivate the AI ​​of the enemies, whose difficulty will depend on the difficulty of the game.
  Sound menu: (C to enter and ENTER to confirm)
    - Music volume (ARROWS).
    - Volume of the effects (ARROWS).
  Graphics menu: (C to enter and ENTER to confirm)
    - Screen resolution (ARROWS).
    - Pixel art (ARROWS). If disabled at very high resolutions, you need a fairly powerful CPU.
  Controls menu: (C to enter and ENTER to confirm)
    To change the control highlighted in yellow, you must keep SPACE and without releasing it, press the desired key, then release space to confirm.

Back doors:
  As a debugging, a back door has been enabled to start on the map you want and add extra time:
  A plain text file named "backdoor.info" (without the quotes) should be created inside the "resources" directory.
  This file can contain the lines "MAP: X" and "TIME: Y", where X is the map number (1 to 15) and Y is the overtime in seconds.
  Example of file "backdoor.info":
    MAP: 15
    TIME: 60
