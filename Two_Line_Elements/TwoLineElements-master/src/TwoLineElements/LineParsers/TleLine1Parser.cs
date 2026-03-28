namespace TwoLineElements.LineParsers
{
    using System;
    using System.Linq;
    using Extensions;
    using Models;

    public static class TleLine1Parser
    {
        /// <summary>
        ///     Parse first line Tle
        /// </summary>
        /// <param name="line1"></param>
        /// <returns>
        ///     <see cref="Line1Model" />
        /// </returns>
        /// <exception cref="ArgumentNullException"></exception>
        /// <exception cref="ArgumentOutOfRangeException"></exception>
        public static Line1Model Parse(ReadOnlySpan<char> line1)
        {
            if (line1 == null || line1.IsEmpty)
            {
                throw new ArgumentNullException(nameof(line1), @"line1 can't be empty");
            }

            if (line1.Length > 69)
            {
                throw new ArgumentOutOfRangeException(nameof(line1), @"line0 exceeds 69 chars");
            }

            var checkSum = Convert.ToInt32(line1.Columns(69, 69).ToString());
            Utils.Checksum(line1, checkSum);
            var result = new Line1Model
            {
                Line = Utils.ParseIntValue(line1.Columns(1, 1)),
                Number = Utils.ParseDoubleValue(line1.Columns(3, 7)),
                Classification = (Classification) line1.Columns(8, 8).ToArray().First(),
                Id = line1.Columns(10, 17).ToString().Trim(),
                Date = Utils.JulianToDateTimeUtc(line1.Columns(19, 32)),
                FirstDerivativeMeanMotion = Utils.ParseDoubleValue(line1.Columns(34, 43)),
                SecondDerivativeMeanMotion = Utils.ParseFloatValue(line1.Columns(45, 52)),
                DragTermRadiationPressure = Utils.ParseFloatValue(line1.Columns(54, 61)),
                EphemerisType = Utils.ParseIntValue(line1.Columns(63, 63)),
                ElementSetNumber = Utils.ParseIntValue(line1.Columns(65, 68))
            };

            return result;
        }
    }
}