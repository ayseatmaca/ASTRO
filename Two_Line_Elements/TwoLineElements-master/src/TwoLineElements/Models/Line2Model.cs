namespace TwoLineElements.Models
{
    public class Line2Model
    {
        /// <summary>
        ///     Line number
        /// </summary>
        public int Line { get; set; }

        /// <summary>
        ///     <a href="https://en.wikipedia.org/wiki/Satellite_Catalog_Number">Satellite Catalog Number</a>
        /// </summary>
        public double Number { get; set; }

        /// <summary>
        ///     Inclination (degrees)
        ///     <a href="https://en.wikipedia.org/wiki/Orbital_inclination">See Inclination</a>
        /// </summary>
        public double Inclination { get; set; }

        /// <summary>
        ///     Right ascension of the ascending node (degrees)
        ///     <a href="https://en.wikipedia.org/wiki/Longitude_of_the_ascending_node">See Longitude of the ascending node</a>
        /// </summary>
        public double Ascension { get; set; }

        /// <summary>
        ///     Eccentricity (decimal point assumed)
        ///     <a href="https://en.wikipedia.org/wiki/Orbital_eccentricity">See Orbital eccentricity</a>
        /// </summary>
        public double Eccentricity { get; set; }

        /// <summary>
        ///     Argument of perigee (degrees)
        ///     <a href="https://en.wikipedia.org/wiki/Argument_of_periapsis">See Argument of periapsis</a>
        /// </summary>
        public double Perigee { get; set; }

        /// <summary>
        ///     Mean anomaly (degrees)
        ///     <a href="https://en.wikipedia.org/wiki/Mean_anomaly">See Mean anomaly</a>
        /// </summary>
        public double Anomaly { get; set; }

        /// <summary>
        ///     Mean motion (revolutions per day)
        ///     <a href="https://en.wikipedia.org/wiki/Mean_motion">See Mean Motion</a>
        /// </summary>
        public double Motion { get; set; }

        /// <summary>
        ///     Revolution number at epoch (revolutions)
        /// </summary>
        public double Revolution { get; set; }
    }
}