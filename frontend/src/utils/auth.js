import $ from 'jquery'

export default {
    loggedIn: false,
    async login(session, username, password, router) {
        try {
            let response = await $.ajax({
                url: '/api/auth/obtain_token',
                method: 'POST',
                data: {
                    password, username
                }
            });
            session.start();
            session.set('jwt', response.token);
            this.loggedIn = true;
            router.push('/');
        } catch (e) {
            console.log(e);
        }
    },
    logout(session, router) {
        session.destroy();
        this.loggedIn = false;
        router.push('/');
    },
    async verify(session) {
        try {
            await $.ajax({
                url: '/api/auth/verify_token',
                method: 'POST',
                data: {
                    token: session.get('jwt'),
                }
            });
            this.loggedIn = true;
        } catch (e) {
            this.loggedIn = false;
        }
    },
    async signup(username, password1, password2, router) {
        try {
            await $.ajax({
                url: '/api/auth/signup',
                method: 'POST',
                data: {
                    password1, password2, username
                }
            });
            router.push('/');
        } catch (e) {
            console.log(e);
        }
    },
    getUserInfo(session) {
        let encoded = session.get('jwt');
        encoded = encoded.slice(encoded.indexOf('.') + 1, encoded.lastIndexOf('.'));
        return JSON.parse(atob(encoded));
    }
}