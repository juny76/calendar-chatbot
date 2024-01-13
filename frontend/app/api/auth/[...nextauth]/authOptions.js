import GoogleProvider from 'next-auth/providers/google';

const scopes = [
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar',

].join(' ');
const NEXTAUTH_URL="http://localhost:3000"
const NEXTAUTH_SECRET="youreawizardharry"
const GOOGLE_CLIENT_ID="153638901952-7vr981ro03265b8e3jbelj3prc2tani7.apps.googleusercontent.com"
const GOOGLE_CLIENT_SECRET="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"
// Get URL from environment and alert if unset
const BASE_URL = "http://127.0.0.1:8000";
export const authOptions = {
    providers: [
        GoogleProvider({
            clientId: GOOGLE_CLIENT_ID,
            clientSecret: GOOGLE_CLIENT_SECRET,
            checks: ['none'],
            authorization: {
                params: {
                    prompt: "consent",
                    access_type: "offline",
                    response_type: "code",
                    scope: scopes
                }
            },
        })
    ],
    callbacks: {
        async signIn(user, account, profile) {
            
            console.log('User signed in successfully: ', user.user.name);
            console.log('Access token: ', user.account.access_token.slice(0,5) + 'XXXXX');

            // Post to the FastAPI server with the user email, name, access token, and timestamp for latest login
            try {
                const endpoint = `${BASE_URL}/users`;
                const response = await fetch(endpoint, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: user.user.email,
                        name: user.user.name,
                        access_token: user.account.access_token,
                        timestamp: new Date().toISOString()
                    })
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }

                const responseData = await response.json();
                console.log('Response data: ', responseData);
                return true;
            } catch (error) {
                console.error('Error in POST request: ', error);
                return false;
            }
        }
    },
    jwt: {
        encryption: true,
    },
    secret: NEXTAUTH_SECRET,
};