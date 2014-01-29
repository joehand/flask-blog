requirejs.config({
    paths: {
        'model'              : 'model', //shortcuts for model/view files
        'view'               : 'view',
        'jquery'             : 'libs/jquery-2.0.3',
        'underscore'         : 'libs/underscore',
        'backbone'           : 'libs/backbone',
        'backbone_dual'      : 'libs/backbone.dualstorage.amd',
    },
    shim: {
        backbone: {
            deps: ['jquery', 'underscore'],
            exports: 'Backbone'
        },
        backbone_dual: {
            deps: ['backbone'],
        },
        underscore: {
            exports: '_'
        }
    }
});

// Load the main app module to start the app
requirejs(["main"]);