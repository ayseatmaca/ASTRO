## Repository
Library for parsing two-line element sets (TLE), a data format used to encode a list of orbital elements for an Earth-orbiting object at a specific point in time known as the epoch.https://wikipedia.org/wiki/Two-line_element_set

## Repo 
https://github.com/ponoorak5/TwoLineElements

## Instalation Tle parser
![Nuget](https://img.shields.io/nuget/dt/TwoLineElements) ![Nuget](https://img.shields.io/nuget/v/TwoLineElements)

Tle parser is available on [NuGet](https://www.nuget.org/packages/TwoLineElements). 

```
Install-Package TwoLineElements
```
```sh
dotnet add package TwoLineElements
```
### Ussage Tle parser

```
var lines = "STARLINK-24\n" +
                       	"1 44238U 19029D   20182.10581531  .00001387  00000-0  94194-4 0  9999\n" +
                        "2 44238  52.9975 151.8469 0000937  68.7807 291.3284 15.13099176 60950";

TwoLineElementsModel result = Tle.Parse(lines);
```
Or
```
line0 = "STARLINK-24
string result = TleLine0Parser.Parse(line0)
```
Or
```
line1 = "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927";
Line1Model result = TleLine1Parser.Parse(line1)
```
Or
```
line2 = "2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537";
Line2Model result = TleLine2Parser.Parse(line2)
```


## License
[MIT](https://choosealicense.com/licenses/mit/)
