import Auth from '../auth'
import axios from 'axios'
import cookies from 'js-cookie'

export default {
    async retrieve(id) {
        return await axios.get('/api/rest/classrooms/' + id + '/',
            {
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            })
    },
    async list() {
        return await axios.get('/api/rest/classrooms/',
            {
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            })
    },
}