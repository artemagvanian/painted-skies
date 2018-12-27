<template>
    <div id="pdf-uploader">
        <b-jumbotron class="m-5" header="Painted Skies" lead="Завантажте файл:">
            <b-form-file type="file" @change="onFileChange" placeholder="Виберіть файл..."></b-form-file>
            <b-form-group label="Виберіть мову:" class="mt-3">
                <b-form-select :options="options"
                               required
                               v-model="language">
                </b-form-select>
            </b-form-group>
            <label for="first-page">Введіть сторінку, з якої почнете конспектувати: </label>
            <b-form-input type="number" id="first-page" min="1" v-model="firstPage"></b-form-input>
            <label for="last-page">Введіть сторінку, на якій закінчите: </label>
            <b-form-input type="number" id="last-page" min="1" v-model="lastPage"></b-form-input>

            <b-button size="lg"
                      variant="success"
                      class="mt-3"
                      @click="uploadPdf()">
                Поїхали!
            </b-button>
        </b-jumbotron>
    </div>
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

<style scoped>

</style>