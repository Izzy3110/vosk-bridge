/**
 *  Find selector in this and descendants of this.
 *  if up == true, search parents as well.
 *
 */

;(function (global) {
    var $ = global.jQuery || global.Zepto;

    $.fn.findAll = function findAll(selector, up) {
        var self = this
        ,   search = up ? self.closest(selector) : self.filter(selector)
        ;
        return search.add(self.not(search).find(selector));
    } ;

})(this);
