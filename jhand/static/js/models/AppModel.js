/* ========================================================================
 * AppModel
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore'
], function (Backbone, _) {

    var App = Backbone.Model.extend({

        defaults: {
            'contentDirty' : false,
            'adminUser'    : false,
        },

        initialize: function(opt) {
            var user = opt.user;

            if (user != false) {
                if (_.contains(user.roles, 'admin')) {
                    this.set('adminUser', true);
                }
            }
        }
    });

    return App;
});