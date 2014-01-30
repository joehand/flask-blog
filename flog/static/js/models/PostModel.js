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
        }
    });

    var Posts = Backbone.Collection.extend({
        model : Post,
        url : postURL,
    });

    return Posts;
});