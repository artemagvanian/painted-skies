import Auth from '../auth'
import axios from 'axios';
import cookies from "js-cookie";

export default {
    async list() {
        return await axios.get('/api/rest/mindmaps/',
            {
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            });
    },
    async create(title, nodes, edges) {
        return await axios.post('/api/rest/mindmaps/',
            {
                title,
                mindmap: JSON.stringify({
                    nodes, edges,
                })
            },
            {
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            });
    },
    async retrieve(id) {
        return await axios.get('/api/rest/mindmaps/' + id + '/',
            {
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            })
    },
    async update(id, title, nodes, edges) {
        return await axios.put('/api/rest/mindmaps/' + id + '/',
            {
                title,
                mindmap: JSON.stringify({
                    nodes, edges,
                })
            },
            {
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            });
    },
    async delete(id) {
        return await axios.delete('/api/rest/mindmaps/' + id + '/',
            {
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': cookies.get('csrftoken'),
                }
            });
    },
}