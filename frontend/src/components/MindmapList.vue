<template>
    <div class="container">
        <div class="row mb-5">
            <div class="col-xs-12 col-md-6 col-lg-4 mt-5"
                 v-for="mindmap in mindmaps">
                <div class="card border-info">
                    <div class="card-body">
                        <h5 class="card-title text-center"> {{ mindmap.title }}</h5>
                        <router-link
                                :to="{ name: 'mindmap', params: { id: mindmap.id }}"
                                tag="div">
                            <div class="btn btn-block btn-info">Редагувати</div>
                        </router-link>
                    </div>
                    <div class="card-footer">
                        <small class="text-muted"> {{ moment.utc(mindmap.created_at).fromNow() }}</small>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import $ from 'jquery'
    import 'jquery.cookie/jquery.cookie'
    import moment from 'moment'

    export default {
        name: "MindmapList",
        data() {
            return {
                mindmaps: [],
                moment,
            }
        },
        async mounted() {
            moment.locale('uk');
            try {
                this.mindmaps = await $.ajax({
                    url: '/api/rest/mindmaps/',
                    method: 'GET',
                    headers: {
                        'Authorization': 'JWT ' + this.$session.get('jwt'),
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': $.cookie('csrftoken'),
                    }
                });
                this.mindmaps.sort((a, b) => {
                    return moment.utc(a.created_at) > moment.utc(b.created_at) ? -1 : 1;
                })
            } catch (e) {
                this.$router.push('/');
            }
        }
    }
</script>

<style>
    html, body, #app {
        height: 100%;
        overflow: visible;
        margin: 0;
    }
</style>

