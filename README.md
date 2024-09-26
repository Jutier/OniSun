# OniSun
Where should you sit on the Bus?


## What is this?

s a simple python application that should help you decide which side to sit on the **bus** (*or whatever*). It does this by providing data on how much **Sun** there would be on each side. Which I consider to be very relevant some days.

## How it does?

It calculates the position of the Sun using a somewhat rough approximation, but it should not have a relevant error when compared to the error from the terrain and general city infrastructure.
Then use this position to determine the arc value for every point, and draw your path along with this information.

Currently it needs a .kml file, which I usually create in google maps.

### Why this name?
The name comes from ***ônibus*** (bus) and **Sun**, just because I thought it was funny.