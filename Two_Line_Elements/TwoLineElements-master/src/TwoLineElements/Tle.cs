namespace TwoLineElements
{
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using LineParsers;
    using Models;
    using Properties;

    public static class Tle
    {
        public static TwoLineElementsModel Parse(string lines)
        {
            if (string.IsNullOrWhiteSpace(lines))
            {
                throw new ArgumentNullException(nameof(lines),
                    @"lines is null, it should contain at least 2 lines https://pl.wikipedia.org/wiki/Tle");
            }

            var linesArray = lines.Split('\n').Where(s => !string.IsNullOrEmpty(s)).ToList();
            return Parse(linesArray);
        }

        public static TwoLineElementsModel Parse(Queue<string> lines)
        {
            if (lines == null)
            {
                throw new ArgumentNullException(nameof(lines));
            }

            if (lines.Count < Convert.ToInt32(Resources.TLE_MIN_LINE_COUNT))
            {
                throw new ArgumentException("Lines count is to low");
            }

            //Tle could be 3 lines, first than is satellite name
            if (lines.Count > Convert.ToInt32(Resources.TLE_MAX_LINE_COUNT))
            {
                throw new ArgumentOutOfRangeException(nameof(lines), @"lines has more than 3 positions");
            }

            var tle = new TwoLineElementsModel();
            if (lines.Count > Convert.ToInt32(Resources.TLE_MIN_LINE_COUNT))
            {
                tle.Name = TleLine0Parser.Parse(lines.Dequeue());
            }

            tle.Line1 = TleLine1Parser.Parse(lines.Dequeue());
            tle.Line2 = TleLine2Parser.Parse(lines.Dequeue());

            return tle;
        }

        public static TwoLineElementsModel Parse(IReadOnlyCollection<string> lines)
        {
            return Parse(new Queue<string>(lines));
        }

        public static TwoLineElementsModel Parse(params string[] lines)
        {
            return Parse(new Queue<string>(lines));
        }
    }
}