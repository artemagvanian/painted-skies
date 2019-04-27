<template>
    <v-container fill-height fluid>
        <v-layout align-center justify-center>
            <v-flex md4 sm8 xs12>
                <v-card class="elevation-12">
                    <v-toolbar color="primary" dark>
                        <v-toolbar-title>{{ $t("classroom.selectNotesForComparison") }}</v-toolbar-title>
                    </v-toolbar>
                    <v-card-text>
                        <v-select :items="classrooms" :placeholder="$t('classroom.selectGroup')"
                                  @change="onClassroomChange" v-model="selectedClassroom"></v-select>
                        <v-select :items="pupils" :placeholder="$t('classroom.selectStudent')" @change="onPupilChange"
                                  v-model="selectedPupil"></v-select>
                        <v-select :items="mindmaps" :placeholder="$t('classroom.selectStudentNotes')"
                                  v-model="selectedMindmap"></v-select>
                        <v-select :items="myMindmaps" :placeholder="$t('classroom.selectTeacherNotes')"
                                  v-model="selectedMyMindmap"></v-select>
                    </v-card-text>
                    <v-card-actions>
                        <p>{{ similarity }}</p>
                        <v-spacer></v-spacer>
                        <v-btn @click="onSubmit" color="primary">{{ $t("classroom.compare") }}</v-btn>
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
                this.similarity = this.$t("classroom.similarityIndex") + ': ' + response.index + '%';
            },
            parseMindmaps(mindmaps) {
                return mindmaps.data.map(dat => {
                    return {
                        text: dat.title,
                        value: dat.id,
                    }
                })
            },
            parseClassrooms(classrooms) {
                return classrooms.data.map(dat => {
                    return {
                        text: dat.title,
                        value: dat.id,
                    }
                })
            },
            async onClassroomChange() {
                let classroom = await Classrooms.retrieve(this.selectedClassroom);
                this.pupils = classroom.data.students.map(dat => {
                    return {
                        text: dat.username,
                        value: dat.id,
                    }
                });

            },
            async onPupilChange() {
                let pupil = await Users.retrieve(this.selectedPupil);
                this.mindmaps = pupil.data.mindmaps.map(dat => {
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