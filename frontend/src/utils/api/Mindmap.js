import $ from 'jquery'
import Auth from '../auth'

export default {
    async list() {
        try {
            return await $.ajax({
                url: '/api/rest/mindmaps/',
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + Auth.getToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': $.cookie('csrftoken'),
                }
            });
        } catch (e) {
            return false;
        }
    },
    async create(title, nodes, edges) {
        return await $.ajax({
            url: '/api/rest/mindmaps/',
            data: {
                title,
                mindmap: JSON.stringify({
                    nodes, edges,
                })
            },
            method: 'POST',
            headers: {
                'Authorization': 'Bearer ' + Auth.getToken(),
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        });
    },
    async retrieve(id) {
        return await $.ajax({
            url: '/api/rest/mindmaps/' + id + '/',
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + Auth.getToken(),
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        })
    },
    async update(id, title, nodes, edges) {
        return await $.ajax({
            url: '/api/rest/mindmaps/' + id + '/',
            data: {
                title,
                mindmap: JSON.stringify({
                    nodes, edges,
                })
            },
            method: 'PUT',
            headers: {
                'Authorization': 'Bearer ' + Auth.getToken(),
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        });
    },
    async delete(id) {
        return await $.ajax({
            url: '/api/rest/mindmaps/' + id + '/',
            method: 'DELETE',
            headers: {
                'Authorization': 'Bearer ' + Auth.getToken(),
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        });
    },
}