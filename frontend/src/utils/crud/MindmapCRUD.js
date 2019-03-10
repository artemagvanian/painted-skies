import $ from 'jquery'

export default {
    async list(token) {
        try {
            return await $.ajax({
                url: '/api/rest/mindmaps/',
                method: 'GET',
                headers: {
                    'Authorization': 'JWT ' + token,
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': $.cookie('csrftoken'),
                }
            });
        } catch (e) {
            return false;
        }
    },
    async create(token, title, nodes, edges) {
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
                'Authorization': 'JWT ' + token,
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        });
    },
    async retrieve(token, id) {
        return await $.ajax({
            url: '/api/rest/mindmaps/' + id + '/',
            method: 'GET',
            headers: {
                'Authorization': 'JWT ' + token,
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        })
    },
    async update(token, id, title, nodes, edges) {
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
                'Authorization': 'JWT ' + token,
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        });
    },
    async delete(token, id) {
        return await $.ajax({
            url: '/api/rest/mindmaps/' + id + '/',
            method: 'DELETE',
            headers: {
                'Authorization': 'JWT ' + token,
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': $.cookie('csrftoken'),
            }
        });
    },
}