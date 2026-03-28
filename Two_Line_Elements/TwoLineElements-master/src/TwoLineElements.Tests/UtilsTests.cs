namespace TwoLineElements.Tests
{
    using System;
    using Exceptions;
    using Extensions;
    using Xunit;

    public class UtilsTests
    {
        [Fact]
        public void Checksum_ValidChecksum()
        {
            var line = @"1 43554U 98067PC  20118.45620883  .00054942  00000-0  30671-3 0  9993";
            Assert.Equal(3, Utils.Checksum(line));
        }

        [Fact]
        public void Checksum_InvalidChecksum_Exception()
        {
            var line = @"1 43554U 98067PC  20118.45620883  .00054942  00000-0  30671-3 0  9993";
            var exception = Assert.Throws<ChecksumException>(() => Utils.Checksum(line, 5));
            Assert.Equal(5, exception.Expected);
            Assert.Equal(3, exception.Actual);
        }

        [Fact]
        public void JulianToDateTimeUtc_Valid_DateTime()
        {
            var jDate = @"08264.51782528";
            var dateTime = Utils.JulianToDateTimeUtc(jDate);
            var expected = new DateTime(2008, 9, 20, 12, 25, 40, 104, DateTimeKind.Utc);
            Assert.Equal(expected.Day, dateTime.Day);
            Assert.Equal(expected.Year, dateTime.Year);
            Assert.Equal(expected.Month, dateTime.Month);
            Assert.Equal(expected.Hour, dateTime.Hour);
            Assert.Equal(expected.Minute, dateTime.Minute);
            Assert.Equal(expected.Second, dateTime.Second);
            Assert.Equal(expected.Millisecond, dateTime.Millisecond);
            Assert.Equal(DateTimeKind.Utc, dateTime.Kind);
        }

        [Fact]
        public void JulianToDateTimeUtc_Invalid_Exception()
        {
            var jDate = @"08264.517825254";
            Assert.Throws<IndexOutOfRangeException>(() => Utils.JulianToDateTimeUtc(jDate));
            Assert.Throws<IndexOutOfRangeException>(() => Utils.JulianToDateTimeUtc(null));
            Assert.Throws<IndexOutOfRangeException>(() => Utils.JulianToDateTimeUtc(string.Empty));
            Assert.Throws<IndexOutOfRangeException>(() => Utils.JulianToDateTimeUtc("123"));
        }
    }
}