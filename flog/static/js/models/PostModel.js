/* ========================================================================
 * Post Model and Collection
 * Author: JoeHand
 * ========================================================================
 */

define([
    'backbone',
    'underscore'
], function (Backbone, _) {

    var SAVE_DELAY = 3000;  //delay after typing is over until we try to save

    var saveTimeout;

    var Post = Backbone.Model.extend({
        initialize: function(opts) {
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
        },

        checkSave: function(self, v, opts, forceSave) {
            self = _.isUndefined(self) ? this : self;
            forceSave = !_.isUndefined(forceSave);

            if (forceSave === true) {
                self.save(null);
                self.syncPending = false;
            } else {
                self.syncPending = true; // flag if we manually force server sync

                if(saveTimeout) {
                    clearTimeout(saveTimeout);
                    saveTimeout = null;
                }

                saveTimeout = setTimeout(
                    function() {
                        self.save(null, { // pass null means pass whole model
                            wait:true, // wait to move on until success
                            success: function(model, rsp) {
                                self.syncPending = false;
                                /* TODO: Do I want to send updated HTML back over wire to re-render?
                                self.render();*/
                            }
                        });
                }, SAVE_DELAY);                   
            }             
        }
       
    });

    var Posts = Backbone.Collection.extend({
        model : Post,
        initialize: function(models, opts) {
            this.url = opts.url;
        },
        save: function() {
            // check if any children models have changed any sync them each
            // TODO: better way to do this?
            this.each(function(model){ 
                if (model.syncPending === true) {
                    model.checkSave(model, null, null, true); //forces server sync on model
                }
            });
        }
    });

    return Posts;
});