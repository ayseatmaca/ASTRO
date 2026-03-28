namespace TwoLineElements.Tests
{
    using System;
    using LineParsers;
    using Models;
    using Xunit;

    public class Line1ParserTests
    {
        [Fact]
        public void Parse_EmptyLine_Exception()
        {
            Assert.Throws<ArgumentNullException>(() => TleLine1Parser.Parse(""));
        }

        [Fact]
        public void Parse_LineToLong_Exception()
        {
            Assert.Throws<ArgumentOutOfRangeException>(() =>
                TleLine1Parser.Parse("2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537 "));
        }

        [Fact]
        public void Parse_ValidLine_Line1Model()
        {
            var line = "1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927";
            var result = TleLine1Parser.Parse(line);
            Assert.Equal(1, result.Line);
            Assert.Equal(25544, result.Number);
            Assert.Equal(Classification.Unclassified, result.Classification);
            Assert.Equal(DateTime.Parse("2008-09-20T12:25:40.1041920Z").ToUniversalTime(), result.Date);
            Assert.Equal(-2.182E-05, result.FirstDerivativeMeanMotion);
            Assert.Equal(0, result.SecondDerivativeMeanMotion);
            Assert.Equal(-0.11606E-4, result.DragTermRadiationPressure);
            Assert.Equal(0, result.EphemerisType);
            Assert.Equal(292, result.ElementSetNumber);
        }
    }
}