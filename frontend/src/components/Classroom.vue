<template>
    <v-container fill-height fluid>
        <v-layout align-center justify-center>
            <v-flex md4 sm8 xs12>
                <v-card class="elevation-12">
                    <v-toolbar color="primary" dark>
                        <v-toolbar-title>Виберіть конспекти для порівняння</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-select :items="classrooms" @change="onClassroomChange"
                                  placeholder="Виберіть клас учня" v-model="selectedClassroom"></v-select>
                        <v-select :items="pupils" @change="onPupilChange" placeholder="Виберіть учня"
                                  v-model="selectedPupil"></v-select>
                        <v-select :items="mindmaps" placeholder="Виберіть конспект учня"
                                  v-model="selectedMindmap"></v-select>
                        <v-select :items="myMindmaps" placeholder="Виберіть свій конспект"
                                  v-model="selectedMyMindmap"></v-select>
                    </v-card-text>
                    <v-card-actions>
                        <p>{{ similarity }}</p>
                        <v-spacer></v-spacer>
                        <v-btn @click="onSubmit" color="primary">Порівняти</v-btn>
                    </v-card-actions>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import Classrooms from '../utils/api/Classroom'
    import Users from '../utils/api/User'
    import Mindmaps from '../utils/api/Mindmap'
    import Auth from '../utils/auth'
    import $ from 'jquery'

    export default {
        name: "Classroom",
        data() {
            return {
                classrooms: [],
                pupils: [],
                mindmaps: [],
                myMindmaps: [],
                selectedClassroom: null,
                selectedPupil: null,
                selectedMindmap: null,
                selectedMyMindmap: null,
                similarity: '',
            }
        },
        methods: {
            async onSubmit() {
                let response = await $.ajax({
                    url: '/api/compare',
                    data: {
                        a: this.selectedMindmap,
                        b: this.selectedMyMindmap,
                    },
                    method: 'GET',
                    headers: {
                        'Authorization': 'Bearer ' + Auth.getToken(),
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': $.cookie('csrftoken'),
                    }
                });
                this.similarity = 'Індекс схожості: ' + response.index;
            },
            parseMindmaps(mindmaps) {
                return mindmaps.map(dat => {
                    return {
                        text: dat.title,
                        value: dat.id,
                    }
                })
            },
            parseClassrooms(classrooms) {
                return classrooms.map(dat => {
                    return {
                        text: dat.title,
                        value: dat.id,
                    }
                })
            },
            async onClassroomChange() {
                let classroom = await Classrooms.retrieve(this.selectedClassroom);
                this.pupils = classroom.students.map(dat => {
                    return {
                        text: dat.user.username,
                        value: dat.user.id,
                    }
                });

            },
            async onPupilChange() {
                let pupil = await Users.retrieve(this.selectedPupil);
                this.mindmaps = pupil.mindmaps.map(dat => {
                    return {
                        text: dat.title,
                        value: dat.id,
                    }
                })
            }
        },
        async mounted() {
            this.classrooms = this.parseClassrooms(await Classrooms.list());
            this.myMindmaps = this.parseMindmaps(await Mindmaps.list())
        }
    }
</script>

<style scoped>

</style>