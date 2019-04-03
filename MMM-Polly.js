/*
 * File:        MMM-Polly.js
 * Created:     31/03/2019 by Daniel Burr <dburr@dburr.net>
 * Description: Main file for MMM-Polly
 * License:     GNU Public License, version 3
 */

Module.register('MMM-Polly', {
    defaults: {
        voice: null,    // Voice for Polly to use, e.g. "Nicole".
        language: null, // Language for Polly to use, e.g. "en-AU".
        rate: 100,      // Specify a percentage to increase or decrease the speed of the speech. 100% indicates no change from the normal rate.  Percentages greater than 100% increase the rate.  Percentages below 100% decrease the rate.  The minimum value you can provide is 20%.
        pitch: 0,       // Specify a percentage to raise or lower the tone (pitch) of the speech.  The maximum value allowed is +50%.  The smallest value allowed is -33.3%.
        volume: 0,      // Change the volume of speech (in decibels).  +6dB is approximately twice the current amplitude. The maximum positive value is about +4.08dB.  -6dB means approximately half the current amplitude.
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
