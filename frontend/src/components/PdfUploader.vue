<template>
    <v-container fill-height fluid>
        <v-layout>
            <v-flex>
                <v-card>
                    <v-toolbar>
                        <h1>Завантажте файл</h1>
                    </v-toolbar>
                    <v-card-text>
                        <v-btn @click="$refs.inputUpload.click()" block color="info">Натисніть, щоб вибрати документ на
                            комп'ютері
                        </v-btn>
                        <input @change="onFileChange" ref="inputUpload" type="file" v-show="false">
                        <v-select
                                :items="options"
                                class="mt-4"
                                label="Виберіть мову конспектування"
                                v-model="language"
                        ></v-select>
                        <v-text-field
                                class="mt-3"
                                label="Введіть сторінку, з якої почнете конспектувати"
                                type="number"
                                v-model="firstPage"
                        ></v-text-field>
                        <v-text-field
                                class="mt-3"
                                label="Введіть сторінку, на якій закінчите конспектувати"
                                type="number"
                                v-model="lastPage"
                        ></v-text-field>

                        <v-btn @click="uploadPdf()"
                               block
                               color="success" size="lg">
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