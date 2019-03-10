import $ from 'jquery'
import moment from 'moment'

export default {
    async login(username, password) {
        try {
            let response = await $.ajax({
                url: '/api/auth/obtain_token',
                method: 'POST',
                data: {
                    password, username
                }
            });
            return response.token;
        } catch (e) {
            return false;
        }
    },
    async verify(token) {
        try {
            await $.ajax({
                url: '/api/auth/verify_token',
                method: 'POST',
                data: {
                    token,
                }
            });
            return true;
        } catch (e) {
            return false;
        }
    },
    async signup(username, password1, password2) {
        try {
            await $.ajax({
                url: '/api/auth/signup',
                method: 'POST',
                data: {
                    password1, password2, username
                }
            });
            return true;
        } catch (e) {
            return false;
        }
    },
    parseToken(token) {
        let encoded = token.slice(token.indexOf('.') + 1, token.lastIndexOf('.'));
        return JSON.parse(atob(encoded));
    },
    checkToken(token) {
        try {
            let data = this.parseToken(token);
            let expires = moment.unix(data.exp);
            return expires.isAfter(moment());
        } catch (e) {
            return false;
        }
    }
}