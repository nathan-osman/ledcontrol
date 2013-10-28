## ledcontrol

ledcontrol simplifies the task of controlling LED devices connected via USB.

### Usage

The ledcontrol module contains two important classes:

 - `Enumerator` - acts as an iterator, providing a list of connected devices
 - `Device` - represents an individual connected device

An example is included below:

    from ledcontrol.enumerator import Enumerator
    
    # Create an enumerator
    e = Enumerator()
    
    # Create a list of all connected devices
    l = list(e)
    
    # Grab the first device
    d = l[0]
    
    # Set the color to red
    d.color = (9, 0, 0,)
    
