import $ from 'jquery'
import moment from 'moment'

export default {
    saveToken(token) {
        if (token) {
            $.cookie('token', token, {expires: 1});
            return true;
        } else {
            return false;
        }
    },
    getToken() {
        return $.cookie('token');
    },
    async obtainToken(username, password) {
        try {
            let response = await $.ajax({
                url: '/api/auth/obtain_token',
                method: 'POST',
                data: {
                    password, username
                }
            });
            this.saveToken(response.access);
            return true;
        } catch (e) {
            return false;
        }
    },
    destroyToken() {
        $.removeCookie('token');
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
    checkToken() {
        if (this.getToken()) {
            let data = this.parseToken(this.getToken());
            let expires = moment.unix(data.exp);
            return expires.isAfter(moment());
        } else {
            return false;
        }
    }
}