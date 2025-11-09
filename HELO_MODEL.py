import HELO
import HELO.FCS
import HELO.Helicopter
import numpy

FlightController = HELO.FCS.FCS(Mode=2, P=0.5, I=0.0, D=0.0)
FlyingThing = HELO.Helicopter.Helicopter(Lat = numpy.radians(45.5),
                                         Lon = numpy.radians(8.70))
FlyingThing.V = numpy.float64(180.0 * 1852.0 / 3600.0)

SimulationActive : bool = False