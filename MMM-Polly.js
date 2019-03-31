/*
 * File:        MMM-Polly.js
 * Created:     31/03/2019 by Daniel Burr <dburr@dburr.net>
 * Description: Main file for MMM-Polly
 * License:     GNU Public License, version 3
 */

Module.register('MMM-Polly', {
    defaults: {
        voice: null,    // voice for Polly to use, e.g. "Nicola"
        language: null, // language for Polly to use, e.g. "en-AU"
        notification: "SPEECH_DISPATCHER_SAID", // notification to send after text has been spoken
    },

    start() {
        Log.info(`Starting module: ${this.name}`)
        this.sendSocketNotification('CONFIG', this.config)
    },

    notificationReceived(notification, payload) {
        if(notification === 'SPEECH_DISPATCHER_SAY') {
            var text = payload.replace(/\s+/gm, ' ') // strip newlines
            text = text.replace('&', " and ")
            this.sendSocketNotification('TTS', text)
        }
    },

    socketNotificationReceived(notification) {
        if(notification === 'FINISHED') {
            if(this.config.notification) this.sendNotification(this.config.notification)
        }
    },

    getDom: function() {
        return document.createElement("div")
    },

});
