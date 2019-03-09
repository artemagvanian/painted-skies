<template>
    <v-container fluid fill-height>
        <v-layout>
            <v-flex>
                <v-card>
                    <v-toolbar>
                        <h1>Завантажте файл</h1>
                    </v-toolbar>
                    <v-card-text>
                        <v-btn color="info" @click="$refs.inputUpload.click()">Виберіть документ на комп'ютері</v-btn>
                        <input v-show="false" ref="inputUpload" type="file" @change="onFileChange">
                        <v-select
                                :items="options"
                                label="Виберіть мову конспектування"
                                v-model="language"
                                class="mt-4"
                        ></v-select>
                        <v-text-field
                                label="Введіть сторінку, з якої почнете конспектувати"
                                v-model="firstPage"
                                type="number"
                                class="mt-3"
                        ></v-text-field>
                        <v-text-field
                                label="Введіть сторінку, на якій закінчите конспектувати"
                                v-model="lastPage"
                                type="number"
                                class="mt-3"
                        ></v-text-field>

                        <v-btn size="lg"
                               color="success"
                               @click="uploadPdf()">
                            Поїхали!
                        </v-btn>
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import $ from 'jquery'
    import 'jquery.cookie/jquery.cookie'

    export default {
        name: "PdfUploader",
        data() {
            return {
                options: [
                    {text: 'Українська', value: 'ukr'},
                    {text: 'Англійська', value: 'eng'},
                    {text: 'Російська', value: 'rus'},
                ],
                language: 'eng',
                file: null,
                firstPage: 1,
                lastPage: 1,
            }
        },
        methods: {
            onFileChange(e) {
                let files = e.target.files || e.dataTransfer.files;
                if (!files.length)
                    return;

                this.file = files[0];
            },
            uploadPdf() {
                let fd = new FormData;

                fd.append('pdf', this.file);
                fd.append('first', this.firstPage.toString());
                fd.append('last', this.lastPage.toString());

                $.ajax(
                    {
                        method: 'POST',
                        url: '/api/pdf',
                        data: fd,
                        processData: false,
                        contentType: false,

                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': $.cookie('csrftoken'),
                        }
                    }
                ).then((image) => {
                    this.$router.push({
                        name: 'canvas',
                        params: {lang: this.language, image},
                    });
                }).catch(() => {
                    window.alert("Сталася помилка! Спробуйте оновити сторінку!");
                })
            }
        }
    }
</script>