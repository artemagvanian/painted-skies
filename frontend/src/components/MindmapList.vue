<template>
    <v-container fluid full-height>
        <v-layout row wrap>
            <v-flex xs12 sm6 md3 pa-3 v-for="mindmap in mindmaps">
                <v-card color="blue-grey darken-2" class="white--text pa-3">
                    <v-card-title primary-title>
                        <div>
                            <h3 class="headline mb-2"> {{ mindmap.title }}</h3>
                            <div>
                                <p>Створено {{ moment.utc(mindmap.created_at).fromNow() }}</p>
                            </div>
                        </div>
                    </v-card-title>
                    <v-card-actions>
                        <router-link
                                :to="{ name: 'mindmap', params: { id: mindmap.id }}"
                                tag="div">
                            <v-btn>Редагувати</v-btn>
                        </router-link>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
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

