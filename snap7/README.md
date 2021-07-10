# Snap7

This is a fork of http://snap7.sourceforge.net/


This fork focuses on extending the Snap7Server module to support some features helping to implement a software PLC.
These features are currently:
* support for program blocks (up-/download, listing)
* some dynamic SZLs
* vartable watching
* monitor mode

# Also 
This fork takes advantage of the work of @efrenlopezm who added to Snap7 the possibility to capture ladder logic programs ([honeyPLC](https://github.com/sefcom/honeyplc))

# Snap7 server
We leverage this server to simulate the sevices exposed by a real PLC. This allows to provide a higher level of interaction than a simple script would. 
