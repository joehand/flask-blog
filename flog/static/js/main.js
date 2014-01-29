/*! =======================================================================
 * Main JS File for Writr
 * Author: JoeHand
 * ======================================================================== */
define([
    'backbone',
    'underscore',
    'jquery',
    'view',
    'model',
    'backbone_dual',
], function (Backbone, _, $, WritrView, WritrCol) {
    // This file is getting a bit complex ;)
    var $mainEl = $('.writr'),
        userId = $mainEl.attr('data-userid'),
        mainId = $mainEl.attr('data-postid'),
        writrCol, writrView, writrModel;

    var AppModel = Backbone.Model.extend({});

    writrModel = new AppModel({'app_offline':false, 'content_dirty':false});

    writrCol = new WritrCol([{
                                     user_id : userId,
                                     id: mainId
                                    }]);

    writrView = new WritrView({ 
                                    el : $mainEl.get(0),
                                    collection : writrCol,
                                    model : writrModel,
                                    post_id: mainId
                                  });
});