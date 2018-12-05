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

            <router-link :to="{
                    name: 'canvas',
                    params: { lang: this.language, image: this.image },
                }" tag="div">
                <b-button size="lg"
                          variant="success"
                          :disabled="!imageProcessed">
                    Поїхали!
                </b-button>
            </router-link>
        </b-jumbotron>
    </div>
</template>

<script>
    import $ from 'jquery'

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
                imageProcessed: false,
                image: null,
                firstPage: 1,
                lastPage: 1,
            }
        },
        methods: {
            onFileChange(e) {
                let files = e.target.files || e.dataTransfer.files, vm = this;
                if (!files.length)
                    return;

                let fd = new FormData;

                fd.append('pdf', files[0]);
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
                            'X-CSRFToken': $("[name=csrfmiddlewaretoken]").val(),
                        }
                    }
                ).then((file) => {
                    this.imageProcessed = true;
                    this.image = file;

                })
            },
        }
    }
</script>

<style scoped>

</style>