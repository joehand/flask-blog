/* ========================================================================
 * Models JS File for Writr
 * Author: JoeHand
 * ========================================================================
 */
define(['backbone', 'underscore'], function(Backbone, _) {

    var Post = Backbone.Model.extend({
        initialize: function(options) {
            this.user_id = options.user_id;
            this.url = this.collection.url + this.id;
        }
    });

    var Posts = Backbone.Collection.extend({
        model : Post,
        url : '/edit/',
    });

    return Posts;
});