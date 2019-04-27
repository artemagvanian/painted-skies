<template>
    <v-container fill-height fluid>
        <v-layout>
            <v-flex>
                <v-card>
                    <v-toolbar>
                        <h1>{{ $t('uploader.uploadFile') }}</h1>
                    </v-toolbar>
                    <v-card-text>
                        <v-btn @click="$refs.inputUpload.click()" block color="info">
                            {{ $t('uploader.clickToSelectDocument') }}
                        </v-btn>
                        <input @change="onFileChange" ref="inputUpload" type="file" v-show="false">
                        <v-select
                                :items="options"
                                :label="$t('uploader.selectLanguage')"
                                class="mt-4"
                                v-model="language"
                        ></v-select>
                        <v-text-field
                                :label="$t('uploader.selectFirstPage')"
                                class="mt-3"
                                type="number"
                                v-model="firstPage"
                        ></v-text-field>
                        <v-text-field
                                :label="$t('uploader.selectLastPage')"
                                class="mt-3"
                                type="number"
                                v-model="lastPage"
                        ></v-text-field>

                        <v-btn @click="uploadPdf()" block color="success" size="lg">
                            {{ $t('uploader.start') }}
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
                    {text: this.$t('languages.ukrainian'), value: 'ukr'},
                    {text: this.$t('languages.english'), value: 'eng'},
                    {text: this.$t('languages.russian'), value: 'rus'},
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
                    window.alert(this.$t('serverErrorMessage.shortText'));
                })
            }
        }
    }
</script>