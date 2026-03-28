namespace TwoLineElements.Models
{
    /// <summary>
    ///     Classification (U=Unclassified, C=Classified, S=Secret)
    /// </summary>
    public enum Classification
    {
        /// <summary>
        ///     Unclassified satellite
        /// </summary>
        Unclassified = 'U',

        /// <summary>
        ///     Classified satellite
        /// </summary>
        Classified = 'C',

        /// <summary>
        ///     Secret satellite
        /// </summary>
        Secret = 'S'
    }
}