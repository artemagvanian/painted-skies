<template>
    <div id="image-uploader">
        <b-jumbotron class="m-5" header="Painted Skies" lead="Завантажте файл:">
            <b-form-file type="file" @change="onFileChange" placeholder="Виберіть файл..." accept="image/*"></b-form-file>
            <b-form-group label="Виберіть мову:" class="mt-3">
                <b-form-select :options="options"
                               required
                               v-model="language">
                </b-form-select>
            </b-form-group>
            <b-button size="lg"
                      variant="success"
                      @click="buttonClick()">
                Поїхали!
            </b-button>
        </b-jumbotron>
    </div>
</template>

<script>
    export default {
        name: "ImageUploader",
        data() {
            return {
                options: [
                    {text: 'Українська', value: 'ukr'},
                    {text: 'Англійська', value: 'eng'},
                    {text: 'Російська', value: 'rus'},
                ],
                language: 'eng',
                image: null,
            }
        },
        methods: {
            buttonClick() {
                this.$root.$emit('imageUploaded', {'image': this.image, 'lang': this.language});
            },
            onFileChange(e) {
                let files = e.target.files || e.dataTransfer.files;
                if (!files.length)
                    return;
                this.createImage(files[0]);
            },
            createImage(file) {
                let reader = new FileReader(),
                    vm = this;

                reader.onload = (e) => {
                    vm.image = e.target.result;
                };

                reader.readAsDataURL(file);
            },
        }
    }
</script>

<style scoped>

</style>