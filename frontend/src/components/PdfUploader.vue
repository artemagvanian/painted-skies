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
            <router-link :to="{
                    name: 'canvas',
                    params: { lang: this.language, image: this.image },
                }" tag="div">
                <b-button size="lg"
                          variant="success">
                    Поїхали!
                </b-button>
            </router-link>
            <b-button @click="showData()">Show</b-button>
        </b-jumbotron>
    </div>
</template>

<script>
    let pdfjs = require("pdfjs-dist/webpack");
    import range from 'lodash/range'

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
                canvases: [],
            }
        },
        methods: {
            showData() {
                console.log(this.canvases);
            },
            onFileChange(e) {
                let files = e.target.files || e.dataTransfer.files;
                if (!files.length)
                    return;
                this.createFile(files[0]);
            },
            createFile(file) {
                let reader = new FileReader();
                let vm = this;
                reader.onload = (e) => {
                    pdfjs
                        .getDocument(e.target.result)
                        .then((pdf) => {
                            const pagePromises = range(1, pdf.numPages).map(number => pdf.getPage(number));
                            return Promise.all(pagePromises)
                        }).then((pages) => {
                            const scale = 2;
                            pages.forEach(page => {
                                const viewport = page.getViewport(scale);

                                // Prepare canvas using PDF page dimensions
                                const canvas = document.createElement('canvas');
                                canvas.height = viewport.height;
                                canvas.width = viewport.width;

                                // Render PDF page into canvas context
                                const canvasContext = canvas.getContext('2d');
                                const renderContext = {canvasContext, viewport};
                                page.render(renderContext).then(() => console.log('Page rendered'));
                                vm.canvases.push(canvas);
                            });
                        },
                        error => console.log('Error', error),
                    )
                };
                reader.readAsDataURL(file);
            }
        }
    }
</script>

<style scoped>

</style>