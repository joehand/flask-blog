/*! =======================================================================
 * Main JS
 * Author: JoeHand
 * ======================================================================== */

define([
    'backbone',
    'jquery',
    'views/AppView',
    'models/AppModel',
    'models/PostModel',
    'backboneStick',
], function (Backbone, $, AppView, AppModel, Posts) {

    var appView, appModel, postsCol;

    appModel = new AppModel({ 
        'user': currentUser 
    });

    postsCol = new Posts(postsBootstrap);

    appView = new AppView({
        model      : appModel,
        collection : postsCol,
        el         : $('#main').get(0),
        childView  : childView
    });
    
});