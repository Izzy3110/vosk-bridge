/**
 * flattenArray(nestedArray)
 * 
 * Accepts an array of values and arrays and returns
 * a single array of values.
 * 
 * Usage:
 * 
 *     var nested = [[1, 2, [3]], 4];
 *     var flat = flattenArray(nested);
 *     // console.log(flat) => [1, 2, 3, 4]
 */
function flattenArray(nestedArray) {
	var flat = [], i;
	for (i = 0; i < nestedArray.length; i++) {
		if (Array.isArray(nestedArray[i])) {
			flat = flat.concat(flattenArray(nestedArray[i]));
		} else {
			flat.push(nestedArray[i]);
		}
	}
	return flat;
}

/**
 * Array.isArray()
 * 
 * Ensures that Array.isArray() is defined; code thanks
 * to Andy E: <http://stackoverflow.com/a/4029057/38666>
 * 
 * Determining if something is an array in Javascript is
 * really difficult to do predictably prior to ECMAScript 5.
 * As I know nothing about where this flattening code might
 * need to run, it's safest to include a fallback for older
 * browsers and assume that cross-window calls to this code
 * are possible (which precludes the use of `nestedArray
 * instanceof Array`).
 */
(function () {
    var toString = Object.prototype.toString,
        strArray = Array.toString(),
        jscript  = /*@cc_on @_jscript_version @*/ +0;

    // jscript will be 0 for browsers other than IE
    if (!jscript) {
        Array.isArray = Array.isArray || function (obj) {
            return toString.call(obj) == "[object Array]";
        }
    }
    else {
        Array.isArray = function (obj) {
            return "constructor" in obj && String(obj.constructor) == strArray;
        }
    }
})();