import $ from "jquery";
import Auth from '../auth'

export default {
    async retrieve(id) {
        return await $.ajax({
            url: '/api/rest/classrooms/' + id + '/',
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + Auth.getToken(),
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        })
    },
    async list() {
        return await $.ajax({
            url: '/api/rest/classrooms/',
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + Auth.getToken(),
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        })
    },
}