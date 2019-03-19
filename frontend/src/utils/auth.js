import moment from 'moment'
import cookies from 'js-cookie'
import axios from 'axios'

export default {
    saveToken(token) {
        if (token) {
            cookies.set('token', token, {expires: 1});
            return true;
        } else {
            return false;
        }
    },
    getToken() {
        return cookies.get('token');
    },
    async obtainToken(username, password) {
        return await axios.post('/api/auth/obtain_token',
            {
                password, username
            },
            {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            });
    },
    destroyToken() {
        cookies.remove('token');
    },
    async signup(username, password1, password2) {
        return await axios.post('/api/auth/signup',
            {
                password1, password2, username
            });
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