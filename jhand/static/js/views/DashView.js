/* ========================================================================
 * AdminView file
 * Author: JoeHand
 * ========================================================================
 */
 
define([
    'backbone',
    'underscore',
    'jquery',
], function (Backbone, _, $) {

    var formactive;

    var DashView = Backbone.View.extend({

        events: {
            'focusin .title-input input'    : '_showNewPostSettings',
        },

        _showNewPostSettings: function(e) {
            this.$el.find('.new-post-settings').slideDown().removeClass('hidden');
        },

        initialize: function(opts) {
            this.render();
        },

        render: function() {
            console.log(this);
            return this;
        },

    });

    return DashView;
});