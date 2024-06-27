import { initializeApp } from 'firebase/app';

import { getMessaging, getToken, onMessage } from 'firebase/messaging';

import { firebaseConfig } from './config';

// Replace this firebaseConfig object with the congurations for the project you created on your firebase console. 

const firebaseApp = initializeApp(firebaseConfig)

const messaging = getMessaging(firebaseApp)

export const requestForToken = async () => {
    try {
        const currentToken = await getToken(messaging, { vapidKey: 'BC438YTR0a--B-OlMPvG9fJ7dK1cwCPrqEtU1YAN_-qTrziZMV8JRN2lA4xJhfHhswJYFX8sRkOlZP8BRC5N39Q' })
        if (currentToken) {
            console.log('current token for client: ', currentToken)
            return currentToken
        } else {
            // Show permission request UI
            console.log('No registration token available. Request permission to generate one.')
            return null
        }
    } catch (err) {
        console.log('An error occurred while retrieving token. ', err)
        return null
    }
}

export const onMessageListener = () =>
    new Promise((resolve) => {
        onMessage(messaging, (payload) => {
            resolve(payload);
        });
    });
