/* ========================================================================
 * Post Model and Collection
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore'
], function (Backbone, _) {

    var Post = Backbone.Model.extend({
        initialize: function(opt) {
            this.url = this.collection.url + this.id;
        },
        isInFilter: function(filter) {
            var inFilter = null;
            // return True if In filter (shown)
            _.each(filter, function(val, key) {
                if (_.contains(val, this.get(key))) {
                    if (inFilter !== false){
                        inFilter = true;
                    }
                } else {
                    inFilter = false; 
                }
            }, this);

            return inFilter;
        }
    });

    var Posts = Backbone.Collection.extend({
        model : Post,
        url : postURL,
    });

    return Posts;
});