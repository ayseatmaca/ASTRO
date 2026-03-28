namespace TwoLineElements.Tests
{
    using System;
    using LineParsers;
    using Xunit;

    public class Line0ParserTests
    {
        [Fact]
        public void InvalidParam()
        {
            Assert.Throws<ArgumentNullException>(() => TleLine0Parser.Parse(""));
        }

        [Fact]
        public void ParamToLong()
        {
            Assert.Throws<ArgumentOutOfRangeException>(() => TleLine0Parser.Parse("1998-067PC               "));
        }

        [Fact]
        public void ValidParam()
        {
            //24 length 
            var line = "1998-067PC              ";
            Assert.Equal("1998-067PC", TleLine0Parser.Parse(line));
        }
    }
}