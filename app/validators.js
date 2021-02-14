module.exports = {
    validateSpeeds: function(input) {
        /* integers seperated by spaces */
        return input.split(' ').every(isInt);
    },

    validateWordLimit: function(input) {
        /* single positive integer or -1 */
        return ((parseInt(input, 10) > 0 || parseInt(input, 10) === -1) && isInt(input));
    },

    validateExtra: function(input) {
        /* floating point value */
        return !isNaN(input - 0);
    },

    validateLanguage: function(input) {
        /* ENGLISH or SWEDISH */
        return (input === 'ENGLISH' || input === 'SWEDISH');
    }
};

var isInt = function(input) {
    return parseInt(input, 10) === parseFloat(input);
}