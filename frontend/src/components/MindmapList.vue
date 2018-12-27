<template>
    <ul>
        <li v-for="mindmap in mindmaps">
            {{ mindmap.title }}
        </li>
    </ul>
</template>

<script>
    import $ from 'jquery'
    import 'jquery.cookie/jquery.cookie'

    export default {
        name: "MindmapList",
        data() {
            return {
                mindmaps: [],
            }
        },
        async mounted() {
            try {
                this.mindmaps = await $.ajax({
                    url: '/api/rest/mindmaps/',
                    method: 'GET',
                    headers: {
                        'Authorization': 'JWT ' + this.$session.get('jwt'),
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': $.cookie('csrftoken'),
                    }
                })
            } catch (e) {
                this.$router.push('/');
            }
        }
    }
</script>

<style scoped>

</style>