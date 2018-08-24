<template>
    <div id="image-uploader">
        <b-jumbotron class="m-5" header="Painted Skies" lead="Завантажте файл:">
            <b-form-file type="file" @change="onFileChange" placeholder="Виберіть файл..."></b-form-file>
        </b-jumbotron>
    </div>
</template>

<script>
    export default {
        name: "ImageUploader",
        methods: {
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
                    let image = e.target.result;
                    vm.$root.$emit('imageUploaded', image);
                };

                reader.readAsDataURL(file);
            },
        }
    }
</script>

<style scoped>

</style>