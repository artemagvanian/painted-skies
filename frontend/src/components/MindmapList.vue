<template>
    <v-container fluid full-height>
        <v-layout row wrap>
            <v-flex md3 pa-3 sm6 v-for="mindmap in mindmaps" xs12>
                <v-card class="white--text pa-3" color="blue-grey darken-2">
                    <v-card-title primary-title>
                        <div>
                            <h3 class="headline mb-2"> {{ mindmap.title }}</h3>
                            <div>
                                <p>Створено {{ moment.utc(mindmap.created_at).fromNow() }}</p>
                                <p>Змінено {{ moment.utc(mindmap.edited_at).fromNow() }}</p>
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
    import Mindmaps from '../utils/api/Mindmap'
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
                let mindmaps = await Mindmaps.list();
                this.mindmaps = mindmaps.data;
            } catch (e) {
                this.$router.push('/');
            }
        }
    }
</script>

